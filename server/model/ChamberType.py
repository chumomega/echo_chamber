from enum import StrEnum


class ChamberType(StrEnum):
    YOUTUBE = "youtube"
    REDDIT = "reddit"
    X = "x"

    @classmethod
    def has_value(cls, value):
        return any(member.value == value for member in cls)
