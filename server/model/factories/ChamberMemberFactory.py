import praw.models
from model.ChamberType import ChamberType
from model.Comment import Comment
import praw
from context_initializers import get_firebase, get_youtube, get_gemini, get_reddit
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
            case ChamberType.REDDIT.value:
                return self.__get_reddit_chamber_members(identifier)
            case ChamberType.X.value:
                return self.__get_x_chamber_members(identifier)
            case _:
                raise Exception(f"Unsupported chamber type: {chamber_type}")

    def __get_youtube_chamber_members(self, identifier: str) -> list[Comment]:
        firebase_client = get_firebase()
        youtube_client = get_youtube()

        video_comments = firebase_client.get_chamber_members(
            identifier, ChamberType.YOUTUBE
        )
        if len(video_comments) > 0:
            return video_comments

        video_comments = youtube_client.get_video_comments(identifier)

        gemini_client = get_gemini()
        comments_with_labels = gemini_client.get_labels_for_comments(video_comments)

        for comment in comments_with_labels:
            firebase_client.add_chamber_member(identifier, ChamberType.YOUTUBE, comment)

        return comments_with_labels

    def __get_reddit_chamber_members(self, identifier: str) -> list[Comment]:
        firebase_client = get_firebase()
        reddit_client = get_reddit()

        comments = firebase_client.get_chamber_members(identifier, ChamberType.REDDIT)
        if len(comments) > 0:
            return comments

        comments = reddit_client.get_post_comments(
            identifier=identifier, num_comments=5
        )

        gemini_client = get_gemini()
        comments_with_labels = gemini_client.get_labels_for_comments(comments=comments)

        for comment in comments_with_labels:
            firebase_client.add_chamber_member(identifier, ChamberType.REDDIT, comment)

        return comments_with_labels

    def __get_x_chamber_members(self, identifier: str) -> list[Comment]:
        raise NotImplementedError
