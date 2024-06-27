from flask import Flask, request
# Import libraries
from googleapiclient.discovery import build
import google.generativeai as genai
import logging

# TODO - abstract to env variabls
YOUTUBE_DATA_API_KEY = "AIzaSyCDCTZp4MaApIyX4r5aUOXE5Fjbnu9TPKw"
MAX_OPINIONS = 5

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/getEchoChamberStatus")
def get_echo_chamber_status():
    identifier = request.args.get('identifier')
    chamber_type = request.args.get('chamber_type')
    validateInput(identifier, chamber_type)
    
    # TODO - support other internet spaces like X and Reddit
    if chamber_type != "youtube":
        raise Exception(f"Chamber type not supported: {chamber_type}")
    
    youtube_client = getYoutubeClient()
    comment_thread_request = youtube_client.commentThreads().list(
        part="snippet",
        videoId=identifier,
        maxResults=MAX_OPINIONS
    )
    threads_response  = comment_thread_request.execute()
    logging.info("Number of opinions received from youtube: {}".format(len(threads_response["items"])))

    # TODO - get_chamber_labels(commentThreads) -> list:
    # TODO - get_aggregated_chamber_status(chamber_labels) -> dict:

    return {
        "isChamber": True,
        "chamberLabel": "right-wing",
        "chamberMagnitude": 9,
        "chamberReasoning": "Because I said so"
    }

def validateInput(identifier, chamber_type) -> None:
    if identifier is None or chamber_type is None:
        raise Exception(f"Empty input! identifier: {identifier} || chamber_type: {chamber_type}")
    else:
        return

def getYoutubeClient():
    # Build the YouTube service object
    return build("youtube", "v3", developerKey=YOUTUBE_DATA_API_KEY)
