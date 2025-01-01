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
            
            # Set custom headers to avoid potential blocking
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'application/rss+xml, application/xml, application/atom+xml, application/xhtml+xml, text/xml;q=0.9',
            }
            
            # Fetch the feed content
            response = requests.get(self.feed_url, headers=headers, allow_redirects=True, timeout=10)
            self.logger.info(f"Response status code: {response.status_code}")
            self.logger.info(f"Final URL after redirects: {response.url}")
            
            # Check response headers
            self.logger.debug(f"Response headers: {dict(response.headers)}")
            
            # Log response content type
            content_type = response.headers.get('content-type', 'unknown')
            self.logger.info(f"Content-Type: {content_type}")
            
            # Parse feed content
            feed = feedparser.parse(response.text)
            
            # Basic feed validation
            if not hasattr(feed, 'entries'):
                self.logger.error("No entries found in feed")
                self.logger.debug(f"Response content preview: {response.text[:500]}...")
                raise Exception("Invalid feed structure - no entries found")
            
            # Log feed information
            feed_title = feed.feed.get('title', 'Unknown') if hasattr(feed, 'feed') else 'No feed title'
            self.logger.info(f"Feed title: {feed_title}")
            self.logger.info(f"Number of entries: {len(feed.entries)}")
            
            if feed.entries:
                self.logger.info(f"Latest entry: {feed.entries[0].title}")
            
            return feed
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Request error: {str(e)}")
            self.logger.debug("Request exception details:", exc_info=True)
            raise Exception(f"Failed to fetch feed: {str(e)}")
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