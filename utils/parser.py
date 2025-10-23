import PyPDF2
from pdfminer.high_level import extract_text as pdfminer_extract
from docx import Document
import re
from datetime import datetime

class ResumeParser:
    def extract_text(self, file_path, file_ext):
        """Extract text from PDF or DOCX files with fallback methods"""
        try:
            if file_ext == '.pdf':
                # Try pdfminer first (better for some PDFs)
                try:
                    text = pdfminer_extract(file_path)
                    if text and len(text.strip()) > 100:
                        return text
                except Exception as e:
                    print(f"pdfminer failed: {e}, trying PyPDF2...")
                
                # Fallback to PyPDF2
                try:
                    with open(file_path, 'rb') as file:
                        reader = PyPDF2.PdfReader(file)
                        text = ""
                        for page in reader.pages:
                            page_text = page.extract_text()
                            if page_text:
                                text += page_text + "\n"
                        return text
                except Exception as e:
                    print(f"PyPDF2 failed: {e}")
                    return f"Error reading PDF: {str(e)}"
                    
            elif file_ext == '.docx':
                try:
                    doc = Document(file_path)
                    text = ""
                    for paragraph in doc.paragraphs:
                        if paragraph.text:
                            text += paragraph.text + "\n"
                    return text
                except Exception as e:
                    return f"Error reading DOCX: {str(e)}"
            else:
                return f"Unsupported file type: {file_ext}"
                
        except Exception as e:
            return f"Error extracting text: {str(e)}"
    
    def parse_personal_info(self, text):
        """Extract personal information from resume text"""
        info = {'name': '', 'email': '', 'phone': '', 'location': ''}
        
        if not text:
            return info
        
        # Extract email
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        if emails:
            info['email'] = emails[0]
        
        # Extract phone numbers (international format support)
        phone_patterns = [
            r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',  # US format
            r'\+?[\d\s-]{10,}',  # International format
            r'\(\d{3}\)\s*\d{3}[-.\s]?\d{4}'  # (123) 456-7890
        ]
        
        for pattern in phone_patterns:
            phones = re.findall(pattern, text)
            if phones:
                # Take the first phone number found
                phone = phones[0]
                if isinstance(phone, tuple):
                    phone = ''.join(phone)
                info['phone'] = phone.strip()
                break
        
        # Extract name (improved heuristic)
        lines = text.split('\n')
        for i, line in enumerate(lines[:15]):  # Check first 15 lines
            line = line.strip()
            if (len(line) > 2 and len(line) < 50 and 
                not any(char.isdigit() for char in line) and
                '@' not in line and 
                'http' not in line.lower() and
                not line.lower().startswith('experience') and
                not line.lower().startswith('education') and
                not line.lower().startswith('skills') and
                len(line.split()) >= 2 and len(line.split()) <= 4):
                
                # Additional check: next line often contains title
                if i + 1 < len(lines) and len(lines[i + 1].strip()) > 0:
                    info['name'] = line
                    break
        
        # Extract location (simple keyword matching)
        location_keywords = [
            'new york', 'london', 'san francisco', 'chicago', 'austin', 
            'remote', 'hybrid', 'boston', 'seattle', 'los angeles',
            'toronto', 'sydney', 'berlin', 'paris', 'tokyo'
        ]
        
        text_lower = text.lower()
        for location in location_keywords:
            if location in text_lower:
                info['location'] = location.title()
                break
        
        return info
    
    def extract_skills(self, text):
        """Extract skills from resume text using comprehensive skill database"""
        if not text:
            return {}
        
        skills_db = {
            'Programming': [
                'python', 'java', 'javascript', 'c++', 'c#', 'ruby', 'php', 'swift', 
                'kotlin', 'go', 'rust', 'typescript', 'scala', 'r', 'matlab'
            ],
            'Web Development': [
                'html', 'css', 'react', 'angular', 'vue', 'django', 'flask', 
                'node.js', 'express', 'spring', 'laravel', 'bootstrap', 'jquery'
            ],
            'Database': [
                'sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'oracle', 
                'sqlite', 'cassandra', 'dynamodb', 'firebase'
            ],
            'Cloud & DevOps': [
                'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 
                'terraform', 'ansible', 'git', 'ci/cd', 'github', 'gitlab'
            ],
            'AI/ML': [
                'machine learning', 'deep learning', 'tensorflow', 'pytorch', 
                'nlp', 'computer vision', 'neural networks', 'scikit-learn',
                'opencv', 'keras'
            ],
            'Data Science': [
                'pandas', 'numpy', 'r', 'matplotlib', 'seaborn', 'tableau', 
                'power bi', 'excel', 'statistics', 'analytics'
            ],
            'Soft Skills': [
                'leadership', 'communication', 'teamwork', 'problem solving', 
                'project management', 'agile', 'scrum', 'time management',
                'critical thinking', 'creativity', 'adaptability'
            ],
            'Tools & Platforms': [
                'jira', 'confluence', 'slack', 'teams', 'zoom', 'notion',
                'trello', 'asana', 'word', 'excel', 'powerpoint', 'outlook'
            ]
        }
        
        found_skills = {}
        text_lower = text.lower()
        
        for category, skills in skills_db.items():
            found_skills[category] = []
            for skill in skills:
                # Use word boundaries to avoid partial matches
                pattern = r'\b' + re.escape(skill) + r'\b'
                if re.search(pattern, text_lower, re.IGNORECASE):
                    found_skills[category].append(skill)
        
        return found_skills
    
    def extract_experience(self, text):
        """Extract work experience information"""
        experience = {
            'total_years': 0,
            'positions': [],
            'companies': []
        }
        
        if not text:
            return experience
        
        # Extract years from text
        year_pattern = r'\b(19|20)\d{2}\b'
        years = [int(year) for year in re.findall(year_pattern, text)]
        
        if years:
            # Calculate approximate experience (max year - min year)
            if len(years) >= 2:
                experience['total_years'] = max(years) - min(years)
            else:
                experience['total_years'] = 0
            
            # Simple heuristic: if only one year found, assume 1+ years
            if len(years) == 1 and years[0] <= datetime.now().year:
                experience['total_years'] = datetime.now().year - years[0]
        
        # Extract job titles and companies (basic pattern matching)
        job_patterns = [
            r'(?i)(.*?)\s*(?:at|@|\|)\s*(.*?)(?:\n|$)',
            r'(?i)(.*?)\s*-\s*(.*?)(?:\n|$)',
            r'(?i)(senior|junior|lead)?\s*([a-z]+)\s*(?:developer|engineer|analyst|manager)'
        ]
        
        for pattern in job_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                if len(match) == 2:
                    position, company = match
                    position = position.strip()
                    company = company.strip()
                    
                    if (len(position) > 2 and len(company) > 2 and
                        not any(word in position.lower() for word in ['email', 'phone', 'http']) and
                        not any(word in company.lower() for word in ['email', 'phone', 'http'])):
                        
                        if position not in experience['positions']:
                            experience['positions'].append(position)
                        if company not in experience['companies']:
                            experience['companies'].append(company)
        
        return experience
    
    def extract_education(self, text):
        """Extract education information"""
        education = {
            'highest_degree': 'Unknown',
            'degrees': [],
            'institutions': []
        }
        
        if not text:
            return education
        
        text_lower = text.lower()
        
        # Degree patterns with institutions
        degree_patterns = [
            (r'\b(ph\.?d|doctorate)\b', 'PhD'),
            (r'\b(m\.?s|m\.?a|master\'?s?|mba)\b', 'Masters'),
            (r'\b(b\.?s|b\.?a|bachelor\'?s?|undergraduate)\b', 'Bachelors'),
            (r'\b(associate|diploma|certificate)\b', 'Diploma')
        ]
        
        found_degrees = []
        for pattern, degree in degree_patterns:
            if re.search(pattern, text_lower):
                found_degrees.append(degree)
        
        education['degrees'] = found_degrees
        
        # Determine highest degree
        if 'PhD' in found_degrees:
            education['highest_degree'] = 'PhD'
        elif 'Masters' in found_degrees:
            education['highest_degree'] = 'Masters'
        elif 'Bachelors' in found_degrees:
            education['highest_degree'] = 'Bachelors'
        elif 'Diploma' in found_degrees:
            education['highest_degree'] = 'Diploma'
        
        # Extract institution names (simple pattern)
        institution_keywords = ['university', 'college', 'institute', 'school']
        lines = text.split('\n')
        for line in lines:
            line_lower = line.lower()
            if any(keyword in line_lower for keyword in institution_keywords):
                # Check if this line likely contains an institution name
                if (len(line.strip()) > 5 and len(line.strip()) < 100 and
                    not any(word in line_lower for word in ['experience', 'skills', 'projects'])):
                    education['institutions'].append(line.strip())
        
        return education

# Test the parser
if __name__ == "__main__":
    print("🧪 Testing Resume Parser...")
    
    parser = ResumeParser()
    
    # Test with sample resume text
    sample_resume = """
    JOHN DOE
    Senior Software Engineer
    Email: john.doe@email.com
    Phone: (555) 123-4567
    Location: San Francisco, CA
    
    EXPERIENCE:
    Senior Python Developer - Tech Solutions Inc. (2020-2023)
    • Developed web applications using Python and Django
    • Led a team of 5 developers
    
    Python Developer - Startup Co. (2018-2020)
    • Built REST APIs and microservices
    
    EDUCATION:
    Bachelor of Science in Computer Science - State University (2014-2018)
    
    SKILLS:
    Programming: Python, Java, JavaScript
    Web: HTML, CSS, React, Django
    Database: SQL, MongoDB
    Tools: Git, Docker, AWS
    """
    
    personal_info = parser.parse_personal_info(sample_resume)
    skills = parser.extract_skills(sample_resume)
    experience = parser.extract_experience(sample_resume)
    education = parser.extract_education(sample_resume)
    
    print("✅ Parser tested successfully!")
    print(f"Name: {personal_info['name']}")
    print(f"Email: {personal_info['email']}")
    print(f"Phone: {personal_info['phone']}")
    print(f"Skills Categories: {len(skills)}")
    print(f"Experience: {experience['total_years']} years")
    print(f"Highest Degree: {education['highest_degree']}")