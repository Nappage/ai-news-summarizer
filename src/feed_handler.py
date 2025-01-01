import feedparser
from bs4 import BeautifulSoup
import requests
from datetime import datetime
from .config import Config
import logging

class FeedHandler:
    def __init__(self):
        self.feed_url = Config.RSS_FEED_URL
        self.logger = logging.getLogger(__name__)
        
    def fetch_feed(self):
        """Fetch the RSS feed and return the parsed data"""
        try:
            # Configure session with headers
            session = requests.Session()
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            # Make the request with proper headers
            self.logger.info(f"Fetching feed from: {self.feed_url}")
            response = session.get(self.feed_url, headers=headers, allow_redirects=True)
            
            self.logger.info(f"Response status code: {response.status_code}")
            self.logger.info(f"Final URL: {response.url}")
            
            # Use feedparser to parse the response content
            feed = feedparser.parse(response.text)
            
            # Print debug information
            self.logger.debug(f"Feed version: {feed.get('version', 'unknown')}")
            self.logger.debug(f"Feed title: {feed.feed.get('title', 'unknown') if hasattr(feed, 'feed') else 'no feed info'}")
            
            # Validate feed structure
            if not hasattr(feed, 'entries'):
                self.logger.error("No entries found in feed")
                self.logger.debug(f"Response content preview: {response.text[:500]}...")
                raise Exception("Invalid feed structure - no entries found")
            
            self.logger.info(f"Successfully parsed feed with {len(feed.entries)} entries")
            return feed
            
        except Exception as e:
            self.logger.error(f"Error fetching feed: {str(e)}")
            self.logger.error(f"Feed URL: {self.feed_url}")
            raise Exception(f"Error fetching feed: {str(e)}")
    
    def get_new_entries(self, feed):
        """Extract new entries from the feed"""
        entries = []
        for entry in feed.entries:
            entry_data = {
                'title': entry.title,
                'link': entry.link,
                'published': entry.published if hasattr(entry, 'published') else None,
                'content': self._extract_content(entry)
            }
            entries.append(entry_data)
        return entries
    
    def _extract_content(self, entry):
        """Extract and clean the main content from an entry"""
        if hasattr(entry, 'content'):
            content = entry.content[0].value
        elif hasattr(entry, 'summary'):
            content = entry.summary
        else:
            content = ""
            
        soup = BeautifulSoup(content, 'html.parser')
        return soup.get_text(separator=' ').strip()