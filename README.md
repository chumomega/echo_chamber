## About
This is the repo for the client and server code for the echo chamber extension. More information on the tool's background can be found here: https://docs.google.com/document/d/16NS5V96opIYdOv_j8M8UlKoxTS1b0NyqWscIKGHP3q0/edit#heading=h.w5o1q08h92q6

## Getting Started for the first time
- Clone repo
- Create virtual env for dependencies while dev: `python3 -m venv .venv`
- Activate virtual env: `. .venv/bin/activate`
- 

## Getting Started Frontend
- Locally you will need to load the unpacked extension. Follow these instructions https://developer.chrome.com/docs/extensions/get-started/tutorial/hello-world#load-unpacked
 - Please note that the code for it is nested in the `./client` directory


## Getting Started Backend
- Run `flask --app server/controllers/getEchoChamberStatus run` from the root directory to run the server
- Go to `http://127.0.0.1:5000` to inspect 
