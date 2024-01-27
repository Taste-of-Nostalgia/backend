from os import environ as env
from dotenv import load_dotenv, find_dotenv

from tasteofnostalgia import APP

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

if __name__ == "__main__":
    APP.run(host="0.0.0.0", port=env.get("PORT", 3010), debug=True)
