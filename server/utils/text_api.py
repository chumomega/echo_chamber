import google.generativeai as genai

class TextAPI:

    FLASH_15_MODEL = 'gemini-1.5-flash'
    PRO_15_MODEL = 'gemini-1.5-pro'
    PRO_VISION_MODEL = 'gemini-pro-vision'

    def __init__(self, gemini_api_key) -> None:
        genai.configure(api_key=gemini_api_key)
        self.client = genai.GenerativeModel(self.FLASH_15_MODEL)
        return

    def get_response_from_ai(self, prompt) -> str:
        response = self.client.generate_content(prompt, stream=False) #stream=True fails
        return response.text