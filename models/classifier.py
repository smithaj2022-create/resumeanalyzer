import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
import joblib
import os
import re

class ResumeClassifier:
    def __init__(self):
        self.departments = ['IT', 'HR', 'Finance', 'Marketing', 'Engineering', 'Operations', 'Sales']
        self.vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        self.classifier = RandomForestClassifier(n_estimators=100, random_state=42)
        self.is_trained = False
        self.load_or_train_model()
    
    def load_or_train_model(self):
        """Load existing model or train new one"""
        try:
            if os.path.exists('data/trained_models/vectorizer.pkl') and os.path.exists('data/trained_models/classifier.pkl'):
                self.vectorizer = joblib.load('data/trained_models/vectorizer.pkl')
                self.classifier = joblib.load('data/trained_models/classifier.pkl')
                self.is_trained = True
                print("✅ Pre-trained models loaded successfully!")
            else:
                self.train_model()
        except Exception as e:
            print(f"⚠️ Error loading models: {e}. Training new models...")
            self.train_model()
    
    def train_model(self):
        """Train the classification model with enhanced training data"""
        try:
            # Enhanced training data with more examples
            training_data = {
                'texts': [
                    # IT examples
                    "python java programming software development web database sql cloud aws docker kubernetes backend frontend",
                    "javascript react node.js web development full stack mobile app programming api rest",
                    "data science machine learning python sql analysis visualization pandas numpy",
                    "devops aws azure cloud infrastructure docker kubernetes ci cd jenkins",
                    
                    # HR examples
                    "recruitment hiring talent acquisition HR management interviewing onboarding employee relations",
                    "human resources payroll benefits compensation training development performance management",
                    "recruiter sourcing screening candidates HR policies compliance diversity inclusion",
                    
                    # Finance examples
                    "accounting finance budgeting financial analysis audit tax investment banking",
                    "financial planning analysis fpa forecasting budgeting reporting excel",
                    "accountant bookkeeping gaap financial statements audit tax preparation",
                    
                    # Marketing examples
                    "marketing sales digital social media SEO content strategy advertising branding",
                    "digital marketing google analytics seo sem social media content creation",
                    "brand management product marketing market research campaign management",
                    
                    # Engineering examples
                    "engineering mechanical electrical civil design construction manufacturing",
                    "mechanical engineer design cad solidworks manufacturing production",
                    "civil engineer construction project management structural design",
                    
                    # Operations examples
                    "operations supply chain logistics management production quality control",
                    "supply chain logistics inventory management procurement operations",
                    "project management operations process improvement lean manufacturing",
                    
                    # Sales examples
                    "sales business development client relationship negotiation deal closing",
                    "account executive sales representative business development b2b sales",
                    "sales manager team leadership revenue growth customer acquisition"
                ],
                'labels': [0, 0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6]
            }
            
            X = self.vectorizer.fit_transform(training_data['texts'])
            self.classifier.fit(X, training_data['labels'])
            self.is_trained = True
            
            # Ensure directory exists
            os.makedirs('data/trained_models', exist_ok=True)
            
            # Save models
            joblib.dump(self.vectorizer, 'data/trained_models/vectorizer.pkl')
            joblib.dump(self.classifier, 'data/trained_models/classifier.pkl')
            
            print("✅ Model trained and saved successfully!")
            
        except Exception as e:
            print(f"❌ Error training model: {e}")
            self.is_trained = False
    
    def classify_resume(self, text, skills):
        """Classify resume into department and status with enhanced logic"""
        try:
            if not self.is_trained:
                print("⚠️ Model not trained, using fallback classification")
                return self.fallback_classification(skills, text)
            
            # Create feature text from skills and resume content
            skill_text = " ".join([skill for category in skills.values() for skill in category])
            combined_text = text + " " + skill_text
            
            # Transform and predict
            X = self.vectorizer.transform([combined_text])
            dept_idx = self.classifier.predict(X)[0]
            department = self.departments[dept_idx] if dept_idx < len(self.departments) else 'General'
            
            # Enhanced acceptance logic
            status = self.determine_acceptance_status(skills, text)
            
            # Calculate comprehensive ranking score
            ranking_score = self.calculate_ranking_score(skills, text)
            
            return status, department, ranking_score
            
        except Exception as e:
            print(f"❌ Classification error: {e}")
            return self.fallback_classification(skills, text)
    
    def determine_acceptance_status(self, skills, text):
        """Enhanced acceptance criteria"""
        tech_skills = len(skills.get('Programming', [])) + len(skills.get('AI/ML', [])) + len(skills.get('Web Development', []))
        total_skills = sum(len(skills[cat]) for cat in skills)
        
        # Check for experience indicators
        year_pattern = r'\b(19|20)\d{2}\b'
        years = [int(year) for year in re.findall(year_pattern, text)]
        has_experience = len(years) >= 2
        
        # Check for education indicators
        has_education = any(degree in text.lower() for degree in ['bachelor', 'master', 'mba', 'ph.d', 'doctorate', 'degree'])
        
        # Enhanced acceptance rules
        if total_skills >= 4:  # Reduced threshold for better acceptance
            return "Accepted"
        elif tech_skills >= 2 and has_experience:
            return "Accepted"
        elif has_education and total_skills >= 2:
            return "Accepted"
        elif total_skills >= 3:  # More lenient for diverse skills
            return "Accepted"
        else:
            return "Rejected"
    
    def calculate_ranking_score(self, skills, text):
        """Calculate comprehensive ranking score (0-100)"""
        score = 0
        
        # Skills component (40 points max)
        total_skills = sum(len(skills[cat]) for cat in skills)
        score += min(total_skills * 4, 40)  # 4 points per skill, max 40
        
        # Technical skills bonus (20 points max)
        tech_skills = len(skills.get('Programming', [])) + len(skills.get('AI/ML', [])) + len(skills.get('Web Development', []))
        score += min(tech_skills * 5, 20)  # 5 points per tech skill, max 20
        
        # Experience component (20 points max)
        year_pattern = r'\b(19|20)\d{2}\b'
        years = [int(year) for year in re.findall(year_pattern, text)]
        if years:
            exp_years = max(years) - min(years)
            score += min(exp_years * 4, 20)  # 4 points per year, max 20
        
        # Education component (20 points max)
        education_bonus = 0
        text_lower = text.lower()
        
        if 'ph.d' in text_lower or 'doctorate' in text_lower:
            education_bonus = 20
        elif 'master' in text_lower or 'mba' in text_lower:
            education_bonus = 15
        elif 'bachelor' in text_lower or 'b.s.' in text_lower or 'b.a.' in text_lower:
            education_bonus = 10
        elif 'diploma' in text_lower or 'associate' in text_lower:
            education_bonus = 5
        
        score += education_bonus
        
        return min(score, 100)
    
    def detect_fraud(self, text, skills, experience):
        """Enhanced fraud detection with multiple checks"""
        findings = []
        score = 0
        
        # AI-generated content detection (25 points)
        ai_patterns = [
            r"\b(as an AI|language model|I cannot|I am unable to)\b",
            r"\b(based on my training|according to my knowledge)\b",
            r"\b(I don't have|I do not have)\b",
            r"\b(as a large language model)\b",
            r"\b(I am designed to|I am programmed to)\b"
        ]
        
        text_lower = text.lower()
        for pattern in ai_patterns:
            if re.search(pattern, text_lower, re.IGNORECASE):
                score += 25
                findings.append("🤖 AI-generated content patterns detected")
                break
        
        # Skill exaggeration check (20 points)
        total_skills = sum(len(skills[cat]) for cat in skills)
        if total_skills > 25:
            score += 25
            findings.append("📚 Unusually high number of skills listed (>25)")
        elif total_skills > 15:
            score += 15
            findings.append("📖 High number of skills listed (>15)")
        
        # Experience-skills mismatch (20 points)
        exp_years = experience.get('total_years', 0)
        if exp_years < 2 and total_skills > 12:
            score += 20
            findings.append("⚖️ Skills-to-experience ratio suspicious")
        
        # Date consistency check (30 points)
        year_pattern = r'\b(19|20)\d{2}\b'
        years = [int(year) for year in re.findall(year_pattern, text)]
        if len(years) >= 2:
            sorted_years = sorted(years)
            if years != sorted_years:
                score += 30
                findings.append("📅 Date inconsistencies detected - timeline issues")
        
        # Education level verification (15 points)
        education_keywords = {
            'high_school': ['high school', 'diploma'],
            'bachelors': ['bachelor', 'b.s.', 'b.a.', 'undergraduate'],
            'masters': ['master', 'm.s.', 'm.a.', 'mba', 'graduate'],
            'phd': ['ph.d', 'doctorate', 'phd']
        }
        
        education_levels_found = []
        for level, keywords in education_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                education_levels_found.append(level)
        
        if len(education_levels_found) > 2:
            score += 15
            findings.append("🎓 Multiple education levels claimed")
        
        # Contact information check (10 points)
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        phone_pattern = r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        
        emails = re.findall(email_pattern, text)
        phones = re.findall(phone_pattern, text)
        
        if len(emails) == 0 and len(phones) == 0:
            score += 10
            findings.append("📞 Missing contact information")
        
        # Text quality check (10 points)
        if len(text.strip()) < 100:
            score += 10
            findings.append("📝 Very short resume content")
        
        return min(score, 100), findings
    
    def fallback_classification(self, skills, text):
        """Fallback classification when ML model fails"""
        tech_skills = len(skills.get('Programming', [])) + len(skills.get('AI/ML', [])) + len(skills.get('Web Development', []))
        total_skills = sum(len(skills[cat]) for cat in skills)
        
        # Simple rule-based department assignment
        if tech_skills >= 2:
            department = "IT"
        elif len(skills.get('Soft Skills', [])) >= 3:
            department = "HR"
        elif any(finance in text.lower() for finance in ['finance', 'accounting', 'banking']):
            department = "Finance"
        elif any(marketing in text.lower() for marketing in ['marketing', 'sales', 'advertising']):
            department = "Marketing"
        else:
            department = "General"
        
        # Simple acceptance
        status = "Accepted" if total_skills >= 3 else "Rejected"
        
        # Basic ranking
        ranking_score = min(total_skills * 15, 100)
        
        return status, department, ranking_score

# Test the classifier
if __name__ == "__main__":
    print("🧪 Testing Resume Classifier...")
    
    classifier = ResumeClassifier()
    
    # Test with sample data
    test_text = "Python developer with 5 years experience in web development and machine learning. Bachelor's degree in Computer Science."
    test_skills = {
        'Programming': ['python', 'java'],
        'Web Development': ['html', 'css', 'javascript'],
        'Database': ['sql', 'mongodb'],
        'AI/ML': ['machine learning']
    }
    test_experience = {'total_years': 5}
    
    status, department, score = classifier.classify_resume(test_text, test_skills)
    fraud_score, findings = classifier.detect_fraud(test_text, test_skills, test_experience)
    
    print(f"✅ Classification: {status} | Department: {department} | Score: {score}")
    print(f"✅ Fraud Detection: {fraud_score}%")
    print("Findings:", findings)