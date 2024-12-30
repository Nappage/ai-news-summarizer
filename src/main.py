import asyncio
import logging
from datetime import datetime
from .feed_handler import FeedHandler
from .ai_processor import AIProcessor
from .markdown_generator import MarkdownGenerator
from .config import Config

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def process_article(ai_processor, article_data):
    """Process a single article with AI summarization and translation"""
    try:
        # Generate English summary
        summary_en = await ai_processor.summarize(article_data['content'])
        
        # Translate title and summary to Japanese
        title_ja = await ai_processor.translate(article_data['title'])
        summary_ja = await ai_processor.translate(summary_en)
        
        return {
            **article_data,
            'title_ja': title_ja,
            'summary_en': summary_en,
            'summary_ja': summary_ja
        }
    except Exception as e:
        logger.error(f"Error processing article {article_data['title']}: {str(e)}")
        raise

async def main():
    try:
        logger.info("Starting RSS feed processing")
        
        # Initialize components
        feed_handler = FeedHandler()
        ai_processor = AIProcessor()
        md_generator = MarkdownGenerator()
        
        # Fetch and parse feed
        feed = feed_handler.fetch_feed()
        new_entries = feed_handler.get_new_entries(feed)
        
        logger.info(f"Found {len(new_entries)} new entries")
        
        # Process each article
        for entry in new_entries:
            try:
                # Process article with AI
                processed_article = await process_article(ai_processor, entry)
                
                # Generate and save markdown
                markdown_content = md_generator.generate_markdown(processed_article)
                filename = f"{datetime.now().strftime('%Y%m%d')}_{processed_article['title'][:30]}.md"
                filepath = md_generator.save_markdown(markdown_content, filename)
                
                logger.info(f"Successfully processed and saved article to {filepath}")
                
            except Exception as e:
                logger.error(f"Error processing entry: {str(e)}")
                continue
        
        logger.info("Finished processing all entries")
        
    except Exception as e:
        logger.error(f"Error in main process: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(main())