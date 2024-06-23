from typing import Union
from fastapi import FastAPI
from enum import Enum
import analyze_text
import google.generativeai as genai
import uvicorn

class ModelName(str, Enum):
    flash_15 = 'gemini-1.5-flash'
    pro_15 = 'gemini-1.5-pro'
    pro_vision = 'gemini-pro-vision'
    

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/api/answer_question")
def answer(prompt):
    model = genai.GenerativeModel(ModelName.flash_15)
    return analyze_text.answer_question(model, prompt)

if __name__ == "__main__":
    uvicorn.run(app, port=9000)