from flask import request, Blueprint
from os import environ
from model.factories.ChamberFactory import ChamberFactory
from model.factories.ChamberMemberFactory import ChamberMemberFactory
from model.ChamberType import ChamberType
from flask import jsonify
from context_initializers import get_gemini, get_firebase
import logging
import lorem


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Create a blueprint with a name and import name
echo_chamber_reasoning_routes = Blueprint("echo_chamber_reasoning_routes", __name__)


@echo_chamber_reasoning_routes.route("/getEchoChamberReasoning")
def get_echo_chamber_reasoning():
    try:
        identifier = request.args.get("identifier")
        chamber_type = request.args.get("chamber_type")
        validateInput(identifier, chamber_type)

        chamber_x = ChamberFactory().get_chamber(
            identifier=identifier, chamber_type=chamber_type
        )

        chamber_reasoning = chamber_x.get_chamber_reasoning()
        if chamber_reasoning is None:
            logger.info("No chamber reasoning in db, trying to generate...")
            firebase_client = get_firebase()
            chamber_members = ChamberMemberFactory().get_chamber_members(
                identifier=identifier, chamber_type=chamber_type
            )
            chamber_reasoning = get_gemini().get_reasoning_for_comments(
                chamber_x, chamber_members
            )
            firebase_client.add_chamber_reasoning(
                identifier=identifier,
                chamber_type=chamber_type,
                chamber_reasoning=chamber_reasoning,
            )

        data = {"chamberReasoning": chamber_reasoning}
        response = jsonify(data)
        # TODO Replace with your frontend origin
        response.headers["Access-Control-Allow-Origin"] = "*"
        return response
    except Exception as e:
        logger.error(
            f"Could not get chamber reasoning for {identifier} on {chamber_type}", e
        )
        response = jsonify({"error": "Could not get chamber reasoning"})
        response.headers["Access-Control-Allow-Origin"] = "*"
        return response


def validateInput(identifier: str, chamber_type: str) -> None:
    if identifier is None or identifier == "":
        raise Exception(f"Bad identifier: {identifier}")
    elif not ChamberType.has_value(chamber_type):
        raise Exception(f"Unsupported chamber type: {chamber_type}")
    else:
        return
