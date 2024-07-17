from model.GeminiClient import POLITICAL_LABELS
from model.Comment import Comment
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def get_avg_label_magnitude(comments: list[Comment], avg_labels: set = set(POLITICAL_LABELS)) -> dict:
    logger.info(f"Calculating avg label magnitude...")
    label_magnitude_sums = {}
    label_magnitude_counts = {}

    for comment in comments:
        label_magnitudes = comment.get_label_magnitudes()
        for label, magnitude in label_magnitudes.items():
            if label not in avg_labels or \
                magnitude is None or \
                not type(magnitude) is int:
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
        avg_label_magnitudes[label] = label_magnitude_sums[label] / label_magnitude_counts[label]
    return avg_label_magnitudes

def get_biased_chamber(chamber_label_magnitudes: dict) -> str:
    for label, magnitude in chamber_label_magnitudes.items():
        if magnitude >= 10/len(chamber_label_magnitudes):
            return label
    return None