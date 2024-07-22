from model.ChamberType import ChamberType
from model.Comment import Comment
from context_initializers import get_firebase, get_youtube, get_gemini
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class ChamberMemberFactory:

    def __init__(self) -> None:
        return

    def get_chamber_members(self, identifier: str, chamber_type: str) -> list[Comment]:
        match chamber_type:
            case ChamberType.YOUTUBE.value:
                return self.__get_youtube_chamber_members(identifier)
            case _:
                raise Exception(f"Unsupported chamber type: {chamber_type}")

    def __get_youtube_chamber_members(self, identifier: str) -> list[Comment]:
        firebase_client = get_firebase()
        youtube_client = get_youtube()

        video_comments = firebase_client.get_chamber_members(
            identifier, ChamberType.YOUTUBE
        )
        if len(video_comments) > 0:
            logger.info(f"Retrieved cached video comments!")
            return video_comments

        video_comments = youtube_client.get_video_comments(identifier)

        gemini_client = get_gemini()
        comments_with_labels = gemini_client.get_labels_for_comments(video_comments)

        for comment in comments_with_labels:
            firebase_client.add_chamber_member(identifier, ChamberType.YOUTUBE, comment)

        return video_comments
