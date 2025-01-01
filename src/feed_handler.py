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
            # First try to get the final URL after redirects
            session = requests.Session()
            response = session.get(self.feed_url, allow_redirects=True)
            final_url = response.url
            
            self.logger.info(f"Initial URL: {self.feed_url}")
            self.logger.info(f"Final URL after redirects: {final_url}")
            self.logger.info(f"Response status code: {response.status_code}")
            
            # Use feedparser directly with the content
            feed = feedparser.parse(response.text)
            
            # Basic validation of the feed
            if not hasattr(feed, 'entries'):
                self.logger.error("Feed parsing failed: no entries found")
                self.logger.debug(f"Feed content: {response.text[:500]}...")
                raise Exception("Invalid feed format - no entries found")
            
            self.logger.info(f"Successfully parsed feed with {len(feed.entries)} entries")
            return feed
            
        except Exception as e:
            self.logger.error(f"Error fetching feed: {str(e)}")
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