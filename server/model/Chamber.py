import time
from model.LabelMagnitudes import PoliticalLabelMagnitudes


class Chamber:

    def __init__(
        self,
        id: str,
        title: str,
        description: str,
        author: str,
        created_timestamp: float = time.time(),
        label_magnitudes: PoliticalLabelMagnitudes = None,
    ) -> None:

        self.id = id
        self.title = title
        self.description = description
        self.author = author
        self.created_timestamp = created_timestamp
        self.label_magnitudes = label_magnitudes
        return

    def get_id(self) -> str:
        return self.id

    def get_json_body(self) -> dict:
        body = {
            "created_timestamp": self.created_timestamp,
            "description": self.description,
            "title": self.title,
            "author": self.author,
        }

        if self.label_magnitudes is not None:
            body["label_magnitudes"] = self.label_magnitudes

        return body

    def __str__(self):
        return f"Chamber(id='{self.id}', title='{self.title}', description='{self.description}', \
            author='{self.author}', created_timestamp='{self.created_timestamp}', \
                label_magnitudes='{self.label_magnitudes}')"
