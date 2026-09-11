"""
Compares resume text against job description text using TF-IDF + cosine similarity.
"""
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def tfidf_similarity(resume_text, jd_text):
    documents = [resume_text, jd_text]
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(documents)
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    return round(similarity * 100, 2)


def extract_keywords(jd_text, top_n=25):
    vectorizer = TfidfVectorizer(stop_words='english', max_features=top_n)
    vectorizer.fit([jd_text])
    return list(vectorizer.get_feature_names_out())


def keyword_overlap(resume_tokens, jd_keywords):
    resume_token_set = set(resume_tokens)
    matched = [kw for kw in jd_keywords if kw in resume_token_set]
    missing = [kw for kw in jd_keywords if kw not in resume_token_set]
    return matched, missing


def keyword_match_score(matched, jd_keywords):
    if not jd_keywords:
        return 0.0
    return round((len(matched) / len(jd_keywords)) * 100, 2)