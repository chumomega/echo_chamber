from model.Chamber import Chamber
from model.Comment import Comment
from model.ChamberType import ChamberType
from os import environ
from googleapiclient.discovery import build
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

MAX_OPINIONS = 5


# Do not create yourself. please use via context initializers :)
class YoutubeClient:
    def __init__(self) -> None:
        # Build the YouTube service object
        youtube_data_api_key = environ.get("YOUTUBE_DATA_API_KEY")
        self.youtube_client = build("youtube", "v3", developerKey=youtube_data_api_key)
        return

    def get_video_chamber(self, identifier: str) -> Chamber:
        video_request = self.youtube_client.videos().list(
            part="snippet", id=identifier, maxResults=MAX_OPINIONS
        )
        video_response = video_request.execute()

        if (
            video_response is None
            or "items" not in video_response
            or len(video_response["items"]) == 0
        ):
            return None

        return Chamber(
            id=identifier,
            chamber_type=ChamberType.YOUTUBE.value,
            title=video_response["items"][0]["snippet"]["title"],
            description=video_response["items"][0]["snippet"]["description"],
            author=video_response["items"][0]["snippet"]["channelTitle"],
        )

    def get_video_comments(
        self, identifier: str, num_comments: int = None
    ) -> list[Comment]:
        comment_thread_request = self.youtube_client.commentThreads().list(
            part="snippet",
            videoId=identifier,
            maxResults=num_comments if num_comments is not None else MAX_OPINIONS,
            order="relevance",
            textFormat="plainText",
        )
        threads_response = comment_thread_request.execute()

        if "items" not in threads_response:
            return []

        comments = []
        for comment in threads_response["items"]:
            comments.append(
                Comment(
                    id=comment["snippet"]["topLevelComment"]["id"],
                    text=comment["snippet"]["topLevelComment"]["snippet"][
                        "textOriginal"
                    ],
                    author=comment["snippet"]["topLevelComment"]["snippet"][
                        "authorDisplayName"
                    ],
                )
            )
        return comments
