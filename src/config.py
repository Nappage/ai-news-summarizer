import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    RSS_FEED_URL = "https://deepmind.google/blog/feed/basic/"
    OUTPUT_DIR = "output"
    MAX_SUMMARY_LENGTH = 500
    RETRY_COUNT = 3
    RETRY_DELAY = 5  # seconds