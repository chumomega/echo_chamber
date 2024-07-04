from flask import request, Blueprint
from dotenv import load_dotenv
# Import libraries
from googleapiclient.discovery import build
from os import environ
import google.generativeai as genai
import logging
from utils.text_api import TextAPI
from context_initializers.firebase_initializers import get_firebase
from model.Chamber import Chamber
from model.ChamberType import ChamberType
load_dotenv()     # this loads in the environment variables from the .env file

# TODO - abstract to env variabls
YOUTUBE_DATA_API_KEY = environ.get('YOUTUBE_DATA_API_KEY')
GEMINI_API_KEY = environ.get('GEMINI_API_KEY')
MAX_OPINIONS = 5

# Create a blueprint with a name and import name
echo_chamber_info_routes = Blueprint("echo_chamber_info_routes", __name__)

@echo_chamber_info_routes.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@echo_chamber_info_routes.route("/getEchoChamberStatus")
def get_echo_chamber_status():
    identifier = request.args.get('identifier')
    chamber_type = request.args.get('chamber_type')
    validateInput(identifier, chamber_type)
    
    youtube_client = getYoutubeClient()
    video_request = youtube_client.videos().list(
        part="snippet",
        id=identifier,
        maxResults=MAX_OPINIONS
    )
    video_response = video_request.execute()

    chamber_x = Chamber(
        id = identifier, 
        title = video_response["items"][0]["snippet"]["title"],
        description = video_response["items"][0]["snippet"]["description"],
        author = video_response["items"][0]["snippet"]["channelTitle"])

    firebase_client = get_firebase()
    firebase_client.add_chamber(chamber_x, chamber_type)

    comment_thread_request = youtube_client.commentThreads().list(
        part="snippet",
        videoId=identifier,
        maxResults=MAX_OPINIONS
    )
    threads_response  = comment_thread_request.execute()
    logging.info("Number of opinions received from youtube: {}".format(len(threads_response["items"])))

    # TODO - get_chamber_labels(commentThreads) -> list:
    # TODO - get_aggregated_chamber_status(chamber_labels) -> dict:

    text_api = TextAPI(GEMINI_API_KEY)
    return {
        "isChamber": True,
        "chamberLabel": "right-wing",
        "chamberMagnitude": 9,
        "chamberReasoning": text_api.get_response_from_ai("what is your name?")
    }

def validateInput(identifier: str, chamber_type: str) -> None:
    if identifier is None:
        raise Exception(f"Bad identifier: {identifier}")
    elif not chamber_type.isdigit():
        raise Exception(f"Bad chamber type: {chamber_type}")
    elif not ChamberType.has_value(int(chamber_type)):
        raise Exception(f"Unsupported chamber type: {chamber_type}")
    else:
        return

def getYoutubeClient():
    # Build the YouTube service object
    return build("youtube", "v3", developerKey=YOUTUBE_DATA_API_KEY)

