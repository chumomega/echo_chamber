from flask import request, Blueprint
from os import environ
from context_initializers import get_gemini
from model.factories.ChamberFactory import ChamberFactory
from model.factories.ChamberMemberFactory import ChamberMemberFactory
from model.factories.ChamberTagFactory import ChamberTagFactory
from model.ChamberType import ChamberType
from flask import jsonify
import logging


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Create a blueprint with a name and import name
echo_chamber_recommendation_routes = Blueprint(
    "echo_chamber_recommendation_routes", __name__
)


@echo_chamber_recommendation_routes.route("/getDiverseEchoChambers")
def get_diverse_echo_chambers():
    identifier = request.args.get("identifier")
    chamber_type = request.args.get("chamber_type")
    validateInput(identifier, chamber_type)

    chamber_tags = ChamberTagFactory().get_chamber_tags(
        identifier=identifier, chamber_type=chamber_type
    )

    chamber_tags = ChamberFactory().get_chamber_tags(
        identifier=identifier, chamber_type=chamber_type
    )

    data = {"chamberTags": chamber_tags}
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
