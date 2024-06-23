from basic_functions import to_markdown
import google.generativeai as genai
import os
from dotenv import load_dotenv
load_dotenv()

GOOGLE_API_KEY=os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

def answer_question(model, promt):
  response = model.generate_content(promt, stream=False) #stream=True fails
  to_markdown(response.text)
  return response.text

