import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from collections import Counter

class FeatureExtractor:
    def __init__(self):
        self.tfidf_vectorizer = TfidfVectorizer(
            max_features=1000, 
            stop_words='english',
            ngram_range=(1, 2)  # Include bigrams
        )
        self.count_vectorizer = CountVectorizer(
            max_features=500,
            stop_words='english'
        )
    
    def extract_text_features(self, text):
        """Extract comprehensive text-based features"""
        features = {}
        
        if not text:
            return self._get_empty_features()
        
        try:
            # Basic text statistics
            features['char_count'] = len(text)
            features['word_count'] = len(text.split())
            features['sentence_count'] = len(re.split(r'[.!?]+', text))
            
            # Word and character statistics
            words = text.split()
            if words:
                features['avg_word_length'] = sum(len(word) for word in words) / len(words)
                features['max_word_length'] = max(len(word) for word in words)
                features['unique_word_ratio'] = len(set(words)) / len(words)
            else:
                features['avg_word_length'] = 0
                features['max_word_length'] = 0
                features['unique_word_ratio'] = 0
            
            # Extract numeric features
            numbers = re.findall(r'\b\d+\b', text)
            features['number_count'] = len(numbers)
            if numbers:
                features['avg_number'] = sum(map(int, numbers)) / len(numbers)
            else:
                features['avg_number'] = 0
            
            # Contact information features
            emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
            features['email_count'] = len(emails)
            
            phone_patterns = [
                r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',
                r'\+?[\d\s-]{10,}'
            ]
            phone_count = 0
            for pattern in phone_patterns:
                phone_count += len(re.findall(pattern, text))
            features['phone_count'] = phone_count
            
            # URL features
            urls = re.findall(r'http\S+|www\S+|https\S+', text)
            features['url_count'] = len(urls)
            
            # Section detection features
            section_keywords = {
                'experience': ['experience', 'work', 'employment', 'career'],
                'education': ['education', 'academic', 'degree', 'university'],
                'skills': ['skills', 'technical', 'programming', 'languages'],
                'projects': ['projects', 'portfolio', 'work samples'],
                'certifications': ['certifications', 'certificate', 'licenses']
            }
            
            text_lower = text.lower()
            for section, keywords in section_keywords.items():
                features[f'{section}_section'] = any(keyword in text_lower for keyword in keywords)
            
            # Keyword density features
            technical_keywords = ['python', 'java', 'javascript', 'sql', 'aws', 'docker', 'machine learning']
            business_keywords = ['management', 'leadership', 'strategy', 'business', 'marketing']
            
            features['technical_keyword_density'] = sum(text_lower.count(keyword) for keyword in technical_keywords) / max(1, features['word_count'])
            features['business_keyword_density'] = sum(text_lower.count(keyword) for keyword in business_keywords) / max(1, features['word_count'])
            
            return features
            
        except Exception as e:
            print(f"Error extracting text features: {e}")
            return self._get_empty_features()
    
    def extract_skill_features(self, skills_dict):
        """Extract features from skills dictionary"""
        features = {}
        
        try:
            if not skills_dict:
                return self._get_empty_skill_features()
            
            total_skills = sum(len(skills) for skills in skills_dict.values())
            features['total_skills'] = total_skills
            
            # Count skills by category
            skill_categories = {
                'technical': ['Programming', 'Web Development', 'Database', 'Cloud & DevOps', 'AI/ML', 'Data Science', 'Tools & Platforms'],
                'soft': ['Soft Skills'],
                'other': []  # Any other categories
            }
            
            technical_skills = 0
            soft_skills = 0
            other_skills = 0
            
            for category, skills in skills_dict.items():
                category_skill_count = len(skills)
                features[f'{category.lower().replace(" & ", "_").replace(" ", "_")}_count'] = category_skill_count
                
                if category in skill_categories['technical']:
                    technical_skills += category_skill_count
                elif category in skill_categories['soft']:
                    soft_skills += category_skill_count
                else:
                    other_skills += category_skill_count
            
            features['technical_skills_count'] = technical_skills
            features['soft_skills_count'] = soft_skills
            features['other_skills_count'] = other_skills
            
            # Ratios
            if total_skills > 0:
                features['technical_ratio'] = technical_skills / total_skills
                features['soft_ratio'] = soft_skills / total_skills
                features['skill_diversity'] = len(skills_dict) / total_skills
            else:
                features['technical_ratio'] = 0
                features['soft_ratio'] = 0
                features['skill_diversity'] = 0
            
            # Skill depth (average skills per category)
            features['avg_skills_per_category'] = total_skills / max(1, len(skills_dict))
            
            return features
            
        except Exception as e:
            print(f"Error extracting skill features: {e}")
            return self._get_empty_skill_features()
    
    def extract_experience_features(self, experience_data):
        """Extract features from experience data"""
        features = {}
        
        try:
            features['experience_years'] = experience_data.get('total_years', 0)
            features['position_count'] = len(experience_data.get('positions', []))
            features['company_count'] = len(experience_data.get('companies', []))
            
            # Experience level categorization
            exp_years = features['experience_years']
            if exp_years >= 10:
                features['experience_level'] = 'senior'
            elif exp_years >= 5:
                features['experience_level'] = 'mid'
            elif exp_years >= 2:
                features['experience_level'] = 'junior'
            else:
                features['experience_level'] = 'entry'
            
            # Career progression indicator
            positions = experience_data.get('positions', [])
            senior_keywords = ['senior', 'lead', 'principal', 'manager', 'director', 'head']
            junior_keywords = ['junior', 'associate', 'assistant', 'intern']
            
            senior_positions = sum(1 for pos in positions if any(keyword in pos.lower() for keyword in senior_keywords))
            junior_positions = sum(1 for pos in positions if any(keyword in pos.lower() for keyword in junior_keywords))
            
            features['senior_position_ratio'] = senior_positions / max(1, len(positions))
            features['junior_position_ratio'] = junior_positions / max(1, len(positions))
            
            return features
            
        except Exception as e:
            print(f"Error extracting experience features: {e}")
            return {'experience_years': 0, 'position_count': 0, 'company_count': 0, 'experience_level': 'unknown'}
    
    def extract_education_features(self, education_data):
        """Extract features from education data"""
        features = {}
        
        try:
            highest_degree = education_data.get('highest_degree', 'Unknown')
            degree_scores = {
                'PhD': 4,
                'Masters': 3,
                'Bachelors': 2,
                'Diploma': 1,
                'Unknown': 0
            }
            
            features['education_score'] = degree_scores.get(highest_degree, 0)
            features['degree_count'] = len(education_data.get('degrees', []))
            features['institution_count'] = len(education_data.get('institutions', []))
            features['has_higher_education'] = features['education_score'] >= 2
            
            return features
            
        except Exception as e:
            print(f"Error extracting education features: {e}")
            return {'education_score': 0, 'degree_count': 0, 'institution_count': 0, 'has_higher_education': False}
    
    def get_tfidf_features(self, texts):
        """Get TF-IDF features for multiple texts"""
        try:
            if not texts or len(texts) == 0:
                return None
            
            # Ensure all texts are strings
            texts = [str(text) for text in texts if text]
            
            if len(texts) == 0:
                return None
            
            return self.tfidf_vectorizer.fit_transform(texts)
            
        except Exception as e:
            print(f"Error generating TF-IDF features: {e}")
            return None
    
    def get_count_features(self, texts):
        """Get count vectorizer features"""
        try:
            if not texts or len(texts) == 0:
                return None
            
            texts = [str(text) for text in texts if text]
            
            if len(texts) == 0:
                return None
            
            return self.count_vectorizer.fit_transform(texts)
            
        except Exception as e:
            print(f"Error generating count features: {e}")
            return None
    
    def _get_empty_features(self):
        """Return empty feature set"""
        return {
            'char_count': 0, 'word_count': 0, 'sentence_count': 0,
            'avg_word_length': 0, 'max_word_length': 0, 'unique_word_ratio': 0,
            'number_count': 0, 'avg_number': 0, 'email_count': 0,
            'phone_count': 0, 'url_count': 0,
            'technical_keyword_density': 0, 'business_keyword_density': 0
        }
    
    def _get_empty_skill_features(self):
        """Return empty skill feature set"""
        return {
            'total_skills': 0, 'technical_skills_count': 0,
            'soft_skills_count': 0, 'other_skills_count': 0,
            'technical_ratio': 0, 'soft_ratio': 0, 'skill_diversity': 0,
            'avg_skills_per_category': 0
        }

# Test the feature extractor
if __name__ == "__main__":
    print("🧪 Testing Feature Extractor...")
    
    extractor = FeatureExtractor()
    
    # Test with sample data
    sample_text = "Python developer with 5 years experience. Skills: Python, Django, React."
    sample_skills = {
        'Programming': ['python', 'javascript'],
        'Web Development': ['django', 'react']
    }
    sample_experience = {'total_years': 5, 'positions': ['Developer'], 'companies': ['Tech Co']}
    sample_education = {'highest_degree': 'Bachelors', 'degrees': ['Bachelors'], 'institutions': ['University']}
    
    text_features = extractor.extract_text_features(sample_text)
    skill_features = extractor.extract_skill_features(sample_skills)
    exp_features = extractor.extract_experience_features(sample_experience)
    edu_features = extractor.extract_education_features(sample_education)
    
    print("✅ Feature Extractor tested successfully!")
    print(f"Text Features: {len(text_features)}")
    print(f"Skill Features: {len(skill_features)}")
    print(f"Experience Features: {len(exp_features)}")
    print(f"Education Features: {len(edu_features)}")