https://img.shields.io/website?down_color=red&down_message=Offline&up_color=green&up_message=Online&url=https%3A%2F%2Freddit-sentiment-app.herokuapp.com%2F  
  
# Reddit Post Sentiment Analysis Dashboard  
  
On providing a valid URL to a Reddit Post, sentiment analysis on the post comments is carried out. The sentiment scores thus obtained are shown in a graphical manner, along with the basic details of the post such as title, date of submission, upvotes etc.  
Hosted on Heroku, [here](https://reddit-sentiment-app.herokuapp.com/).  
  
## Overview  
  
[Reddit](https://www.reddit.com/) is a widely used social media website, with emphasis on social news aggregation, discussion and user content. In this project, we carry out sentiment analysis on the comments of a particular post, and show the results in graphical form. The extraction of comments is done using the [Python Reddit API Wrapper(PRAW)](https://praw.readthedocs.io/en/latest/), the front-end is developed using [Dash Plotly](https://dash.plotly.com/), the sentiment analysis is performed using [TextBlob](https://textblob.readthedocs.io/en/dev/), and the project is hosted on [Heroku](https://www.heroku.com/).  
  
## Dependencies Used  
  
1. plotly
2. dash_core_components  
3. praw  
4. dash_html_components  
5. numpy  
6. textblob  
7. dash  
8. pandas  
9. dash_bootstrap_components  
10. gunicorn(only needed if deploying on heroku etc, not necesssary if only running locally)  
  
All these dependencies, along with their version numbers, are given in the [requirements.txt](https://github.com/pillaikartik10/reddit-sentiment-analysis-dashboard/blob/main/requirements.txt) file. Using that file, you can install all the packages using a single terminal command,  
```
pip install -r requirements.txt
```  
  
## Running The Code  
  
This code **WILL NOT** run right out of the box!  
  
To initialise the PRAW Agent and to carry out comment extraction, we need to provide certain credentials which are obtained using our Reddit account. Check out how to get these credentials [here](https://github.com/reddit-archive/reddit/wiki/OAuth2-Quick-Start-Example#first-steps).  
  
Insert your credentials at line 20 of [reddit-demo.py](https://github.com/pillaikartik10/reddit-sentiment-analysis-dashboard/blob/main/reddit-demo.py),  
```
reddit = praw.Reddit(client_id = '', client_secret = '', username = '', password = '', user_agent = '')
```  
  
Now you are ready to run the code locally! To deploy this project on Heroku is a bit more work.  
  
To host your project on Heroku, you obviously need a Heroku account. After that, you also need Git and Heroku Command Line Interface(CLI) installed. Know more about it [here](https://devcenter.heroku.com/articles/heroku-cli).  
  
Once you have done all the above-mentioned steps, follow the simple steps for Heroku deployment provided [here](https://dash.plotly.com/deployment).  
  
**NOTE** :  
1. You do not need the [requirements.txt](https://github.com/pillaikartik10/reddit-sentiment-analysis-dashboard/blob/main/requirements.txt), or [Procfile](https://github.com/pillaikartik10/reddit-sentiment-analysis-dashboard/blob/main/Procfile), to run the project locally. They are necessary to deploy the application on Heroku.  
2. Creating a virtual environment isn't mandatory, even though it is a good practice. If you are not using a virtual environment, you do not necessarily need a .gitignore file. So you can avoid those steps.  
  
