from typing import TypedDict

PoliticalLabelMagnitudes = TypedDict(
    "PoliticalLabelMagnitudes",
    {
        "communist": int,
        "leftist": int,
        "liberal": int,
        "moderate": int,
        "conservative": int,
        "nationalist": int,
    },
)
