from flask import request, Blueprint, jsonify
from model.ChamberType import ChamberType
from model.factories.ChamberFactory import ChamberFactory
from model.factories.ChamberMemberFactory import ChamberMemberFactory
from utils.comments import get_avg_label_magnitude, get_biased_chamber
from context_initializers import get_firebase
from os import environ
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

    chamber_x = ChamberFactory().get_chamber(
        identifier=identifier, chamber_type=chamber_type
    )
    biased_chamber = chamber_x.get_chamber_status()
    chamber_label_magnitudes = chamber_x.get_label_magnitudes()
    firebase_client = get_firebase()

    if chamber_label_magnitudes is None:
        logger.info("No label magnitudes in db, trying to generate...")
        chamber_members = ChamberMemberFactory().get_chamber_members(
            identifier=identifier, chamber_type=chamber_type
        )
        chamber_label_magnitudes = get_avg_label_magnitude(chamber_members)
        firebase_client.update_chamber_label_magnitudes(
            identifier=identifier,
            chamber_type=chamber_type,
            label_magnitudes=chamber_label_magnitudes,
        )

    if biased_chamber is None:
        logger.info("No chamber status in db, trying to generate...")
        biased_chamber = get_biased_chamber(chamber_label_magnitudes)
        firebase_client.add_chamber_status(
            identifier=identifier,
            chamber_type=chamber_type,
            chamber_status=biased_chamber,
        )

    data = {
        "isBiasedChamber": True if biased_chamber != None else False,
        "chamberLabelMagnitudes": chamber_label_magnitudes,
        "biasedChamber": biased_chamber,
    }
    response = jsonify(data)
    # TODO Replace with your frontend origin
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response


def validateInput(identifier: str, chamber_type: str) -> None:
    if identifier is None or identifier == "":
        raise Exception(f"Bad identifier: {identifier}")
    elif not ChamberType.has_value(chamber_type):
        raise Exception(f"Unsupported chamber type: {chamber_type}")
    else:
        return
