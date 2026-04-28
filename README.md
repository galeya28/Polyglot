# Polyglot — Multilingual NLP Summarizer

A full-featured multilingual text summarization system supporting **English**, **Hindi**, and **Telugu** with no AI APIs — pure NLP.

## Features

| Feature | Library |
|---|---|
| Text Summarization | `sumy` (LSA algorithm) |
| Language Detection | `langdetect` |
| Keyword Extraction | `YAKE` |
| Word Cloud | `wordcloud` + `matplotlib` |
| PDF Extraction | `pdfplumber` |
| URL Article Extraction | `newspaper3k` |
| Translation | `deep-translator` (Google Translate, free tier) |

## Setup

### 1. Install Python 3.9+

### 2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Download NLTK data (first time only)
```python
python -c "import nltk; nltk.download('punkt'); nltk.download('punkt_tab')"
```

### 5. Run
```bash
python app.py
```

Open **http://localhost:5000** in your browser.

## Tabs

- **Text** — Paste text in English, Hindi (हिंदी), or Telugu (తెలుగు)
- **URL** — Paste any article/news URL to auto-extract + summarize
- **PDF** — Upload a PDF and extract + summarize
- **Translate** — Standalone translator between 10 languages

## Deploying to Render

1. Push this folder to a GitHub repo
2. Create a new **Web Service** on [render.com](https://render.com)
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `gunicorn app:app`
5. Done — your app is live!

Add `gunicorn` to requirements.txt before deploying:
```
gunicorn>=21.0.0
```

## Notes

- Translation requires an internet connection (uses Google Translate free tier via `deep-translator`)
- All other features work fully offline
- Telugu summarization falls back to frequency-based extraction (sumy has limited Telugu support)
- For scanned PDFs, text extraction will return empty — use text-based PDFs only
