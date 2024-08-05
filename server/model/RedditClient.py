import praw.models
from model.Chamber import Chamber
from model.Comment import Comment
from model.ChamberType import ChamberType
from os import environ
import praw
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

MAX_OPINIONS = 5

# Do not create yourself. please use via context initializers :)
class RedditClient:
    def __init__(self) -> None:
        # Build the YouTube service object
        self.reddit_client = reddit = praw.Reddit(
            client_id=environ.get("REDDIT_ID"),
            client_secret=environ.get("REDDIT_SECRET"),
            user_agent="Echo Chamber v1.3 by /u/chumomega",
        )
        logger.info(f"Reddit instance initialized. read_only={reddit.read_only}")
        return

    def get_post_chamber(self, identifier: str) -> Chamber:
        submission = self.reddit_client.submission(id=identifier)

        if submission is None:
            return None

        return Chamber(
            id=identifier,
            chamber_type=ChamberType.REDDIT.value,
            title=submission.title,
            description=submission.selftext,
            author=submission.author.name,
        )

    def get_post_comments(
        self, identifier: str, num_comments: int = 5
    ) -> list[Comment]:
        submission = self.reddit_client.submission(id=identifier)

        comments = []

        submission.comment_sort = "top"
        for top_level_comment in submission.comments.list():
            comments.append(
                Comment(
                    id=top_level_comment.id,
                    text=top_level_comment.body,
                    author=top_level_comment.author.name,
                )
            )
            if len(comments) == num_comments:
                break

        return comments
