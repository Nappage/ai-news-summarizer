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
            self.logger.info(f"Attempting to fetch feed from {self.feed_url}")
            
            # Try to fetch the feed content directly with requests first
            response = requests.get(self.feed_url)
            self.logger.info(f"HTTP Status: {response.status_code}")
            self.logger.info(f"Content type: {response.headers.get('content-type', 'unknown')}")
            
            if response.status_code == 200:
                feed = feedparser.parse(response.content)
            else:
                self.logger.warning(f"Direct request failed with status {response.status_code}, trying feedparser")
                feed = feedparser.parse(self.feed_url)
            
            # Validate feed structure
            if not hasattr(feed, 'entries'):
                self.logger.error("No entries found in feed")
                self.logger.debug(f"Feed content preview: {response.text[:500]}...")
                raise Exception("Invalid feed structure - no entries found")
            
            if feed.entries:
                self.logger.info(f"Successfully fetched {len(feed.entries)} entries")
                self.logger.info(f"First entry title: {feed.entries[0].title}")
            else:
                self.logger.warning("Feed contains no entries")
            
            return feed
            
        except Exception as e:
            self.logger.error(f"Error fetching feed: {str(e)}")
            self.logger.debug("Exception details:", exc_info=True)
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