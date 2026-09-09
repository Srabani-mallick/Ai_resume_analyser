# AI Resume Analyzer

A Flask web app that compares a resume against a job description and gives an
ATS (Applicant Tracking System) compatibility score, along with matched/missing
keywords and improvement suggestions.

## Features
- Upload resume as PDF or DOCX
- Paste any job description
- Get an overall ATS match score (0–100%)
- See which JD keywords are matched vs missing
- Get actionable suggestions to improve the resume
- View history of past analyses

## Tech Stack
- **Backend:** Flask, Flask-SQLAlchemy
- **NLP/Matching:** scikit-learn (TF-IDF + cosine similarity), NLTK
- **File Parsing:** pdfplumber (PDF), python-docx (DOCX)
- **Database:** SQLite
- **Frontend:** Jinja2 templates, Chart.js (score visualization)

## Folder Structure
ai_resume_analyzer/
├── app.py # main Flask app + routes
├── config.py # app configuration
├── models.py # SQLAlchemy models
├── requirements.txt
│
├── utils/
│ ├── init.py
│ ├── parser.py # extract text from PDF/DOCX
│ ├── preprocessor.py # clean, tokenize, lemmatize text
│ ├── matcher.py # TF-IDF + cosine similarity matching
│ ├── scorer.py # combine scores into final ATS score
│ └── suggestions.py # generate feedback text
│
├── templates/
│ ├── base.html
│ ├── upload.html
│ ├── result.html
│ └── history.html
│
├── static/
│ └── css/
│ └── style.css
│
├── uploads/ # saved resume files (gitignored)
└── instance/ # SQLite database (gitignored)


## Setup

```bash
# 1. Clone the repository
git clone 
cd ai_resume_analyzer

# 2. Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
python app.py
```

Then open `http://127.0.0.1:5000/` in your browser.

The database (`instance/resume_analyzer.db`) and `uploads/` folder are created
automatically on first run — no manual setup needed.

## How It Works
1. **Parsing** — `parser.py` extracts raw text from the uploaded PDF/DOCX
2. **Preprocessing** — `preprocessor.py` cleans, tokenizes, removes stopwords,
   and lemmatizes both the resume and job description text
3. **Matching** — `matcher.py` computes TF-IDF cosine similarity and extracts
   top keywords from the job description, then checks which ones appear in
   the resume
4. **Scoring** — `scorer.py` combines keyword match (60%), semantic similarity
   (25%), and formatting checks (15%) into one overall score
5. **Suggestions** — `suggestions.py` turns missing keywords and formatting
   gaps into readable feedback

   ## Screenshots

### Upload Page
![Upload Page](screenshots/dashboard.png)

### Result Page
![Result Page](screenshots/result-page.png)
## Screenshots

### Upload Page
![Upload Page](screenshots/history.png)

### Result Page
![Result Page](screenshots/output2.png)

## Notes
- Max upload size: 5MB (adjustable in `config.py`)
- Supported formats: PDF, DOCX only
- Formatting score is rule-based (section headers, contact info, word count) —
  it's a heuristic proxy for ATS parsing, not a real ATS engine
- NLTK data (stopwords, tokenizer, lemmatizer) downloads automatically on first run

## Author
Sushree  srabani Mallick