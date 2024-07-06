from flask import g
from model.FirebaseClient import FirebaseClient
from model.YoutubeClient import YoutubeClient
from model.GeminiClient import GeminiClient


# add firebase client to Flask application context so only 1 instance of firebase running per Flask request
def get_firebase() -> FirebaseClient:
    if 'firebase' not in g:
        g.firebase = FirebaseClient()

    return g.firebase


# add youtube client to Flask application context so only 1 instance of youtube running per Flask request
def get_youtube() -> YoutubeClient:
    if 'youtube' not in g:
        g.youtube = YoutubeClient()

    return g.youtube

# add gemini client to Flask application context so only 1 instance of gemini running per Flask request
def get_gemini() -> GeminiClient:
    if 'gemini' not in g:
        g.gemini = GeminiClient()

    return g.gemini

