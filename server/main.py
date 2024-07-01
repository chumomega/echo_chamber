from flask import Flask
from os import environ
from controllers.getEchoChamberStatus import echo_chamber_info_routes

app = Flask(__name__)
app.register_blueprint(echo_chamber_info_routes)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(environ.get("PORT", 8080)))