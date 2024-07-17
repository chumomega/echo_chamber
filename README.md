## About
In the digital age, we find ourselves in, information is easier to access than ever before. But this easy access to information has brought about a phenomenon called “echo chambers” that reduces the amount of good information available to users. According to the NIH, this occurs when “users’ opinions, political leanings, or beliefs about a topic are reinforced by repeated interactions with peers with similar tendencies and attitudes” (Gao 2023). Research has shown that this is more prevalent than you might think. Users in the study saw over 50% of content with similar views and less than 15% with differing views (Zadrozny 2023). 

We want to help democratize the internet for users to get good and balanced information, no matter the platform. This starts with first helping users identify when they are in an echo chamber. From there, we want to provide users with alternative viewpoints to help diminish the effects of the echo chamber.

More information on the tool's background can be found here: https://docs.google.com/document/d/16NS5V96opIYdOv_j8M8UlKoxTS1b0NyqWscIKGHP3q0/edit#heading=h.w5o1q08h92q6

## Getting Started for the first time
- Clone repo
- Create virtual env for dependencies while dev: `python3 -m venv .venv`
- Activate virtual env: `. .venv/bin/activate`
- Create `.env` file within the `./server/` directory. You will need several variables including gemini, youtube, and client origin

## Getting Started Frontend
- Locally you will need to load the unpacked extension. Follow these instructions https://developer.chrome.com/docs/extensions/get-started/tutorial/hello-world#load-unpacked
 - Please note that the code for it is nested in the `./client` directory


## Getting Started Backend
- Navigate to root directory for server `cd ./server`
- Make sure you've installed dependencies `pip install -r ./requirements.txt`
- Run `gunicorn main:app` from the root dir to run the server
- Go to `http://127.0.0.1:8000` to inspect

## Build and Deploy
- Run `gcloud builds submit --tag gcr.io/echo-chamber-427700/echochamber` to build container image
- Run `gcloud run deploy --image gcr.io/echo-chamber-427700/echochamber` to deploy the container you built

### Notes
- If you add a python dependency, please make sure to run `pip freeze > requirements.txt` so that dependency will get written to our requirements file



## References
- Gao, Y., Liu, F., & Gao, L. (2023, April 18). Echo chamber effects on short video platforms. Scientific reports. https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10111082/ 

- Zadrozny, B. (2023, July 27). Facebook opened its doors to researchers. what they found paints a complicated picture of social media and echo chambers. NBCNews.com. https://www.nbcnews.com/tech/tech-news/facebook-opened-doors-researchers-found-paints-complicated-picture-soc-rcna96536 

