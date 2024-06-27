from flask import Flask, request
import google.generativeai as genai


app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/getEchoChamberStatus")
def get_echo_chamber_status():
    identifier = request.args.get('identifier')
    chamber_type = request.args.get('chamber_type')
    validateInput(identifier, chamber_type)

    return {
        "isChamber": True,
        "chamberLabel": "right-wing",
        "chamberMagnitude": 9,
        "chamberReasoning": "Because I said so"
    }

def validateInput(identifier, chamber_type) -> None:
    if identifier is None or chamber_type is None:
        raise Exception(f"Empty input! identifier: {identifier} || chamber_type: {chamber_type}")
    else:
        return