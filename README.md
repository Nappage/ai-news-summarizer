# AI News Summarizer

Google DeepMindのブログ記事を自動で要約・翻訳するPythonツール

## セキュリティに関する重要な注意

⚠️ **APIキーの取り扱いについて**
- APIキーは環境変数`GOOGLE_API_KEY`として設定してください
- `.env`ファイルは絶対にGitHubにコミットしないでください
- Google Colabを使用する場合は、Secretsマネージャーを使用してください

## セットアップ

### ローカル環境

1. リポジトリのクローン:
```bash
git clone https://github.com/Nappage/ai-news-summarizer.git
cd ai-news-summarizer
```

2. 環境変数の設定:
```bash
cp .env.example .env
# .envファイルを編集してGOOGLE_API_KEYを設定
```

3. 仮想環境のセットアップ:
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Google Colab環境

1. Secretsの設定:
   - Colab メニューから「ファイル」→「シークレットを管理」を選択
   - 名前: `GOOGLE_API_KEY`を追加
   - APIキーを値として設定

2. リポジトリのクローンとセットアップ:
```python
!git clone https://github.com/Nappage/ai-news-summarizer.git
%cd ai-news-summarizer
!pip install -r requirements.txt
```

## 使用方法

```python
# ローカル環境
python -m src.main

# Google Colab
from src.main import main
await main()
```

## 出力ファイル

- 生成されたファイルは`output/`ディレクトリに保存されます
- このディレクトリは`.gitignore`に含まれており、生成ファイルはGitHubにコミットされません

## セキュリティポリシー

詳細なセキュリティガイドラインについては、[SECURITY.md](SECURITY.md)を参照してください。