from model.ChamberType import ChamberType
from context_initializers import get_firebase, get_youtube
from model.Chamber import Chamber
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class ChamberFactory:

    def __init__(self) -> None:
        return

    def get_chamber(self, identifier: str, chamber_type: str) -> Chamber:
        match chamber_type:
            case ChamberType.YOUTUBE.value:
                return self._get_youtube_chamber(identifier)
            case ChamberType.REDDIT.value:
                return self._get_reddit_chamber(identifier)
            case ChamberType.X.value:
                return self._get_x_chamber(identifier)
            case _:
                raise Exception(f"Unsupported chamber type: {chamber_type}")

    def _get_youtube_chamber(self, identifier: str) -> Chamber:
        firebase_client = get_firebase()
        chamber_from_db = firebase_client.get_chamber(identifier, ChamberType.YOUTUBE)
        if chamber_from_db is not None:
            return chamber_from_db

        youtube_client = get_youtube()
        chamber = youtube_client.get_video_chamber(identifier)
        firebase_client.add_chamber(chamber, ChamberType.YOUTUBE)
        return chamber

    def _get_reddit_chamber(self, identifier: str) -> Chamber:
        raise NotImplementedError
    
    def _get_x_chamber(self, identifier: str) -> Chamber:
        raise NotImplementedError