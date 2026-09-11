"""
Cleans and tokenizes raw text before matching.
"""
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

for pkg in ('punkt', 'punkt_tab', 'stopwords', 'wordnet'):
    try:
        nltk.data.find(f'tokenizers/{pkg}' if 'punkt' in pkg else f'corpora/{pkg}')
    except LookupError:
        nltk.download(pkg, quiet=True)

STOP_WORDS = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

SECTION_HEADERS = [
    'experience', 'work experience', 'education', 'skills',
    'projects', 'certifications', 'summary', 'objective', 'contact'
]


def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s.+#]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def tokenize(text):
    from nltk.tokenize import word_tokenize
    return word_tokenize(text)


def remove_stopwords(tokens):
    return [t for t in tokens if t not in STOP_WORDS and len(t) > 1]


def lemmatize(tokens):
    return [lemmatizer.lemmatize(t) for t in tokens]


def preprocess(text):
    cleaned = clean_text(text)
    tokens = tokenize(cleaned)
    tokens = remove_stopwords(tokens)
    tokens = lemmatize(tokens)
    return tokens


def detect_sections(raw_text):
    lower_text = raw_text.lower()
    return [h for h in SECTION_HEADERS if h in lower_text]