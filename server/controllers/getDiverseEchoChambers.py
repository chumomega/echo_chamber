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

    chamber_tag_factory = ChamberTagFactory()
    chamber_tags = chamber_tag_factory.get_chamber_tags(
        identifier=identifier, chamber_type=chamber_type
    )

    chamber_factory = ChamberFactory()
    chamber = chamber_factory.get_chamber(
        identifier=identifier, chamber_type=chamber_type
    )
    similar_tag_chamber_ids = chamber_factory.get_similar_chambers_ids(
        chamber_type=chamber_type, tags=chamber_tags
    )

    similar_tag_chambers = chamber_factory.get_chambers(
        map(lambda chamber_id: (chamber_id, "youtube"), similar_tag_chamber_ids)
    )
    filtered_similar_chambers = list(
        filter(
            lambda sim_tag_chamber: sim_tag_chamber != None
            and sim_tag_chamber.get_chamber_status() != None
            and sim_tag_chamber.get_chamber_status() != chamber.get_chamber_status(),
            similar_tag_chambers,
        )
    )
    similar_chamber_urls = chamber_factory.get_similar_youtube_chamber_urls(
        tags=chamber_tags
    )

    data = {
        "chamberTags": chamber_tags,
        "diverseChambers": list(similar_chamber_urls),
        "diverseChamberObjects": list(
            map(lambda chamber: chamber.get_serialized(), filtered_similar_chambers)
        ),
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
