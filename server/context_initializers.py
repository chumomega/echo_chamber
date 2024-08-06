from flask import g
from model.FirebaseClient import FirebaseClient
from model.YoutubeClient import YoutubeClient
from model.RedditClient import RedditClient
from model.GeminiClient import GeminiClient
from model.TwitterClient import TwitterClient


# add firebase client to Flask application context so only 1 instance of firebase running per Flask request
def get_firebase() -> FirebaseClient:
    if "firebase" not in g:
        g.firebase = FirebaseClient()

    return g.firebase


# add youtube client to Flask application context so only 1 instance of youtube running per Flask request
def get_youtube() -> YoutubeClient:
    if "youtube" not in g:
        g.youtube = YoutubeClient()

    return g.youtube


# add reddit client to Flask application context so only 1 instance of youtube running per Flask request
def get_reddit() -> RedditClient:
    if "reddit" not in g:
        g.reddit = RedditClient()

    return g.reddit


# add twitter client to Flask application context so only 1 instance of youtube running per Flask request
def get_twitter() -> TwitterClient:
    if "twitter" not in g:
        g.twitter = TwitterClient()

    return g.twitter


# add gemini client to Flask application context so only 1 instance of gemini running per Flask request
def get_gemini() -> GeminiClient:
    if "gemini" not in g:
        g.gemini = GeminiClient()

    return g.gemini
