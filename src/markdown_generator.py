import os
from datetime import datetime
from .config import Config

class MarkdownGenerator:
    def __init__(self):
        self.output_dir = Config.OUTPUT_DIR
        os.makedirs(self.output_dir, exist_ok=True)
    
    def generate_markdown(self, article_data):
        """Generate markdown content from processed article data"""
        markdown_content = f"""# {article_data['title_ja']}

## 原文情報
- 公開日：{article_data['published']}
- 元記事URL：[{article_data['title']}]({article_data['link']})

## 要約（日本語）
{article_data['summary_ja']}

## 原文要約（英語）
{article_data['summary_en']}
"""
        return markdown_content
    
    def save_markdown(self, content, filename):
        """Save markdown content to file"""
        filepath = os.path.join(self.output_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return filepath