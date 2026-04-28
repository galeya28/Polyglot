# Polyglot - Multilingual NLP Summarizer

Polyglot is a web-based application that summarizes text in multiple languages, with support for English, Hindi, and Telugu. It uses traditional NLP techniques and does not rely on AI APIs.

---

## Overview

The goal of this project is to reduce the time required to read long documents by automatically generating concise summaries. The system can process input from plain text, PDFs, and web articles, and also provides keyword extraction and translation.

---

## Features

| Feature                | Library Used           |
| ---------------------- | ---------------------- |
| Text Summarization     | sumy (LSA algorithm)   |
| Language Detection     | langdetect             |
| Keyword Extraction     | YAKE                   |
| Word Cloud             | wordcloud + matplotlib |
| PDF Extraction         | pdfplumber             |
| URL Article Extraction | newspaper3k            |
| Translation            | deep-translator        |

---

## How it works

The application follows a simple pipeline:

Input (text / PDF / URL)
→ Language detection
→ Summarization
→ Keyword extraction
→ (optional) translation
→ Output displayed in the UI

Summarization is done using the LSA algorithm (Latent Semantic Analysis), which selects the most relevant sentences from the input text.

---

## Tech Stack

Backend:

* Python
* Flask

NLP:

* sumy
* langdetect
* YAKE
* NLTK

Document Processing:

* pdfplumber
* newspaper3k

Visualization:

* wordcloud
* matplotlib

Translation:

* deep-translator

Frontend:

* HTML, CSS, JavaScript

---

## Setup

1. Install Python 3.9 or higher

2. Create a virtual environment

```bash
python -m venv venv
```

3. Activate the environment

```bash
# Mac/Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

4. Install dependencies

```bash
pip install -r requirements.txt
```

5. Download NLTK data (only once)

```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('punkt_tab')"
```

6. Run the application

```bash
python app.py
```

Open in browser:
[http://localhost:5000](http://localhost:5000)

---

## Application Tabs

* Text: paste text in English, Hindi (हिंदी), or Telugu (తెలుగు)
* URL: paste a news/article link to extract and summarize
* PDF: upload a document and summarize its contents
* Translate: translate text between supported languages

---

## Deployment (Railway)

1. Push the project to a GitHub repository

2. Go to Railway and create a new project

3. Select **“Deploy from GitHub repo”** and choose your repository

4. Railway will automatically detect the Python project

5. Set the start command:

```
gunicorn app:app
```

6. Add `gunicorn` to your `requirements.txt`:

```
gunicorn>=21.0.0
```

7. Deploy — Railway will generate a public URL for your app

---

## Limitations

* Uses extractive summarization (does not generate new sentences)
* Telugu summarization uses a fallback method due to limited support in sumy
* Scanned PDFs are not supported (no OCR)
* Some websites may block content extraction
* Translation requires an internet connection

---

## Future Improvements

* Add abstractive summarization using transformer models
* Evaluate summaries using ROUGE score
* Add OCR support for scanned PDFs
* Extend support to more Indian languages

---

If you want next, I can:

* add a **“Demo” section (very useful for recruiters)**
* or help you write a **short GitHub description + tags** so your project looks more polished when someone opens it
