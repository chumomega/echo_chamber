from flask import Flask
from os import environ
from controllers.getEchoChamberStatus import echo_chamber_info_routes

app = Flask(__name__)
app.register_blueprint(echo_chamber_info_routes)

# Gunicorn is used to run server
