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
            
            # First try with requests to check the response
            response = requests.get(self.feed_url, allow_redirects=True)
            self.logger.info(f"HTTP Status Code: {response.status_code}")
            self.logger.info(f"Final URL: {response.url}")
            
            if response.status_code != 200:
                self.logger.error(f"HTTP error {response.status_code}")
                self.logger.debug(f"Response headers: {dict(response.headers)}")
                raise Exception(f"HTTP error {response.status_code}")
            
            # Parse the feed content
            feed = feedparser.parse(response.text)
            
            # Validate feed structure
            if not hasattr(feed, 'entries'):
                self.logger.error("No entries found in feed")
                self.logger.debug(f"Feed content preview: {response.text[:500]}...")
                raise Exception("Invalid feed structure - no entries found")
            
            if len(feed.entries) == 0:
                self.logger.warning("Feed contains no entries")
            else:
                self.logger.info(f"Successfully fetched {len(feed.entries)} entries")
                # Log first entry title for debugging
                self.logger.debug(f"First entry title: {feed.entries[0].title if feed.entries else 'N/A'}")
            
            return feed
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Request error: {str(e)}")
            raise Exception(f"Failed to fetch feed: {str(e)}")
        except Exception as e:
            self.logger.error(f"Error fetching feed: {str(e)}")
            raise
    
    def get_new_entries(self, feed):
        """Extract new entries from the feed"""
        try:
            entries = []
            for entry in feed.entries:
                entry_data = {
                    'title': entry.title,
                    'link': entry.link,
                    'published': entry.published if hasattr(entry, 'published') else None,
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
            if hasattr(entry, 'content'):
                content = entry.content[0].value
            elif hasattr(entry, 'summary'):
                content = entry.summary
            else:
                self.logger.warning(f"No content found for entry: {entry.title if hasattr(entry, 'title') else 'unknown'}")
                content = ""
                
            soup = BeautifulSoup(content, 'html.parser')
            return soup.get_text(separator=' ').strip()
        except Exception as e:
            self.logger.error(f"Error extracting content: {str(e)}")
            return ""