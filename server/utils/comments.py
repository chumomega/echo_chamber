from model.GeminiClient import POLITICAL_LABELS
from model.Comment import Comment
from model.LabelMagnitudes import PoliticalLabelMagnitudes

import logging
import operator

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def get_avg_label_magnitude(
    comments: list[Comment], avg_labels: set = set(POLITICAL_LABELS)
) -> PoliticalLabelMagnitudes:
    logger.info(f"Calculating avg label magnitude...")
    label_magnitude_sums = {}
    label_magnitude_counts = {}

    for comment in comments:
        label_magnitudes = comment.get_label_magnitudes()
        for label, magnitude in label_magnitudes.items():
            if (
                label not in avg_labels
                or magnitude is None
                or not type(magnitude) is int
            ):
                logger.error(f"Bad label magnitude received for: {comment.get_id()}")
                continue

            if label in label_magnitude_sums:
                label_magnitude_sums[label] += magnitude
                label_magnitude_counts[label] += 1
            else:
                label_magnitude_sums[label] = magnitude
                label_magnitude_counts[label] = 1

    avg_label_magnitudes = {}
    for label in label_magnitude_sums.keys():
        avg_label_magnitudes[label] = (
            label_magnitude_sums[label] / label_magnitude_counts[label]
        )
    return avg_label_magnitudes


def get_biased_chamber(chamber_label_magnitudes: PoliticalLabelMagnitudes) -> str:
    largest_label = max(chamber_label_magnitudes.items(), key=operator.itemgetter(1))[0]
    if largest_label != "moderate" and chamber_label_magnitudes[largest_label] > 4:
        return largest_label
    return None
