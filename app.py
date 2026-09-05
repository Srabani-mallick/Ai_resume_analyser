import os
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename

from config import Config
from models import db, Resume, JobDescription, AnalysisResult

from utils.parser import extract_text
from utils.preprocessor import preprocess
from utils.matcher import tfidf_similarity, extract_keywords, keyword_overlap, keyword_match_score
from utils.scorer import formatting_score, calculate_overall_score
from utils.suggestions import generate_feedback

app = Flask(__name__)
app.config.from_object(Config)

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(os.path.join(os.path.dirname(__file__), 'instance'), exist_ok=True)

db.init_app(app)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        uploaded_file = request.files.get('resume_file')
        jd_text = request.form.get('job_description', '').strip()
        job_title = request.form.get('job_title', '').strip()

        if not uploaded_file or uploaded_file.filename == '':
            flash('Please choose a resume file.')
            return redirect(url_for('upload'))

        if not allowed_file(uploaded_file.filename):
            flash('Only PDF and DOCX files are supported.')
            return redirect(url_for('upload'))

        if not jd_text:
            flash('Please paste a job description.')
            return redirect(url_for('upload'))

        filename = secure_filename(uploaded_file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        uploaded_file.save(file_path)

        raw_text = extract_text(file_path)

        resume = Resume(filename=filename, extracted_text=raw_text)
        db.session.add(resume)

        job_description = JobDescription(title=job_title, raw_text=jd_text)
        db.session.add(job_description)
        db.session.commit()

        resume_tokens = preprocess(raw_text)
        jd_tokens_text = ' '.join(preprocess(jd_text))
        resume_tokens_text = ' '.join(resume_tokens)

        similarity_score = tfidf_similarity(resume_tokens_text, jd_tokens_text)
        jd_keywords = extract_keywords(jd_text)
        matched, missing = keyword_overlap(resume_tokens, jd_keywords)
        kw_score = keyword_match_score(matched, jd_keywords)

        file_ext = filename.rsplit('.', 1)[1].lower()
        fmt_score, fmt_checks = formatting_score(raw_text, file_ext)

        overall = calculate_overall_score(kw_score, similarity_score, fmt_score)

        suggestions = generate_feedback(missing, fmt_checks, raw_text)

        result = AnalysisResult(
            resume_id=resume.id,
            job_description_id=job_description.id,
            score=overall,
            keyword_match_score=kw_score,
            formatting_score=fmt_score,
            matched_keywords=matched,
            missing_keywords=missing,
            suggestions=suggestions,
        )
        db.session.add(result)
        db.session.commit()

        return redirect(url_for('result', result_id=result.id))

    return render_template('upload.html')


@app.route('/result/<int:result_id>')
def result(result_id):
    result = AnalysisResult.query.get_or_404(result_id)
    return render_template('result.html', result=result)


@app.route('/history')
def history():
    results = AnalysisResult.query.order_by(AnalysisResult.created_at.desc()).limit(50).all()
    return render_template('history.html', results=results)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)