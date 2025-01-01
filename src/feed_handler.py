import feedparser
from bs4 import BeautifulSoup
import requests
from datetime import datetime
from .config import Config

class FeedHandler:
    def __init__(self):
        self.feed_url = Config.RSS_FEED_URL
        
    def fetch_feed(self):
        """Fetch the RSS feed and return the parsed data"""
        try:
            # Use requests to handle redirects
            response = requests.get(self.feed_url, allow_redirects=True)
            if response.status_code != 200:
                raise Exception(f"Failed to fetch feed. Status: {response.status_code}")
            
            # Parse the feed content
            feed = feedparser.parse(response.content)
            
            # Validate feed parsing
            if not hasattr(feed, 'entries'):
                raise Exception("Invalid feed format")
                
            return feed
            
        except Exception as e:
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