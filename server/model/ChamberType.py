from enum import StrEnum


class ChamberType(StrEnum):
    YOUTUBE = "youtube"
    REDDIT = "reddit"
    TWITTER = "twitter"

    @classmethod
    def has_value(cls, value):
        return any(member.value == value for member in cls)
