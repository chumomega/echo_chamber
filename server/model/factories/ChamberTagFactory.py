from model.ChamberType import ChamberType
from context_initializers import get_gemini, get_firebase
from model.Chamber import Chamber
from model.factories.ChamberFactory import ChamberFactory
from model.factories.ChamberMemberFactory import ChamberMemberFactory
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class ChamberTagFactory:

    def __init__(self) -> None:
        return

    def get_chamber_tags(self, identifier: str, chamber_type: str) -> list:
        match chamber_type:
            case ChamberType.YOUTUBE.value:
                return self.get_youtube_chamber_tags(identifier)
            case _:
                raise Exception(f"Unsupported chamber type: {chamber_type}")

    def get_youtube_chamber_tags(self, identifier: str) -> Chamber:
        logger.info(f"Retrieving chamber tags for {identifier}...")
        firebase_client = get_firebase()
        chamber_tags_from_db = firebase_client.get_chamber_tags(
            identifier, ChamberType.YOUTUBE
        )
        if len(chamber_tags_from_db) > 0:
            logger.info(
                f"Successfully got chamber tags for {identifier} from firebase..."
            )
            return chamber_tags_from_db

        chamber_x = ChamberFactory().get_chamber(
            identifier=identifier, chamber_type=ChamberType.YOUTUBE.value
        )
        chamber_members = ChamberMemberFactory().get_chamber_members(
            identifier=identifier, chamber_type=ChamberType.YOUTUBE.value
        )

        gemini_client = get_gemini()
        tags = gemini_client.get_tags_for_chamber(
            chamber=chamber_x, comments=chamber_members
        )
        firebase_client.add_chamber_tags(identifier, ChamberType.YOUTUBE, tags)
        return tags
