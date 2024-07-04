from flask import Flask
from controllers.getEchoChamberStatus import echo_chamber_info_routes
import firebase_admin

app = Flask(__name__)
firebase_admin.initialize_app(options = {"databaseURL": "https://echo-chamber-427700-default-rtdb.firebaseio.com/"})
app.register_blueprint(echo_chamber_info_routes)

# Gunicorn is used to run server
