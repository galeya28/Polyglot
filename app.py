from flask import Flask, render_template, request, jsonify
import os, io, re
from collections import Counter

try:
    from langdetect import detect as _detect_lang
    def detect_language(text):
        try:
            code = _detect_lang(text)
            names = {"en":"English","hi":"Hindi","te":"Telugu","es":"Spanish",
                     "fr":"French","de":"German","it":"Italian","pt":"Portuguese",
                     "ar":"Arabic","zh-cn":"Chinese","ja":"Japanese","ko":"Korean"}
            return code, names.get(code, code.upper())
        except:
            return "en", "English"
except ImportError:
    def detect_language(text):
        telugu = sum(1 for c in text if '\u0C00' <= c <= '\u0C7F')
        hindi  = sum(1 for c in text if '\u0900' <= c <= '\u097F')
        if telugu > 5:  return "te", "Telugu"
        if hindi  > 5:  return "hi", "Hindi"
        return "en", "English"

try:
    import yake
    def extract_keywords(text, lang="en", n=15):
        kw_extractor = yake.KeywordExtractor(lan=lang, n=2, top=n)
        kws = kw_extractor.extract_keywords(text)
        if not kws: return []
        max_s = max(s for _,s in kws) or 1
        return [{"word": kw, "score": round((1 - score/max_s)*100, 1)} for kw, score in kws]
except ImportError:
    def extract_keywords(text, lang="en", n=15):
        stop = set("the a an is are was were be been being have has had do does did will would could should may might shall to of in on at for with by from up about into than through during before after above below between each while this that these those i me my myself we our you your he she it its they them their what which who whom when where why how all both each few more most other some such no nor not only own same so than too very just".split())
        words = re.findall(r'\b[a-zA-Z\u0900-\u097F\u0C00-\u0C7F]{3,}\b', text.lower())
        freq = Counter(w for w in words if w not in stop)
        top = freq.most_common(n)
        if not top: return []
        max_f = top[0][1]
        return [{"word": w, "score": round(f/max_f*100,1)} for w,f in top]

try:
    from sumy.parsers.plaintext import PlaintextParser
    from sumy.nlp.tokenizers import Tokenizer
    from sumy.summarizers.lsa import LsaSummarizer
    from sumy.nlp.stemmers import Stemmer
    from sumy.utils import get_stop_words
    import nltk
    try: nltk.data.find('tokenizers/punkt')
    except:
        try: nltk.download('punkt', quiet=True)
        except: pass
    try: nltk.data.find('tokenizers/punkt_tab')
    except:
        try: nltk.download('punkt_tab', quiet=True)
        except: pass

    def summarize_text(text, lang_code="en", num_sentences=5):
        lang_map = {"en":"english","hi":"english","te":"english",
                    "es":"spanish","fr":"french","de":"german","it":"italian","pt":"portuguese"}
        lang = lang_map.get(lang_code, "english")
        try:
            parser = PlaintextParser.from_string(text, Tokenizer(lang))
            stemmer = Stemmer(lang)
            summarizer = LsaSummarizer(stemmer)
            summarizer.stop_words = get_stop_words(lang)
            sentences = summarizer(parser.document, num_sentences)
            result = " ".join(str(s) for s in sentences)
            return result if result.strip() else _fallback_summary(text, num_sentences)
        except Exception:
            return _fallback_summary(text, num_sentences)
except ImportError:
    def summarize_text(text, lang_code="en", num_sentences=5):
        return _fallback_summary(text, num_sentences)

def _fallback_summary(text, n=5):
    stop = set("the a an is are was were be been have has had do does did will would could should to of in on at for with by from i me we you he she it they".split())
    sentences = re.split(r'(?<=[.!?।])\s+', text.strip())
    sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
    if not sentences: return text[:500]
    words = re.findall(r'\b\w+\b', text.lower())
    freq = Counter(w for w in words if w not in stop)
    def score(s):
        ws = re.findall(r'\b\w+\b', s.lower())
        return sum(freq.get(w,0) for w in ws) / (len(ws) or 1)
    ranked = sorted(enumerate(sentences), key=lambda x: score(x[1]), reverse=True)
    top_idx = sorted([i for i,_ in ranked[:n]])
    return " ".join(sentences[i] for i in top_idx)

try:
    import pdfplumber
    def extract_pdf(file_bytes):
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            return "\n".join(p.extract_text() or "" for p in pdf.pages)
except ImportError:
    def extract_pdf(file_bytes):
        return "[PDF extraction unavailable. Install pdfplumber.]"

try:
    from newspaper import Article
    def extract_url(url):
        a = Article(url)
        a.download(); a.parse()
        return a.text, a.title
except ImportError:
    def extract_url(url):
        try:
            import urllib.request
            with urllib.request.urlopen(url, timeout=10) as r:
                html = r.read().decode('utf-8','ignore')
            text = re.sub(r'<[^>]+>','',html)
            text = re.sub(r'\s+',' ',text).strip()
            return text[:8000], "Article"
        except Exception as e:
            return f"[Could not fetch URL: {e}]", "Error"

try:
    from deep_translator import GoogleTranslator
    def translate_text(text, src, tgt):
        chunks = [text[i:i+4500] for i in range(0, len(text), 4500)]
        return " ".join(GoogleTranslator(source=src, target=tgt).translate(c) for c in chunks)
except ImportError:
    def translate_text(text, src, tgt):
        return "[Translation unavailable. Install deep-translator: pip install deep-translator]"

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/summarize', methods=['POST'])
def api_summarize():
    data = request.json or {}
    text = data.get('text','').strip()
    num_sentences = int(data.get('sentences', 5))
    if not text:
        return jsonify(error="No text provided"), 400
    lang_code, lang_name = detect_language(text)
    summary  = summarize_text(text, lang_code, num_sentences)
    keywords = extract_keywords(text, lang_code)
    orig_words = len(text.split())
    summ_words = len(summary.split())
    reduction  = round((1 - summ_words/orig_words)*100) if orig_words else 0
    return jsonify(summary=summary, language_code=lang_code, language_name=lang_name,
                   keywords=keywords,
                   stats=dict(original_words=orig_words, summary_words=summ_words,
                              reduction=reduction, sentences=num_sentences))

@app.route('/api/summarize_url', methods=['POST'])
def api_summarize_url():
    data = request.json or {}
    url  = data.get('url','').strip()
    if not url:
        return jsonify(error="No URL provided"), 400
    text, title = extract_url(url)
    if not text or text.startswith('['):
        return jsonify(error=text), 400
    lang_code, lang_name = detect_language(text)
    num = int(data.get('sentences', 5))
    summary  = summarize_text(text, lang_code, num)
    keywords = extract_keywords(text, lang_code)
    orig_words = len(text.split())
    summ_words = len(summary.split())
    return jsonify(title=title, summary=summary, language_code=lang_code,
                   language_name=lang_name, keywords=keywords,
                   stats=dict(original_words=orig_words, summary_words=summ_words,
                              reduction=round((1-summ_words/orig_words)*100) if orig_words else 0,
                              sentences=num))

@app.route('/api/summarize_pdf', methods=['POST'])
def api_summarize_pdf():
    f = request.files.get('pdf')
    if not f:
        return jsonify(error="No PDF uploaded"), 400
    text = extract_pdf(f.read())
    if not text.strip():
        return jsonify(error="Could not extract text from PDF"), 400
    num = int(request.form.get('sentences', 5))
    lang_code, lang_name = detect_language(text)
    summary  = summarize_text(text, lang_code, num)
    keywords = extract_keywords(text, lang_code)
    orig_words = len(text.split())
    summ_words = len(summary.split())
    return jsonify(summary=summary, language_code=lang_code, language_name=lang_name,
                   keywords=keywords,
                   stats=dict(original_words=orig_words, summary_words=summ_words,
                              reduction=round((1-summ_words/orig_words)*100) if orig_words else 0,
                              sentences=num))

@app.route('/api/translate', methods=['POST'])
def api_translate():
    data = request.json or {}
    text = data.get('text','').strip()
    src  = data.get('src','auto')
    tgt  = data.get('tgt','en')
    if not text:
        return jsonify(error="No text"), 400
    return jsonify(translated=translate_text(text, src, tgt))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
