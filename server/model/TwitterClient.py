from model.Chamber import Chamber
from model.Comment import Comment
from model.ChamberType import ChamberType
from os import environ
import tweepy
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

MAX_OPINIONS = 5


# Do not create yourself. please use via context initializers :)
class TwitterClient:
    def __init__(self) -> None:
        self.twitter_client = tweepy.Client(
            bearer_token=environ.get("TWITTER_BEARER_TOKEN")
        )
        return

    def get_post_chamber(self, identifier: str) -> Chamber:
        tweet = self.twitter_client.get_tweet(
            id=identifier, tweet_fields=["text", "author_id"]
        ).data
        if tweet is None:
            return None

        user = self.twitter_client.get_user(
            id=tweet.author_id, user_fields=["name"]
        ).data

        if user is None:
            return None

        return Chamber(
            id=identifier,
            chamber_type=ChamberType.TWITTER.value,
            title=tweet.text,
            description="",
            author=user.name,
        )

    def get_post_comments(
        self, identifier: str, num_comments: int = 10
    ) -> list[Comment]:
        quote_tweets = self.twitter_client.get_quote_tweets(
            id=identifier, max_results=num_comments, tweet_fields=["text", "author_id"]
        ).data

        if quote_tweets is None:
            return None

        comments = []

        for tweet in quote_tweets:
            user = self.twitter_client.get_user(
                id=tweet.author_id, user_fields=["name"]
            ).data

            if user is None:
                continue

            comments.append(
                Comment(
                    id=str(tweet.id),
                    text=tweet.text,
                    author=user.name,
                )
            )

        return comments
