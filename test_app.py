#!/usr/bin/env python3
"""
Test script for Smart Resume Analyzer
Run this to check if all components are working correctly
"""

import sys
import os
import sqlite3
import tempfile
import shutil
from datetime import datetime

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def print_status(message, status="INFO"):
    """Print colored status messages"""
    colors = {
        "INFO": "\033[94m",    # Blue
        "SUCCESS": "\033[92m", # Green
        "WARNING": "\033[93m", # Yellow
        "ERROR": "\033[91m",   # Red
        "END": "\033[0m"       # Reset
    }
    print(f"{colors.get(status, '')}[{status}] {message}{colors['END']}")

def test_imports():
    """Test if all required modules can be imported"""
    print_status("Testing module imports...", "INFO")
    
    modules_to_test = [
        ("Flask", "flask"),
        ("SQLAlchemy", "flask_sqlalchemy"),
        ("PyPDF2", "PyPDF2"),
        ("python-docx", "docx"),
        ("scikit-learn", "sklearn"),
        ("numpy", "numpy"),
        ("pandas", "pandas"),
        ("nltk", "nltk"),
        ("joblib", "joblib")
    ]
    
    all_imports_ok = True
    for module_name, import_name in modules_to_test:
        try:
            if import_name == "flask_sqlalchemy":
                __import__("flask_sqlalchemy")
            else:
                __import__(import_name)
            print_status(f"✅ {module_name}", "SUCCESS")
        except ImportError as e:
            print_status(f"❌ {module_name} - {e}", "ERROR")
            all_imports_ok = False
    
    return all_imports_ok

def test_custom_modules():
    """Test if our custom modules can be imported"""
    print_status("Testing custom modules...", "INFO")
    
    custom_modules = [
        ("ResumeParser", "utils.parser"),
        ("TextPreprocessor", "utils.preprocessor"),
        ("FeatureExtractor", "utils.feature_extractor"),
        ("ResumeClassifier", "models.classifier"),
        ("ResumeRanker", "models.ranker")
    ]
    
    all_custom_ok = True
    for class_name, module_path in custom_modules:
        try:
            module = __import__(module_path, fromlist=[class_name])
            getattr(module, class_name)
            print_status(f"✅ {class_name}", "SUCCESS")
        except ImportError as e:
            print_status(f"❌ {class_name} - {e}", "ERROR")
            all_custom_ok = False
        except AttributeError as e:
            print_status(f"❌ {class_name} - Class not found", "ERROR")
            all_custom_ok = False
    
    return all_custom_ok

def test_database():
    """Test database connection and operations"""
    print_status("Testing database...", "INFO")
    
    try:
        from app import app, db, ResumeAnalysis
        
        with app.app_context():
            # Create all tables
            db.create_all()
            print_status("✅ Database tables created", "SUCCESS")
            
            # Test basic CRUD operations
            test_analysis = ResumeAnalysis(
                filename="test_file.pdf",
                candidate_name="Test Candidate",
                candidate_email="test@example.com",
                classification_status="Accepted",
                department="IT",
                ranking_score=85.5
            )
            
            db.session.add(test_analysis)
            db.session.commit()
            print_status("✅ Database write operation", "SUCCESS")
            
            # Test read operation
            saved_analysis = ResumeAnalysis.query.filter_by(candidate_name="Test Candidate").first()
            if saved_analysis:
                print_status("✅ Database read operation", "SUCCESS")
            else:
                print_status("❌ Database read operation failed", "ERROR")
                return False
            
            # Clean up test data
            db.session.delete(saved_analysis)
            db.session.commit()
            print_status("✅ Database cleanup", "SUCCESS")
            
        return True
        
    except Exception as e:
        print_status(f"❌ Database test failed: {e}", "ERROR")
        return False

def test_parser():
    """Test resume parser functionality"""
    print_status("Testing resume parser...", "INFO")
    
    try:
        from utils.parser import ResumeParser
        
        parser = ResumeParser()
        
        # Test with sample text (simulating what would be extracted from a file)
        sample_text = """
        JOHN DOE
        Software Engineer
        Email: john.doe@email.com
        Phone: +1 (555) 123-4567
        Location: San Francisco, CA
        
        EXPERIENCE:
        Senior Python Developer - Tech Company (2020-2023)
        Developed web applications using Python, Django, and React.
        
        EDUCATION:
        Bachelor of Science in Computer Science - University (2016-2020)
        
        SKILLS:
        Python, JavaScript, Django, React, SQL, AWS, Docker
        """
        
        personal_info = parser.parse_personal_info(sample_text)
        skills = parser.extract_skills(sample_text)
        experience = parser.extract_experience(sample_text)
        education = parser.extract_education(sample_text)
        
        # Verify parsed data
        if personal_info['name']:
            print_status("✅ Personal info parsing", "SUCCESS")
        else:
            print_status("⚠️ Name not parsed", "WARNING")
            
        if personal_info['email']:
            print_status("✅ Email parsing", "SUCCESS")
        else:
            print_status("⚠️ Email not parsed", "WARNING")
            
        if len(skills) > 0:
            print_status("✅ Skills extraction", "SUCCESS")
        else:
            print_status("❌ Skills extraction failed", "ERROR")
            return False
            
        print_status(f"📊 Found {len(skills)} skill categories", "INFO")
        print_status(f"📅 Experience: {experience['total_years']} years", "INFO")
        print_status(f"🎓 Education: {education['highest_degree']}", "INFO")
        
        return True
        
    except Exception as e:
        print_status(f"❌ Parser test failed: {e}", "ERROR")
        return False

def test_classifier():
    """Test ML classifier functionality"""
    print_status("Testing ML classifier...", "INFO")
    
    try:
        from models.classifier import ResumeClassifier
        
        classifier = ResumeClassifier()
        
        # Test with sample data
        test_text = """
        Python developer with 5 years experience in web development.
        Skills include Python, Django, React, SQL, and AWS.
        Bachelor's degree in Computer Science.
        """
        
        test_skills = {
            'Programming': ['python', 'javascript'],
            'Web Development': ['django', 'react'],
            'Database': ['sql'],
            'Cloud & DevOps': ['aws']
        }
        
        test_experience = {'total_years': 5}
        
        status, department, score = classifier.classify_resume(test_text, test_skills)
        fraud_score, findings = classifier.detect_fraud(test_text, test_skills, test_experience)
        
        print_status(f"✅ Classification: {status} | {department} | Score: {score}", "SUCCESS")
        print_status(f"✅ Fraud detection: {fraud_score}%", "SUCCESS")
        
        if findings:
            print_status(f"🔍 Fraud findings: {len(findings)}", "INFO")
        
        return True
        
    except Exception as e:
        print_status(f"❌ Classifier test failed: {e}", "ERROR")
        return False

def test_file_operations():
    """Test file upload and processing operations"""
    print_status("Testing file operations...", "INFO")
    
    try:
        # Create test uploads directory
        test_upload_dir = "test_uploads"
        os.makedirs(test_upload_dir, exist_ok=True)
        
        # Create a simple test file (simulating resume content)
        test_file_path = os.path.join(test_upload_dir, "test_resume.txt")
        with open(test_file_path, 'w', encoding='utf-8') as f:
            f.write("Test resume content for file operations testing.")
        
        if os.path.exists(test_file_path):
            print_status("✅ File creation", "SUCCESS")
            
            # Test file reading
            with open(test_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if content:
                    print_status("✅ File reading", "SUCCESS")
            
            # Clean up
            os.remove(test_file_path)
            os.rmdir(test_upload_dir)
            print_status("✅ File cleanup", "SUCCESS")
            
            return True
        else:
            print_status("❌ File creation failed", "ERROR")
            return False
            
    except Exception as e:
        print_status(f"❌ File operations test failed: {e}", "ERROR")
        return False

def run_comprehensive_test():
    """Run all tests and provide summary"""
    print("\n" + "="*60)
    print_status("🚀 STARTING COMPREHENSIVE TEST SUITE", "INFO")
    print("="*60)
    
    test_results = []
    
    # Run all tests
    test_results.append(("Module Imports", test_imports()))
    test_results.append(("Custom Modules", test_custom_modules()))
    test_results.append(("Database", test_database()))
    test_results.append(("Resume Parser", test_parser()))
    test_results.append(("ML Classifier", test_classifier()))
    test_results.append(("File Operations", test_file_operations()))
    
    # Print summary
    print("\n" + "="*60)
    print_status("📊 TEST SUMMARY", "INFO")
    print("="*60)
    
    passed = sum(1 for _, result in test_results if result)
    total = len(test_results)
    
    for test_name, result in test_results:
        status = "✅ PASS" if result else "❌ FAIL"
        color = "SUCCESS" if result else "ERROR"
        print_status(f"{status} - {test_name}", color)
    
    print("\n" + "="*60)
    print_status(f"Overall: {passed}/{total} tests passed", "SUCCESS" if passed == total else "WARNING")
    
    if passed == total:
        print_status("🎉 All tests passed! The application is ready to run.", "SUCCESS")
        print_status("👉 Run: python app.py", "INFO")
    else:
        print_status("⚠️ Some tests failed. Please check the errors above.", "WARNING")
        print_status("🔧 Check requirements.txt and file structure.", "INFO")
    
    print("="*60)
    
    return passed == total

if __name__ == "__main__":
    # Create necessary directories
    os.makedirs("uploads", exist_ok=True)
    os.makedirs("data/trained_models", exist_ok=True)
    os.makedirs("static/css", exist_ok=True)
    
    success = run_comprehensive_test()
    sys.exit(0 if success else 1)