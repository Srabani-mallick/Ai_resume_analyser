"""
Combines keyword matching + formatting checks into a final ATS-style score.
"""
from utils.preprocessor import detect_sections, SECTION_HEADERS

WEIGHT_KEYWORD_MATCH = 0.6
WEIGHT_SEMANTIC_SIMILARITY = 0.25
WEIGHT_FORMATTING = 0.15


def formatting_score(raw_text, resume_file_ext):
    score = 0.0
    max_score = 100.0
    checks = []

    found_sections = detect_sections(raw_text)
    section_ratio = len(found_sections) / len(SECTION_HEADERS)
    section_points = section_ratio * 40
    score += section_points
    checks.append(('section_headers', found_sections, section_points))

    has_email = '@' in raw_text
    has_phone = any(char.isdigit() for char in raw_text[:500])
    contact_points = (10 if has_email else 0) + (10 if has_phone else 0)
    score += contact_points
    checks.append(('contact_info', {'email': has_email, 'phone_like': has_phone}, contact_points))

    word_count = len(raw_text.split())
    if 250 <= word_count <= 1200:
        length_points = 20
    elif 150 <= word_count < 250 or 1200 < word_count <= 1600:
        length_points = 10
    else:
        length_points = 0
    score += length_points
    checks.append(('word_count', word_count, length_points))

    format_points = 20 if word_count > 20 else 0
    score += format_points
    checks.append(('extractable_text', resume_file_ext, format_points))

    return round(min(score, max_score), 2), checks


def calculate_overall_score(keyword_score, similarity_score, format_score):
    overall = (
        keyword_score * WEIGHT_KEYWORD_MATCH +
        similarity_score * WEIGHT_SEMANTIC_SIMILARITY +
        format_score * WEIGHT_FORMATTING
    )
    return round(overall, 2)