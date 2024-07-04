from flask import g
from model.FirebaseClient import FirebaseClient

def get_firebase() -> FirebaseClient:
    if 'firebase' not in g:
        # add firebase client to Flask application context so only 1 instance of firebase running per Flask request
        g.firebase = FirebaseClient()

    return g.firebase
