from flask import Flask
from controllers.getEchoChamberStatus import echo_chamber_info_routes
import firebase_admin
import logging
from dotenv import load_dotenv

DOT_ENV_FILE = "./.env"
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

load_dotenv(
    dotenv_path=DOT_ENV_FILE, verbose=True
)  # this loads in the environment variables from the .env file for the process
logger.info("Loaded environemnt variables from path: {}".format(DOT_ENV_FILE))

app = Flask(__name__)
# TODO - add credentials. by default it finds credentials if you use cloud run to host
firebase_admin.initialize_app(
    options={"databaseURL": "https://echo-chamber-427700-default-rtdb.firebaseio.com/"}
)
app.register_blueprint(echo_chamber_info_routes)

# Gunicorn is used to run server
