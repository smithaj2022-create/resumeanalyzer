from flask import Flask, render_template, request, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import json
import traceback
import logging
import numpy as np
from werkzeug.utils import secure_filename

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'docx'}

db = SQLAlchemy(app)

class ResumeAnalysis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(200), nullable=False)
    original_filename = db.Column(db.String(200))
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    candidate_name = db.Column(db.String(100))
    candidate_email = db.Column(db.String(100))
    candidate_phone = db.Column(db.String(20))
    candidate_location = db.Column(db.String(100))
    
    work_experience = db.Column(db.Text)
    education = db.Column(db.Text)
    skills = db.Column(db.Text)
    
    classification_status = db.Column(db.String(20), default='Pending')
    department = db.Column(db.String(50))
    ranking_score = db.Column(db.Float, default=0.0)
    experience_years = db.Column(db.Float, default=0.0)
    education_level = db.Column(db.String(50))
    
    ai_generated_score = db.Column(db.Float, default=0.0)
    date_consistency_score = db.Column(db.Float, default=0.0)
    skill_authenticity_score = db.Column(db.Float, default=0.0)
    overall_fraud_score = db.Column(db.Float, default=0.0)
    
    analysis_report = db.Column(db.Text)
    processing_time = db.Column(db.Float)  # Processing time in seconds
    
    def to_dict(self):
        return {
            'id': self.id,
            'filename': self.filename,
            'original_filename': self.original_filename,
            'candidate_name': self.candidate_name,
            'candidate_email': self.candidate_email,
            'candidate_phone': self.candidate_phone,
            'candidate_location': self.candidate_location,
            'classification_status': self.classification_status,
            'department': self.department,
            'ranking_score': self.ranking_score,
            'experience_years': self.experience_years,
            'education_level': self.education_level,
            'ai_generated_score': self.ai_generated_score,
            'overall_fraud_score': self.overall_fraud_score,
            'analysis_report': self.analysis_report,
            'skills': json.loads(self.skills) if self.skills else [],
            'upload_date': self.upload_date.strftime('%Y-%m-%d %H:%M:%S'),
            'processing_time': self.processing_time
        }

# Import components with error handling
try:
    from utils.parser import ResumeParser
    from models.classifier import ResumeClassifier
    from models.ranker import ResumeRanker
    logger.info("✅ All modules imported successfully")
except ImportError as e:
    logger.error(f"❌ Import error: {e}")
    raise

# Initialize components
parser = ResumeParser()
classifier = ResumeClassifier()
ranker = ResumeRanker()

# Create tables
with app.app_context():
    try:
        db.create_all()
        logger.info("✅ Database tables created successfully")
    except Exception as e:
        logger.error(f"❌ Database error: {e}")

def allowed_file(filename):
    """Check if the file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def cleanup_old_files():
    """Clean up files older than 24 hours"""
    try:
        upload_dir = app.config['UPLOAD_FOLDER']
        if not os.path.exists(upload_dir):
            return
        
        current_time = datetime.now()
        for filename in os.listdir(upload_dir):
            file_path = os.path.join(upload_dir, filename)
            if os.path.isfile(file_path):
                file_time = datetime.fromtimestamp(os.path.getctime(file_path))
                if (current_time - file_time).days > 1:  # Older than 1 day
                    os.remove(file_path)
                    logger.info(f"🧹 Cleaned up old file: {filename}")
    except Exception as e:
        logger.error(f"❌ Error cleaning up files: {e}")

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'database': 'connected' if db.session.bind else 'disconnected'
    })

@app.route('/favicon.ico')
def favicon():
    """Serve favicon"""
    return send_file('static/favicon.svg', mimetype='image/svg+xml')

@app.route('/analyze', methods=['POST'])
def analyze_resume():
    """Analyze uploaded resume"""
    start_time = datetime.now()
    
    try:
        # Check if file was uploaded
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        
        # Check if file was selected
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Validate file type
        if not allowed_file(file.filename):
            return jsonify({
                'error': 'Invalid file type. Only PDF and DOCX files are allowed.',
                'allowed_extensions': list(app.config['ALLOWED_EXTENSIONS'])
            }), 400
        
        # Secure filename and save file
        original_filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        filename = f"{timestamp}_{original_filename}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Ensure upload directory exists
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        
        file.save(file_path)
        logger.info(f"📁 File saved: {filename}")
        
        # Extract text from file
        file_ext = os.path.splitext(file.filename)[1].lower()
        text = parser.extract_text(file_path, file_ext)
        
        if not text or len(text.strip()) < 50:
            # Clean up the uploaded file
            if os.path.exists(file_path):
                os.remove(file_path)
            return jsonify({
                'error': 'Could not extract sufficient text from document. The file may be corrupted, scanned, or contain mostly images.'
            }), 400
        
        logger.info(f"📝 Extracted {len(text)} characters from resume")
        
        # Parse resume information
        personal_info = parser.parse_personal_info(text)
        skills = parser.extract_skills(text)
        experience = parser.extract_experience(text)
        education = parser.extract_education(text)
        
        logger.info(f"👤 Candidate: {personal_info['name']} | Skills: {sum(len(s) for s in skills.values())}")
        
        # Classify resume
        status, department, ranking_score = classifier.classify_resume(text, skills)
        
        # Fraud detection
        fraud_score, fraud_findings = classifier.detect_fraud(text, skills, experience)
        
        # Calculate processing time
        processing_time = (datetime.now() - start_time).total_seconds()
        
        # Create comprehensive analysis report
        analysis_report = f"""
COMPREHENSIVE RESUME ANALYSIS REPORT
====================================
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Processing Time: {processing_time:.2f} seconds

CANDIDATE INFORMATION:
────────────────────
Name: {personal_info['name'] or 'Not specified'}
Email: {personal_info['email'] or 'Not specified'}
Phone: {personal_info['phone'] or 'Not specified'}
Location: {personal_info['location'] or 'Not specified'}

CLASSIFICATION RESULTS:
──────────────────────
Status: {status}
Recommended Department: {department}
Ranking Score: {ranking_score:.1f}/100
Experience: {experience['total_years']} years
Highest Education: {education['highest_degree']}

SKILLS ANALYSIS:
───────────────
Total Skills Categories: {len(skills)}
Total Skills: {sum(len(skills[cat]) for cat in skills)}

{json.dumps(skills, indent=2, ensure_ascii=False)}

FRAUD DETECTION:
───────────────
Overall Fraud Score: {fraud_score}%
Findings:
{chr(10).join(['• ' + finding for finding in fraud_findings]) if fraud_findings else '• No significant fraud indicators detected'}

RECOMMENDATION:
──────────────
{'✅ SHORTLIST - Strong candidate for ' + department + ' department' if status == 'Accepted' else '❌ REJECT - Does not meet minimum criteria'}
"""

        # Save analysis to database
        analysis = ResumeAnalysis(
            filename=filename,
            original_filename=original_filename,
            candidate_name=personal_info['name'],
            candidate_email=personal_info['email'],
            candidate_phone=personal_info['phone'],
            candidate_location=personal_info['location'],
            work_experience=json.dumps(experience, ensure_ascii=False),
            education=json.dumps(education, ensure_ascii=False),
            skills=json.dumps(skills, ensure_ascii=False),
            classification_status=status,
            department=department,
            ranking_score=ranking_score,
            experience_years=experience['total_years'],
            education_level=education['highest_degree'],
            overall_fraud_score=fraud_score,
            analysis_report=analysis_report,
            processing_time=processing_time
        )
        
        db.session.add(analysis)
        db.session.commit()
        
        logger.info(f"✅ Analysis completed: {status} | {department} | Score: {ranking_score}")
        
        # Return analysis results
        response_data = analysis.to_dict()
        response_data['processing_time'] = processing_time
        response_data['text_length'] = len(text)
        response_data['total_skills'] = sum(len(skills[cat]) for cat in skills)
        
        return jsonify(response_data)
        
    except Exception as e:
        logger.error(f"❌ Analysis failed: {str(e)}")
        logger.error(traceback.format_exc())
        
        # Clean up uploaded file if it exists
        try:
            file_path_to_remove = locals().get('file_path')
            if file_path_to_remove and os.path.exists(file_path_to_remove):
                os.remove(file_path_to_remove)
        except:
            pass
        
        return jsonify({
            'error': f'Analysis failed: {str(e)}',
            'details': 'Please check the file format and try again.'
        }), 500

@app.route('/history')
def history():
    """Display analysis history"""
    try:
        analyses = ResumeAnalysis.query.order_by(ResumeAnalysis.upload_date.desc()).all()
        return render_template('history.html', analyses=analyses)
    except Exception as e:
        logger.error(f"❌ History error: {e}")
        return render_template('history.html', analyses=[])

@app.route('/dashboard')
def dashboard():
    """Display analytics dashboard"""
    try:
        analyses = ResumeAnalysis.query.all()
        total = len(analyses)
        accepted = len([a for a in analyses if a.classification_status == 'Accepted'])
        
        # Department distribution
        departments = {}
        for analysis in analyses:
            if analysis.department:
                departments[analysis.department] = departments.get(analysis.department, 0) + 1
        
        # Average scores
        avg_ranking = np.mean([a.ranking_score for a in analyses]) if analyses else 0
        avg_fraud = np.mean([a.overall_fraud_score for a in analyses]) if analyses else 0
        
        return render_template('dashboard.html',
                             total_resumes=total,
                             accepted=accepted,
                             rejected=total - accepted,
                             departments=departments,
                             analyses=analyses,
                             avg_ranking=avg_ranking,
                             avg_fraud=avg_fraud)
    except Exception as e:
        logger.error(f"❌ Dashboard error: {e}")
        return render_template('dashboard.html',
                             total_resumes=0,
                             accepted=0,
                             rejected=0,
                             departments={},
                             analyses=[],
                             avg_ranking=0,
                             avg_fraud=0)

@app.route('/api/shortlist')
def get_shortlisted():
    """API endpoint for shortlisted candidates"""
    try:
        accepted_candidates = ResumeAnalysis.query.filter_by(classification_status='Accepted').all()
        candidates_data = [candidate.to_dict() for candidate in accepted_candidates]
        top_candidates = ranker.get_top_candidates_all_departments(candidates_data, top_n=5)
        return jsonify(top_candidates)
    except Exception as e:
        logger.error(f"❌ Shortlist API error: {e}")
        return jsonify({'error': 'Failed to get shortlisted candidates'}), 500

@app.route('/api/analyses')
def get_analyses():
    """API endpoint for all analyses"""
    try:
        analyses = ResumeAnalysis.query.order_by(ResumeAnalysis.upload_date.desc()).all()
        return jsonify([analysis.to_dict() for analysis in analyses])
    except Exception as e:
        logger.error(f"❌ Analyses API error: {e}")
        return jsonify({'error': 'Failed to get analyses'}), 500

@app.route('/analysis/<int:analysis_id>')
def get_analysis(analysis_id):
    """Get specific analysis by ID"""
    try:
        analysis = ResumeAnalysis.query.get_or_404(analysis_id)
        return jsonify(analysis.to_dict())
    except Exception as e:
        logger.error(f"❌ Analysis {analysis_id} error: {e}")
        return jsonify({'error': 'Analysis not found'}), 404

@app.route('/delete/<int:analysis_id>', methods=['DELETE'])
def delete_analysis(analysis_id):
    """Delete analysis by ID"""
    try:
        analysis = ResumeAnalysis.query.get_or_404(analysis_id)
        
        # Delete associated file
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], analysis.filename)
        if os.path.exists(file_path):
            os.remove(file_path)
        
        db.session.delete(analysis)
        db.session.commit()
        
        logger.info(f"🗑️ Deleted analysis: {analysis_id}")
        return jsonify({'message': 'Analysis deleted successfully'})
    except Exception as e:
        logger.error(f"❌ Delete error: {e}")
        return jsonify({'error': 'Failed to delete analysis'}), 500

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

@app.errorhandler(413)
def too_large(error):
    return jsonify({'error': 'File too large. Maximum size is 16MB.'}), 413

if __name__ == '__main__':
    # Ensure required directories exist
    os.makedirs('uploads', exist_ok=True)
    os.makedirs('data/trained_models', exist_ok=True)
    
    # Clean up old files on startup
    cleanup_old_files()
    
    print("🚀 Starting Smart Resume Analyzer...")
    print("📊 Dashboard: http://localhost:5000")
    print("📈 API Health: http://localhost:5000/health")
    print("🔍 Analysis History: http://localhost:5000/history")
    print("⚡ Ready to analyze resumes!")
    print("-" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=5000)