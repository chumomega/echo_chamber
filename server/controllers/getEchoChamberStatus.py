from flask import Flask
import google.generativeai as genai


app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
