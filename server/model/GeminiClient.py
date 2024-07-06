import google.generativeai as genai
from model.Comment import Comment
import json
import logging
from os import environ 

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

POLITICAL_LABELS = ["communist", "leftist", "liberal", "moderate", "conservative", "nationalist"]

class GeminiClient:

    FLASH_15_MODEL = 'gemini-1.5-flash'
    PRO_15_MODEL = 'gemini-1.5-pro'
    PRO_VISION_MODEL = 'gemini-pro-vision'
    

    def __init__(self) -> None:
        gemini_api_key = environ.get('GEMINI_API_KEY')
        genai.configure(api_key=gemini_api_key)
        self.client = genai.GenerativeModel(self.FLASH_15_MODEL)
        return

    def get_response_from_ai(self, prompt) -> str:
        response = self.client.generate_content(prompt, stream=False) #stream=True fails
        return response.text
    
    def get_labels_for_comments(self, comments: list[Comment]):
        political_labels_json = json.dumps(POLITICAL_LABELS, ensure_ascii=False)
        json_comments = self.get_json_comments_str(comments)
        prompt = """{{
            "text": "Given a list of comments with unique IDs, their text content, and their authors; analyze each comment to identify political leaning. Then provide json with the keys being comment ids and the values being json dict of the labels as keys and the magnitudes as values.", 
            "fixed_political_labels": {}, 
            "exampleOutput": { 
                "UgzDsRJK-wcq2BEBwBN4AaABAg": {
                    "communist": 3,
                    "leftist": 1,
                    "liberal": 2,
                    "moderate": 4,
                    "conservative": 1,
                    "nationalist": 4
                }, 
                "Ugw1xwhFJaVjxojdvUV4AaABAg": {...} 
            }, 
            "input": {} 
        }}""".format(political_labels_json, json_comments)
        # formatted_str = " {} | {}".format(political_labels_json, json_comments)
        logger.info(f"test formatted str: {prompt}")
        # return []
        response = self.get_response_from_ai(prompt)
        try:
            json_response = json.loads(response)
            logger.info("Successfully parsed Gemini labels for comments: {}".format(json_response))
        except Exception:
            logger.error("could not parse json!")
        return []
    
    def get_json_comments_str(self, comments: list[Comment]) -> str:
        output = {}
        for comment in comments:
            output[comment.id] = comment.get_json_body()
        return json.dumps(output, ensure_ascii=False)
