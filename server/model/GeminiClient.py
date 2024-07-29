import google.generativeai as genai
from model.Comment import Comment
from model.Chamber import Chamber
import json
import logging
from os import environ
from string import Template
import re

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

POLITICAL_LABELS = [
    "communist",
    "leftist",
    "liberal",
    "moderate",
    "conservative",
    "nationalist",
]


class GeminiClient:

    FLASH_15_MODEL = "gemini-1.5-flash"
    PRO_15_MODEL = "gemini-1.5-pro"
    PRO_VISION_MODEL = "gemini-pro-vision"

    def __init__(self) -> None:
        gemini_api_key = environ.get("GEMINI_API_KEY")
        genai.configure(api_key=gemini_api_key)
        self.client = genai.GenerativeModel(self.FLASH_15_MODEL)
        return

    def get_response_from_ai(self, prompt) -> str:
        try:
            response = self.client.generate_content(prompt, stream=False)
            return response.text
        except Exception as e:
            logger.error("Error getting response from Gemini", e)
            safety_ratings_logs = ""
            for candidate in response.candidates:
                safety_ratings_logs += f"{candidate.safety_ratings}\n"
            logger.error(safety_ratings_logs)
            raise Exception

    def get_labels_for_comments(self, comments: list[Comment]) -> list[Comment]:
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
        complete_prompt_request = prompt_template.substitute(
            political_labels=political_labels_json, comments=json_comments
        )
        response = self.get_response_from_ai(complete_prompt_request)

        comment_labels = []
        # Parse Json Response from Gemini
        try:
            json_begin_index = response.find("{")
            json_end_index = response.rfind("}")
            json_str = response[json_begin_index - 1 : json_end_index + 1]
            comment_labels = json.loads(json_str)
        except Exception:
            logger.error("could not parse json: {}".format(response))

        for comment in comments:
            if comment.get_id() in comment_labels:
                comment.set_label_magnitudes(comment_labels[comment.get_id()])
        return comments

    def get_reasoning_for_comments(
        self, chamber: Chamber, comments: list[Comment]
    ) -> str:
        prompt = """
            Put your clear communicator hat on.

            I'll be giving you data on a potential echo chamber in the "potential_echo_chamber" value 
            with things like the status I calculated and the magnitude of various labels.
            Please analyze it and the "chamber_members" to generate an explanation on why said chamber 
            is or is not a chamber.
            
            Make sure to provide the reasoning for the explanation in a JSON format like: {"reasoning": "Insert Reasoning here"}

            Guidelines:
            - If it is an echo chamber, use the magnitude for it in your explanation
            - Don't say anything that could be assessed as HARASSMENT, HATE_SPEECH, SEXUALLY_EXPLICIT, or DANGEROUS_CONTENT
            - Use double quotes for JSON. This is very important
            - Explain at 10th grade reading level or below.
            - Use 80 words or less
            - Use snippets of examples in your explanation
            - Don't explicitly say "potential_echo_chamber" or "chamber_members" in your explanation

            "potential_echo_chamber": $potential_echo_chamber
            "chamber_members": $chamber_members
        """
        prompt_template = Template(prompt)
        complete_prompt_request = prompt_template.substitute(
            chamber_members=self.get_json_comments_str(comments),
            potential_echo_chamber=chamber.get_json_body_for_explanation(),
        )
        response = self.get_response_from_ai(complete_prompt_request)
        # Parse Json Response from Gemini
        try:
            json_begin_index = response.find("{")
            json_end_index = response.rfind("}")
            json_str = response[json_begin_index - 1 : json_end_index + 1]
            j = json.loads(json_str)
            return j["reasoning"]
        except Exception as e:
            logger.error("could not parse json: {}".format(response), e)

    def get_tags_for_chamber(
        self, chamber: Chamber, comments: list[Comment]
    ) -> list[Comment]:
        content_json = chamber.get_json_body_for_tags()
        content_comments_json = self.get_json_comments_str_for_tags(comments)
        prompt = """
            Put your data analyst/labeler hat on.

            I'm going to give you a piece of content, "content", and some commentary on it, "content_comments".
            Please provide me with a list of labels or tags that best describe it. An example style of output that
            I expect is below as "example_output"

            Tagging Guidelines:
            - Please do not provide more than 7 tags
            - Please make sure every tag is lowercase
            - Please make sure every tag is a single word
            - Please avoid punctiation and capitalization
            - Please exclude common words like "the" or "and"
            - Please prioritize descriptive keywords over proper nouns
            - Please represent compound words as a signle word
            - Please represent numbers in tags as digits insead of words ie - 2 instead of two
            - Please provide response as comma delimited list surrunded by square brackets

            "content": $content
            "content_comments": $content_comments
            "example_output": [politics,2024,election,digitalmedia,comedy]
        """
        logger.info(f"Retrieving tags from Gemini...")
        prompt_template = Template(prompt)
        complete_prompt_request = prompt_template.substitute(
            content=content_json, content_comments=content_comments_json
        )
        response = self.get_response_from_ai(complete_prompt_request)
        tags = []
        # Parse Json Response from Gemini
        try:
            json_begin_index = response.find("[")
            json_end_index = response.rfind("]")
            list_str = response[json_begin_index + 1 : json_end_index]
            tags = list_str.split(",")
        except Exception:
            logger.error("could not parse tags list: {}".format(response))

        return [tag.strip() for tag in tags]

    def get_json_comments_str(self, comments: list[Comment]) -> str:
        output = {}
        for comment in comments:
            output[comment.id] = comment.get_json_body()
        return json.dumps(output)

    def get_json_comments_str_for_tags(self, comments: list[Comment]) -> str:
        output = {}
        for comment in comments:
            output[comment.id] = comment.get_json_body_for_tags()
        return json.dumps(output)
