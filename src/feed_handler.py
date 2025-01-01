import feedparser
from bs4 import BeautifulSoup
import requests
from datetime import datetime
from .config import Config
import logging
import random

class FeedHandler:
    def __init__(self):
        self.feed_url = Config.RSS_FEED_URL
        self.logger = logging.getLogger(__name__)
        # List of common user agents
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15'
        ]
        
    def fetch_feed(self):
        """Fetch the RSS feed and return the parsed data"""
        try:
            self.logger.info(f"Attempting to fetch feed from {self.feed_url}")
            
            headers = {
                'User-Agent': random.choice(self.user_agents),
                'Accept': 'application/rss+xml, application/xml, application/atom+xml, text/xml;q=0.9',
                'Accept-Language': 'en-US,en;q=0.5',
            }
            
            # First try with requests
            response = requests.get(self.feed_url, headers=headers, timeout=10)
            self.logger.info(f"HTTP Status: {response.status_code}")
            
            if response.status_code == 200:
                self.logger.info("Successfully fetched feed with requests")
                self.logger.debug(f"Response headers: {dict(response.headers)}")
                feed = feedparser.parse(response.content)
            else:
                self.logger.warning(f"HTTP request failed with status {response.status_code}")
                raise Exception(f"Failed to fetch feed: HTTP {response.status_code}")
            
            # Validate feed
            if not hasattr(feed, 'entries'):
                self.logger.error("Feed validation failed: no entries found")
                raise Exception("Invalid feed structure - no entries found")
            
            self.logger.info(f"Successfully parsed feed with {len(feed.entries)} entries")
            if feed.entries:
                self.logger.info(f"Latest entry: {feed.entries[0].title}")
            
            return feed
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Request error: {str(e)}")
            raise
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