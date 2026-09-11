"""
Turns scoring gaps into human-readable suggestions.
"""

ACTION_VERBS = [
    'led', 'built', 'developed', 'designed', 'implemented', 'created',
    'improved', 'optimized', 'managed', 'launched', 'automated', 'reduced'
]


def generate_feedback(missing_keywords, formatting_checks, raw_text):
    suggestions = []

    if missing_keywords:
        top_missing = missing_keywords[:8]
        suggestions.append(
            f"Add these missing keywords if genuinely relevant to your experience: {', '.join(top_missing)}."
        )

    for check_name, value, points in formatting_checks:
        if check_name == 'section_headers' and points < 30:
            missing_sections = set(['experience', 'education', 'skills', 'projects']) - set(value)
            if missing_sections:
                suggestions.append(
                    f"Consider adding clear section headers for: {', '.join(missing_sections)}."
                )
        if check_name == 'contact_info':
            if not value.get('email'):
                suggestions.append("No email address detected — make sure it's in plain text, not an image.")
        if check_name == 'word_count':
            if value < 150:
                suggestions.append("Resume looks too short — add more detail to your experience and projects.")
            elif value > 1600:
                suggestions.append("Resume is quite long — consider trimming to the most relevant 1-2 pages.")
        if check_name == 'extractable_text' and points == 0:
            suggestions.append(
                "Very little text could be extracted — avoid scanned images or heavy graphical templates, "
                "since ATS software can't read them either."
            )

    lower_text = raw_text.lower()
    used_verbs = [v for v in ACTION_VERBS if v in lower_text]
    if len(used_verbs) < 3:
        suggestions.append(
            "Use more strong action verbs (e.g. led, built, optimized, automated) to describe your experience."
        )

    if not suggestions:
        suggestions.append("Resume looks well-aligned with this job description. Nice work.")

    return suggestions