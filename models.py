from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Resume(db.Model):
    __tablename__ = 'resumes'

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    extracted_text = db.Column(db.Text, default='')
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

    results = db.relationship('AnalysisResult', backref='resume', lazy=True)

    def __repr__(self):
        return f"<Resume #{self.id} ({self.filename})>"


class JobDescription(db.Model):
    __tablename__ = 'job_descriptions'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), default='')
    raw_text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    results = db.relationship('AnalysisResult', backref='job_description', lazy=True)

    def __repr__(self):
        return f"<JD #{self.id} ({self.title})>"


class AnalysisResult(db.Model):
    __tablename__ = 'analysis_results'

    id = db.Column(db.Integer, primary_key=True)
    resume_id = db.Column(db.Integer, db.ForeignKey('resumes.id'), nullable=False)
    job_description_id = db.Column(db.Integer, db.ForeignKey('job_descriptions.id'), nullable=False)

    score = db.Column(db.Float, nullable=False)
    keyword_match_score = db.Column(db.Float, default=0)
    formatting_score = db.Column(db.Float, default=0)

    matched_keywords = db.Column(db.JSON, default=list)
    missing_keywords = db.Column(db.JSON, default=list)
    suggestions = db.Column(db.JSON, default=list)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Result #{self.id} - {self.score:.1f}%>"