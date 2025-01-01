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
            
            # Parse feed with feedparser
            feed = feedparser.parse(self.feed_url)
            
            self.logger.debug(f"Feed version: {getattr(feed, 'version', 'unknown')}")
            self.logger.debug(f"Feed type: {getattr(feed, 'feed_type', 'unknown')}")
            
            # Validate feed
            if not hasattr(feed, 'entries'):
                raise Exception("Invalid feed structure - no entries found")
            
            self.logger.info(f"Successfully fetched {len(feed.entries)} entries")
            if feed.entries:
                self.logger.debug(f"First entry title: {feed.entries[0].title}")
            
            return feed
            
        except Exception as e:
            self.logger.error(f"Error fetching feed: {str(e)}")
            raise
    
    def get_new_entries(self, feed):
        """Extract new entries from the feed"""
        try:
            entries = []
            for entry in feed.entries:
                entry_data = {
                    'title': getattr(entry, 'title', 'No Title'),
                    'link': getattr(entry, 'link', ''),
                    'published': getattr(entry, 'published', None),
                    'content': self._extract_content(entry)
                }
                entries.append(entry_data)
                self.logger.debug(f"Processed entry: {entry_data['title']}")
            return entries
        except Exception as e:
            self.logger.error(f"Error processing entries: {str(e)}")
            raise
    
    def _extract_content(self, entry):
        """Extract and clean the main content from an entry"""
        try:
            content = ""
            if hasattr(entry, 'content'):
                content = entry.content[0].value
            elif hasattr(entry, 'summary'):
                content = entry.summary
            elif hasattr(entry, 'description'):
                content = entry.description
            
            if not content:
                return ""
                
            soup = BeautifulSoup(content, 'html.parser')
            return soup.get_text(separator=' ').strip()
                
        except Exception as e:
            self.logger.error(f"Error extracting content: {str(e)}")
            return ""