import google.generativeai as genai
from model.Comment import Comment
import json
import logging
from os import environ 
from string import Template

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
        political_labels_json = json.dumps(POLITICAL_LABELS)
        json_comments = self.get_json_comments_str(comments)
        prompt = """
            Put your data analyst/labeler hat on.

            Please provide me with a JSON response of your perception of the best label 
            fit with magnitude for each of the values in the "input" I provide. Please only give labels 
            from the "fixed_labels" I provide. Please reply only with JSON similar to the 
            following "example_output".

            "fixed_labels": $political_labels

            "example_output": { 
                "conservativeCommentId1": {
                    "communist": 1,
                    "leftist": 1,
                    "liberal": 1,
                    "moderate": 1,
                    "conservative": 9,
                    "nationalist": 4
                }, 
                "nonPoliticalCommentId1": {
                    "communist": 0,
                    "leftist": 0,
                    "liberal": 0,
                    "moderate": 0,
                    "conservative": 0,
                    "nationalist": 0
                }
            }

            "input": $comments 
        """
        prompt_template = Template(prompt)
        complete_prompt_request = prompt_template.substitute(political_labels=political_labels_json, comments=json_comments)
        # formatted_str = " {} | {}".format(political_labels_json, json_comments)
        logger.info(f"test formatted str: {str(complete_prompt_request)}")
        # return []
        response = self.get_response_from_ai(complete_prompt_request)
        try:
            json_response = json.loads(response)
            logger.info("Successfully parsed Gemini labels for comments: {}".format(json_response))
        except Exception:
            logger.error("could not parse json: {}".format(response))
        return []
    
    def get_json_comments_str(self, comments: list[Comment]) -> str:
        output = {}
        for comment in comments:
            output[comment.id] = comment.get_json_body()
        return json.dumps(output)
