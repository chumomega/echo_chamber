from flask import request, Blueprint
from os import environ
from context_initializers import get_firebase, get_youtube, get_gemini
from model.Chamber import Chamber
from model.ChamberType import ChamberType

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

    chamber_x = get_chamber(identifier=identifier, chamber_type=chamber_type)
    chamber_members = get_youtube_chamber_members(identifier=identifier)
    # TODO - get_chamber_labels(commentThreads) -> list:
    # TODO - get_aggregated_chamber_status(chamber_labels) -> dict:

    # text_api = TextAPI(GEMINI_API_KEY)
    # text_api.get_response_from_ai("what is your name?")
    return {
        "isChamber": True,
        "chamberLabel": "right-wing",
        "chamberMagnitude": 9,
        "chamberReasoning": 1
    }

def validateInput(identifier: str, chamber_type: str) -> None:
    if identifier is None:
        raise Exception(f"Bad identifier: {identifier}")
    elif not ChamberType.has_value(chamber_type):
        raise Exception(f"Unsupported chamber type: {chamber_type}")
    else:
        return

def get_chamber(identifier: str, chamber_type: str) -> Chamber:
    match chamber_type:
        case ChamberType.YOUTUBE.value:
            return get_youtube_chamber(identifier)
        case _:
            raise Exception(f"Unsupported chamber type: {chamber_type}")

def get_youtube_chamber(identifier: str) -> Chamber:
    firebase_client = get_firebase()
    chamber_from_db = firebase_client.get_chamber(identifier, ChamberType.YOUTUBE)
    if chamber_from_db is not None:
        return chamber_from_db
    
    youtube_client = get_youtube()
    chamber = youtube_client.get_video_chamber(identifier)
    firebase_client.add_chamber(chamber, ChamberType.YOUTUBE)
    return chamber

def get_youtube_chamber_members(identifier: str) -> Chamber:
    # firebase_client = get_firebase()
    # chamber_from_db = firebase_client.get_chamber(identifier, ChamberType.YOUTUBE)
    # if chamber_from_db is not None:
    #     return chamber_from_db
    
    firebase_client = get_firebase()
    youtube_client = get_youtube()
    video_comments = youtube_client.get_video_comments(identifier)

    gemini_client = get_gemini()
    comments_with_labels = gemini_client.get_labels_for_comments(video_comments)
    
    for comment in comments_with_labels:
        firebase_client.add_chamber_member(identifier, ChamberType.YOUTUBE, comment)

    # firebase_client.add_chamber(chamber, ChamberType.YOUTUBE)
    return video_comments
