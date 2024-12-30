# AI News Summarizer

Google DeepMindのブログ記事を自動で要約・翻訳するPythonツール

## 概要

このプロジェクトは、Google DeepMindの公式ブログのRSSフィードから最新の記事を取得し、Gemini APIを使用して要約と日本語翻訳を行います。

### 主な機能

- Google DeepMindのRSSフィードからの記事取得
- Gemini APIによる記事の要約
- 英語から日本語への翻訳
- Markdown形式での出力

## セットアップ

### 必要条件

- Python 3.9以上
- Gemini API キー

### インストール手順

1. リポジトリのクローン:
```bash
git clone https://github.com/Nappage/ai-news-summarizer.git
cd ai-news-summarizer
```

2. 仮想環境の作成と有効化:
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. 必要なパッケージのインストール:
```bash
pip install -r requirements.txt
```

4. 環境変数の設定:
- `.env.example` を `.env` にコピーし、Gemini APIキーを設定

### 使用方法

```bash
python -m src.main
```

## プロジェクト構成

```
ai_news_summarizer/
├── README.md
├── requirements.txt
├── .env
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── feed_handler.py
│   ├── content_processor.py
│   ├── ai_processor.py
│   └── markdown_generator.py
├── tests/
│   ├── __init__.py
│   └── test_feed_handler.py
└── output/
    └── .gitkeep
```

## ライセンス

MIT License

## 貢献について

1. このリポジトリをフォーク
2. 新しいブランチを作成 (`git checkout -b feature/awesome-feature`)
3. 変更をコミット (`git commit -am 'Add awesome feature'`)
4. ブランチをプッシュ (`git push origin feature/awesome-feature`)
5. Pull Requestを作成