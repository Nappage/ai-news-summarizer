import feedparser
from bs4 import BeautifulSoup
import requests
from datetime import datetime
from .config import Config
import logging
import time

class FeedHandler:
    def __init__(self):
        self.feed_url = Config.RSS_FEED_URL
        self.logger = logging.getLogger(__name__)
        
    def fetch_feed(self):
        """Fetch the RSS feed and return the parsed data"""
        try:
            self.logger.info(f"Attempting to fetch feed from {self.feed_url}")
            
            # Use feedparser directly first
            feed = feedparser.parse(self.feed_url)
            
            # Check if feed was successfully parsed
            if hasattr(feed, 'status'):
                self.logger.info(f"Feed status: {feed.status}")
            
            # Check if feed has entries
            if hasattr(feed, 'entries'):
                self.logger.info(f"Found {len(feed.entries)} entries")
                if feed.entries:
                    self.logger.info(f"First entry title: {feed.entries[0].title}")
            else:
                self.logger.warning("No entries found in feed")
            
            # If feedparser fails, try with requests as backup
            if not hasattr(feed, 'entries') or len(feed.entries) == 0:
                self.logger.info("Attempting to fetch with requests as backup")
                response = requests.get(
                    self.feed_url,
                    headers={
                        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                    },
                    timeout=10
                )
                feed = feedparser.parse(response.text)
            
            # Final validation
            if not hasattr(feed, 'entries'):
                raise Exception("Invalid feed structure - no entries found")
            
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
                try:
                    entry_data = {
                        'title': getattr(entry, 'title', 'No Title'),
                        'link': getattr(entry, 'link', ''),
                        'published': getattr(entry, 'published', None),
                        'content': self._extract_content(entry)
                    }
                    entries.append(entry_data)
                    self.logger.debug(f"Processed entry: {entry_data['title']}")
                except Exception as e:
                    self.logger.error(f"Error processing entry: {str(e)}")
                    continue
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
            
            if content:
                soup = BeautifulSoup(content, 'html.parser')
                return soup.get_text(separator=' ').strip()
            else:
                self.logger.warning(f"No content found for entry: {getattr(entry, 'title', 'unknown')}")
                return ""
                
        except Exception as e:
            self.logger.error(f"Error extracting content: {str(e)}")
            return ""