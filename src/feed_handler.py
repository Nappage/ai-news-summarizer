import feedparser
from bs4 import BeautifulSoup
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
            self.logger.info(f"Fetching feed from: {self.feed_url}")
            feed = feedparser.parse(self.feed_url)
            
            if hasattr(feed, 'bozo_exception'):
                self.logger.error(f"Feed parsing error: {feed.bozo_exception}")
            
            if hasattr(feed, 'entries'):
                self.logger.info(f"Found {len(feed.entries)} entries")
                if feed.entries:
                    self.logger.info(f"Latest entry: {feed.entries[0].title}")
                return feed
            else:
                raise Exception("No entries found in feed")
                
        except Exception as e:
            self.logger.error(f"Error fetching feed: {str(e)}")
            raise
    
    def get_new_entries(self, feed):
        """Extract new entries from the feed"""
        try:
            entries = []
            for entry in feed.entries:
                content = self._extract_content(entry)
                if content:  # Only add entries with content
                    entry_data = {
                        'title': getattr(entry, 'title', 'No Title'),
                        'link': getattr(entry, 'link', ''),
                        'published': getattr(entry, 'published', None),
                        'content': content
                    }
                    entries.append(entry_data)
                    self.logger.debug(f"Added entry: {entry_data['title']}")
            
            if not entries:
                self.logger.warning("No valid entries found")
            
            return entries
            
        except Exception as e:
            self.logger.error(f"Error processing entries: {str(e)}")
            raise
    
    def _extract_content(self, entry):
        """Extract and clean the main content from an entry"""
        try:
            content = ""
            # Try different content fields in order of preference
            if hasattr(entry, 'content'):
                content = entry.content[0].value
            elif hasattr(entry, 'summary'):
                content = entry.summary
            elif hasattr(entry, 'description'):
                content = entry.description
            
            if content:
                soup = BeautifulSoup(content, 'html.parser')
                return soup.get_text(separator=' ').strip()
            return ""
                
        except Exception as e:
            self.logger.error(f"Error extracting content: {str(e)}")
            return ""