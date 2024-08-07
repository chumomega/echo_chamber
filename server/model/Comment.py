import time
from model.LabelMagnitudes import PoliticalLabelMagnitudes


class Comment:
    id = None
    text = None
    author = None
    created_timestamp = None
    label_magnitudes = None

    def __init__(
        self,
        id: str,
        text: str,
        author: str,
        created_timestamp: float = time.time(),
        label_magnitudes: PoliticalLabelMagnitudes = None,
    ) -> None:

        self.id = id
        self.text = text
        self.author = author
        self.created_timestamp = created_timestamp
        self.label_magnitudes = label_magnitudes
        return

    def get_id(self) -> str:
        return self.id

    def set_label_magnitudes(self, label_magnitudes: PoliticalLabelMagnitudes) -> None:
        self.label_magnitudes = label_magnitudes

    def get_label_magnitudes(self) -> PoliticalLabelMagnitudes:
        return self.label_magnitudes

    def get_json_body(self) -> dict:
        body = {
            "created_timestamp": self.created_timestamp,
            "text": self.text,
            "author": self.author,
        }

        if self.label_magnitudes is not None:
            body["label_magnitudes"] = self.label_magnitudes

        return body

    def get_json_body_for_tags(self) -> dict:
        return {
            "text": self.text,
            "author": self.author,
        }

    def __repr__(self):
        return f"Comment(id='{self.id}', text='{self.text}', author='{self.author}', \
            created_timestamp='{self.created_timestamp}', label_magnitudes='{self.label_magnitudes}')"

    def to_json(self):
        return {"text": self.text, "author": self.author}
