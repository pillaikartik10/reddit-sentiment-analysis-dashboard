from dash_bootstrap_components._components.Label import Label
from dash_bootstrap_components._components.Row import Row
from dash_html_components.Br import Br
import praw
import pandas as pd
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from textblob import TextBlob
import numpy as np
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
from dash import no_update

#intialising PRAW agent
#enter your own unique credentials below!
reddit = praw.Reddit(client_id = '', client_secret = '', username = '', password = '', user_agent = '')

#getting the top post on r/soccer as the default url
subreddit = reddit.subreddit('soccer')
top_soccer = subreddit.top(limit = 1)
for x in top_soccer:
    default_url = x.url

#declaring the app, and connecting to external stylesheet
app = dash.Dash(external_stylesheets=[dbc.themes.LITERA])
server = app.server

app.title = "Reddit Sentiment Analysis"

#content of popover 
popover_children = [
    dbc.PopoverHeader("Comment Limit"),
    dbc.PopoverBody("Determines the amount of comments processed. Choose 1 for quick results, but with the possibility of not getting every comment. Choose None to get every comment but at the expense of larger running time."),
]

#about this project, contents
about_this_project = [html.Div("This is a simple beginner's project implementing Sentiment Analysis on the comments of a Reddit post, and displaying the results in graphical form."),
                      html.Br(),  
                      html.Div("Libraries used :"),
                      html.Div("Dash Plotly(For the front-end dashboard)"),
                      html.Div("PRAW(to extract comments from Reddit Post)"),
                      html.Div("TextBlob(For Sentiment Analysis)"),
                      html.Div("Plotly(For graphs)"),
                      html.Div("Numpy and Pandas(For processing the extracted comments)"),
                      html.Br(),
                      html.Div("Thanks for checking out this project!"),
                      html.Br(),
                      html.Div("Kartik Pillai"),
                      html.A("Code available on Github", href = "https://github.com/pillaikartik10/reddit-sentiment-analysis-dashboard",target='_blank')
                    ]

#the layout of the app
app.layout = html.Div(children=[
    html.Br(),

    dbc.Row(dbc.Col(html.H3("Reddit Sentiment Analysis App"),
                        width={'offset': 1},
                        ),
                ),  

    html.Br(),

    dbc.Row([dbc.Col(html.Label(children='''
        Enter Reddit Post URL(Default url is set as the top post on r/soccer) :
    '''),width={'offset':1}),
    dbc.Col(dcc.Input(id='input', value=default_url, type='text',size='70'))]),

    html.Br(),

    dbc.Row([dbc.Col(html.Label("Select Comment Limit : "),width={'offset':1}),    
    dbc.Col(dcc.Dropdown(id='select_limit',
        options=[
            {'label' : '1','value' : '1',},
            {'label' : 'None','value' : 'No'},
        ],
        value='1',
        searchable=False,
        optionHeight=25,
    
    ),width=1),
    dbc.Col([dbc.Button(
            "?",
            id="click-target",
            className="mr-1",
            n_clicks=0,
            color='dark'
        ),
        dbc.Popover(
            popover_children,
            id="click",
            target="click-target",
            trigger="click",
        )])
    
    ]),
    
    html.Br(),

    dbc.Row([dbc.Col(dbc.Button(id='submit',n_clicks=0,children='Submit',color='success'),width ={'offset' : 1}),
    dbc.Col(dbc.Button("About This Project", id="open",n_clicks=0,color='info'))]),
    
    html.Br(),

    dbc.Row([
        dbc.Col(html.Label(html.B("Title : ")),width={'offset':1}),
        dbc.Col(html.Div(id='output'))]),


    html.Br(),

    dbc.Row(
    dbc.Col([dcc.Tabs(id='graph-tabs', value='tab-1', children=[
        dcc.Tab(label='Bar Graph', value='tab-1'),
        dcc.Tab(label='Pie Chart', value='tab-2'),
    ]),
    dcc.Loading(id = 'loading-icon',children =[html.Div(id='output-graph')])]),justify='center'),

    dcc.Graph(id = 'table-info'),

    dbc.Modal(
            [
                dbc.ModalHeader("About This Project"),
                dbc.ModalBody(about_this_project),
                dbc.ModalFooter(
                    dbc.Button(
                        "Close", id="close", className="ml-auto", n_clicks=0
                    )
                ),
            ],
            id="modal",
            is_open=False,
        )
],style={'marginLeft' : 40, 'marginRight' : 40})


@app.callback(
    [Output(component_id='output', component_property='children'),
    Output(component_id='output-graph', component_property='children'),
    Output(component_id='table-info', component_property='figure')],
    [Input(component_id='submit',component_property='n_clicks'),
    Input(component_id='graph-tabs',component_property='value')],
    [State(component_id='input', component_property='value'),
    State(component_id='select_limit',component_property='value')]
)
def update_value(n_clicks,tab,input_data,limit):
    url = input_data

    #setting limit for extracting comments
    if limit == '1':
        l = 1
    elif limit == 'No':
        l = None

    #extracting comments
    try:
        submission = reddit.submission(url=url)
        post_comments = []
        submission.comments.replace_more(limit=l)
    except:
        return "Invalid URL, try again!", no_update,no_update

    for comment in submission.comments.list():
        post_comments.append(comment.body)

    #assigning senitment values to the extracted comments
    df = pd.DataFrame(post_comments)
    df['Sentiment'] = np.nan
    df.columns = ['Comment','Sentiment']
    
    for index, row in df.iterrows():
        comment_polarity = TextBlob(row['Comment']).sentiment.polarity
        df.at[index,'Sentiment'] = comment_polarity

    #removing invalid comments, and finding the number of positive, negative and invalid(zero) comments
    unwanted_index = []
    pos_index = 0
    neg_index = 0
    total_processed = len(post_comments)
    for index,row in df.iterrows():
        if row['Sentiment'] == 0.0:
            unwanted_index.append(index)
        elif row['Sentiment'] > 0.0:
            pos_index +=1
        elif row['Sentiment'] < 0.0:
            neg_index +=1

    final_data = df.drop(unwanted_index)
    final_data.reset_index(inplace=True)

    #finding post details

    d = {}
    d['id'] = submission.id
    d['num_comments'] = submission.num_comments
    d['score'] = submission.score
    d['ratio'] = submission.upvote_ratio
    d['date'] = datetime.fromtimestamp(submission.created_utc)
    d['domain'] = submission.domain
    d['gilded'] = submission.gilded
    d['num_crossposts'] = submission.num_crossposts
    d['nsfw'] = submission.over_18
    d['author'] = submission.author.name
    d['processed_comments'] = total_processed
    d['positive'] = pos_index
    d['negative'] = neg_index
    d['zero'] = len(unwanted_index)

    details = pd.DataFrame.from_dict([d])

    #setting the value of 'fig' on the basic of the tab selected by user - 1 for bar chart, 2 for pie chart
    if tab == 'tab-1':
        fig = dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': final_data.index, 'y': final_data.Sentiment, 'type': 'bar', 'name': 'Reddit Post'},
            ],
            'layout': {
                'title': 'Sentiment Analysis of Post comments using TextBlob',
                'xaxis_title': 'Sentiment'
            }
        }
    )
    elif tab == 'tab-2':
        labels = ['Positive','Negative','Zero/Invalid']
        values = [d['positive'],d['negative'],d['zero']]
        fig = dcc.Graph(id = 'example-graph',figure = px.pie(names = labels,values = values, title='Percentage of positive, negative and zero/invalid comments'))

    #returning the outputs
    return submission.title, fig, go.Figure(data=[go.Table(
        header=dict(values=['ID','Total no. of comments','Score','Upvote Ratio','Date','Domain','Awards','Crossposts','NSFW','Author','Total comments processed','Positive comments','Negative comments','Zero/Invalid sentiment comments'],
                    fill_color='lightblue',
                    align='left'),
        cells=dict(values=[details.id, details.num_comments, details.score, details.ratio,details.date,details.domain,details.gilded,details.num_crossposts,details.nsfw,details.author,details.processed_comments,details.positive,details.negative,details.zero],
                fill_color='lavender',
                align='left'),
        columnwidth = [1,1,1,1,2,1,1,1,1,1.5,1,1,1,1]),
    ],
    layout = go.Layout(
        title=go.layout.Title(text="Post Statistics"),
        title_x = 0.5
        
    )
    )
    
#callback to toggle 'about this project' modal window
@app.callback(
    Output("modal", "is_open"),
    [Input("open", "n_clicks"), Input("close", "n_clicks")],
    [State("modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


if __name__ == '__main__':
    app.run_server(debug=True)
