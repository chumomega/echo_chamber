from enum import Enum


class ChamberType(Enum):
    YOUTUBE = "youtube"

    @classmethod
    def has_value(cls, value):
        return any(member.value == value for member in cls)
