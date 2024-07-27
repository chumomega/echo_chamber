from flask import request, Blueprint
from os import environ
from model.factories.ChamberFactory import ChamberFactory
from model.factories.ChamberMemberFactory import ChamberMemberFactory
from model.ChamberType import ChamberType
from flask import jsonify
from context_initializers import get_gemini
import logging
import lorem


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Create a blueprint with a name and import name
echo_chamber_reasoning_routes = Blueprint("echo_chamber_reasoning_routes", __name__)


@echo_chamber_reasoning_routes.route("/getEchoChamberReasoning")
def get_echo_chamber_reasoning():
    identifier = request.args.get("identifier")
    chamber_type = request.args.get("chamber_type")
    validateInput(identifier, chamber_type)
    
    chamber_x = ChamberFactory().get_chamber(
        identifier=identifier, chamber_type=chamber_type
    )
    chamber_members = ChamberMemberFactory().get_chamber_members(
        identifier=identifier, chamber_type=chamber_type
    )
    reasoning = get_gemini().get_reasoning_for_comments(chamber_members)
    data = {"chamberReasoning": reasoning}
    response = jsonify(data)
    # TODO Replace with your frontend origin
    response.headers["Access-Control-Allow-Origin"] = environ.get("CLIENT_ORIGIN")
    return response


def validateInput(identifier: str, chamber_type: str) -> None:
    if identifier is None or identifier == "":
        raise Exception(f"Bad identifier: {identifier}")
    elif not ChamberType.has_value(chamber_type):
        raise Exception(f"Unsupported chamber type: {chamber_type}")
    else:
        return
