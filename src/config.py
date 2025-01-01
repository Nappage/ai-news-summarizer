import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    # Use GOOGLE_API_KEY instead of GEMINI_API_KEY
    GEMINI_API_KEY = os.getenv('GOOGLE_API_KEY')
    # Use alternative feed URL
    RSS_FEED_URL = os.getenv('RSS_FEED_URL', "https://blog.research.google/feeds/posts/default")
    OUTPUT_DIR = os.getenv('OUTPUT_DIR', "output")
    MAX_SUMMARY_LENGTH = int(os.getenv('MAX_SUMMARY_LENGTH', "500"))
    RETRY_COUNT = 3
    RETRY_DELAY = 5  # seconds

    @classmethod
    def validate_config(cls):
        """Validate required configuration settings"""
        if not cls.GEMINI_API_KEY:
            raise ValueError("GOOGLE_API_KEY is not set in environment variables")
        
        # Ensure output directory exists
        os.makedirs(cls.OUTPUT_DIR, exist_ok=True)