from flask import request, Blueprint
from model.ChamberType import ChamberType
from model.factories.ChamberFactory import ChamberFactory
from model.factories.ChamberMemberFactory import ChamberMemberFactory
import logging


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Create a blueprint with a name and import name
echo_chamber_info_routes = Blueprint("echo_chamber_info_routes", __name__)


@echo_chamber_info_routes.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@echo_chamber_info_routes.route("/getEchoChamberStatus")
def get_echo_chamber_status():
    identifier = request.args.get("identifier")
    chamber_type = request.args.get("chamber_type")
    validateInput(identifier, chamber_type)

    chamber_x = ChamberFactory().get_chamber(identifier=identifier, chamber_type=chamber_type)
    chamber_members = ChamberMemberFactory().get_youtube_chamber_members(identifier=identifier)
    # TODO - get_chamber_labels(commentThreads) -> list:
    # TODO - get_aggregated_chamber_status(chamber_labels) -> dict:

    # text_api = TextAPI(GEMINI_API_KEY)
    # text_api.get_response_from_ai("what is your name?")
    return {
        "isChamber": True,
        "chamberLabel": "right-wing",
        "chamberMagnitude": 9,
        "chamberReasoning": 1,
    }

def validateInput(identifier: str, chamber_type: str) -> None:
    if identifier is None or identifier == "":
        raise Exception(f"Bad identifier: {identifier}")
    elif not ChamberType.has_value(chamber_type):
        raise Exception(f"Unsupported chamber type: {chamber_type}")
    else:
        return