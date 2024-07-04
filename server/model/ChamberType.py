from enum import Enum

class ChamberType(Enum):
    YOUTUBE = 1

    @classmethod
    def has_value(cls, value):
        return any(member.value == value for member in cls)
    