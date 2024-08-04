import time
from model.LabelMagnitudes import PoliticalLabelMagnitudes
from model.ChamberType import ChamberType


class Chamber:

    def __init__(
        self,
        id: str,
        title: str,
        description: str,
        author: str,
        created_timestamp: float = time.time(),
        label_magnitudes: PoliticalLabelMagnitudes = None,
        chamber_status: str = None,
        chamber_reasoning: str = None,
        chamber_type: str = None,
    ) -> None:

        self.id = id
        self.chamber_type = chamber_type
        self.title = title
        self.description = description
        self.author = author
        self.created_timestamp = created_timestamp
        self.label_magnitudes = label_magnitudes
        self.chamber_status = chamber_status
        self.chamber_reasoning = chamber_reasoning
        return

    def get_id(self) -> str:
        return self.id

    def get_chamber_status(self) -> str:
        return self.chamber_status

    def get_chamber_reasoning(self) -> str:
        return self.chamber_reasoning

    def get_label_magnitudes(self) -> PoliticalLabelMagnitudes:
        return self.label_magnitudes

    def get_json_body(self) -> dict:
        body = {
            "created_timestamp": self.created_timestamp,
            "description": self.description,
            "title": self.title,
            "author": self.author,
        }

        if self.label_magnitudes is not None:
            body["label_magnitudes"] = self.label_magnitudes

        if self.chamber_status is not None:
            body["chamber_status"] = self.chamber_status

        if self.chamber_status is not None:
            body["chamber_reasoning"] = self.chamber_reasoning

        return body

    def get_json_body_for_tags(self) -> dict:
        return {
            "description": self.description,
            "title": self.title,
            "author": self.author,
            "chamber_reasoning": self.chamber_reasoning,
        }

    def get_json_body_for_explanation(self) -> dict:
        return {
            "description": self.description,
            "title": self.title,
            "author": self.author,
            "label_magnitudes": self.label_magnitudes,
            "chamber_status": self.chamber_status,
        }

    def get_serialized(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "label_magnitudes": self.label_magnitudes,
            "chamber_status": self.chamber_status,
            "chamber_reasoning": self.chamber_reasoning,
            "url": self.__get_url_for_chamber(),
        }

    def __get_url_for_chamber(self) -> str:
        match self.chamber_type:
            case ChamberType.YOUTUBE:
                return f"https://www.youtube.com/watch?v={self.id}"
            case _:
                raise Exception(f"Unsupported chamber type: {self.chamber_type}")

    def __str__(self):
        return f"Chamber(id='{self.id}', type='{self.chamber_type}', title='{self.title}', description='{self.description}', \
            author='{self.author}', created_timestamp='{self.created_timestamp}', \
                label_magnitudes='{self.label_magnitudes}', chamber_status='{self.chamber_status}', \
                chamber_reasoning='{self.chamber_reasoning}')"
