# Smart Resume Analyzer

## Overview
AI-powered resume analysis web application built with Flask. The system automatically parses resumes, classifies candidates into departments, detects potential fraud, and provides comprehensive analysis reports.

## Project Architecture

### Technology Stack
- **Backend**: Flask (Python 3.11)
- **Database**: SQLite with SQLAlchemy ORM
- **ML/AI**: scikit-learn, NLTK
- **Document Processing**: PyPDF2, pdfminer.six, python-docx
- **Frontend**: Bootstrap 5, Font Awesome

### Key Components
1. **Resume Parser** (`utils/parser.py`): Extracts text from PDF/DOCX and parses personal info, skills, experience, education
2. **Classifier** (`models/classifier.py`): ML-based department classification and fraud detection
3. **Ranker** (`models/ranker.py`): Ranks candidates based on department-specific criteria
4. **Web Interface**: Upload, history, and dashboard views

### Features
- Resume upload (PDF/DOCX, max 16MB)
- Automatic text extraction and parsing
- ML-based classification into 7 departments (IT, HR, Finance, Marketing, Engineering, Operations, Sales)
- Fraud detection (AI-generated content, skill exaggeration, date inconsistencies)
- Candidate ranking with department-specific scoring
- Analysis history tracking
- Analytics dashboard

## Database Schema
**ResumeAnalysis Model**:
- Personal info (name, email, phone, location)
- Classification (status, department, ranking score)
- Experience and education details
- Fraud scores (AI-generated, date consistency, skill authenticity, overall)
- Full analysis report

## Recent Changes
- **2025-10-23**: Project imported to Replit environment
  - Installed Python 3.11 and all dependencies
  - Fixed numpy import issue in app.py
  - Fixed file_path error handling in exception handler
  - Configured .gitignore for Python/Flask project
  - Set up workflow to run on port 5000
  - Fixed infinite loading issue in resume analysis
  - Added timeout protection (30 seconds) for file uploads
  - Improved modal backdrop cleanup to prevent UI freezing
  - Added favicon route to fix 404 errors
  - Created pyrightconfig.json (LSP import warnings are false positives - all packages installed)

## User Preferences
None specified yet.

## Development Setup
- Python 3.11 with pip package manager
- All dependencies installed from requirements.txt
- Development server runs on 0.0.0.0:5000
- SQLite database created automatically on first run
- Upload folder created automatically

## Production Notes
- Use `run.py` for production deployment (instead of `app.py`)
- Environment variables: DEBUG, HOST, PORT
- Threaded mode enabled for better performance
