import os

from dotenv import load_dotenv


load_dotenv()

api_secret = os.environ.get("api_secret")
api_key = os.environ.get("api_key")
request_interval_seconds = 60
changes_interval_minutes = 60
percent_change = 1
