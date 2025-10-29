"""
Department Configuration Module
Defines criteria and requirements for each department
"""

DEPARTMENTS = {
    'Software Engineering': {
        'name': 'Software Engineering',
        'required_skills': [
            'Python', 'Java', 'JavaScript', 'C++', 'SQL', 'Git',
            'React', 'Node.js', 'Django', 'Flask', 'Spring Boot',
            'API', 'REST', 'Database', 'OOP', 'Data Structures',
            'Algorithms', 'Cloud', 'AWS', 'Docker', 'Kubernetes'
        ],
        'min_experience': 2.0,
        'required_education': ['B.Tech', 'B.E.', 'MCA', 'M.Tech', 'Computer Science', 'IT', 'Software'],
        'weights': {
            'skill_match': 50,
            'experience': 20,
            'education': 15,
            'projects_certs': 15
        },
        'min_score': 70
    },
    'Data Science': {
        'name': 'Data Science',
        'required_skills': [
            'Python', 'R', 'Machine Learning', 'Deep Learning', 'Statistics',
            'TensorFlow', 'PyTorch', 'Scikit-learn', 'Pandas', 'NumPy',
            'Data Analysis', 'SQL', 'Visualization', 'Tableau', 'Power BI',
            'NLP', 'Computer Vision', 'Neural Networks', 'AI'
        ],
        'min_experience': 2.0,
        'required_education': ['B.Tech', 'M.Tech', 'Ph.D', 'Statistics', 'Mathematics', 'Computer Science', 'Data Science'],
        'weights': {
            'skill_match': 50,
            'experience': 20,
            'education': 15,
            'projects_certs': 15
        },
        'min_score': 70
    },
    'Marketing': {
        'name': 'Marketing',
        'required_skills': [
            'Digital Marketing', 'SEO', 'SEM', 'Content Marketing', 'Social Media',
            'Google Analytics', 'Facebook Ads', 'Google Ads', 'Email Marketing',
            'Marketing Strategy', 'Brand Management', 'Campaign Management',
            'Market Research', 'Communication', 'Copywriting', 'Analytics'
        ],
        'min_experience': 1.5,
        'required_education': ['MBA', 'BBA', 'Marketing', 'Business', 'Communications'],
        'weights': {
            'skill_match': 45,
            'experience': 25,
            'education': 15,
            'projects_certs': 15
        },
        'min_score': 65
    },
    'Human Resources': {
        'name': 'Human Resources',
        'required_skills': [
            'Recruitment', 'Talent Acquisition', 'HR Management', 'Employee Relations',
            'Performance Management', 'HRIS', 'Payroll', 'Compliance', 'Training',
            'Organizational Development', 'Communication', 'Conflict Resolution',
            'Labor Law', 'Benefits Administration', 'Onboarding'
        ],
        'min_experience': 2.0,
        'required_education': ['MBA', 'BBA', 'HR', 'Human Resources', 'Business', 'Psychology'],
        'weights': {
            'skill_match': 40,
            'experience': 30,
            'education': 15,
            'projects_certs': 15
        },
        'min_score': 65
    },
    'Finance': {
        'name': 'Finance',
        'required_skills': [
            'Financial Analysis', 'Accounting', 'Excel', 'Financial Modeling',
            'Budgeting', 'Forecasting', 'Taxation', 'Audit', 'SAP', 'QuickBooks',
            'Financial Reporting', 'Risk Management', 'Investment Analysis',
            'Cost Analysis', 'Corporate Finance', 'GAAP', 'Financial Planning'
        ],
        'min_experience': 2.0,
        'required_education': ['MBA', 'CA', 'CFA', 'Finance', 'Accounting', 'Commerce', 'B.Com', 'M.Com'],
        'weights': {
            'skill_match': 45,
            'experience': 25,
            'education': 20,
            'projects_certs': 10
        },
        'min_score': 70
    },
    'Product Management': {
        'name': 'Product Management',
        'required_skills': [
            'Product Strategy', 'Product Development', 'Agile', 'Scrum', 'Roadmap',
            'User Research', 'Market Analysis', 'Stakeholder Management', 'JIRA',
            'Product Analytics', 'Feature Prioritization', 'UX', 'UI', 'A/B Testing',
            'KPI', 'Metrics', 'Communication', 'Leadership'
        ],
        'min_experience': 2.5,
        'required_education': ['MBA', 'B.Tech', 'M.Tech', 'Engineering', 'Business', 'Computer Science'],
        'weights': {
            'skill_match': 45,
            'experience': 25,
            'education': 15,
            'projects_certs': 15
        },
        'min_score': 70
    },
    'DevOps': {
        'name': 'DevOps',
        'required_skills': [
            'Docker', 'Kubernetes', 'Jenkins', 'CI/CD', 'AWS', 'Azure', 'GCP',
            'Terraform', 'Ansible', 'Linux', 'Shell Scripting', 'Python',
            'Git', 'Monitoring', 'Prometheus', 'Grafana', 'Cloud', 'Automation',
            'Infrastructure as Code', 'Security'
        ],
        'min_experience': 2.0,
        'required_education': ['B.Tech', 'B.E.', 'M.Tech', 'Computer Science', 'IT', 'Engineering'],
        'weights': {
            'skill_match': 50,
            'experience': 25,
            'education': 10,
            'projects_certs': 15
        },
        'min_score': 70
    }
}

def get_all_departments():
    """Get list of all available departments"""
    return list(DEPARTMENTS.keys())

def get_department_config(department_name):
    """Get configuration for a specific department"""
    return DEPARTMENTS.get(department_name)

def calculate_skill_match(candidate_skills, required_skills):
    """
    Calculate skill match percentage
    
    Args:
        candidate_skills: List of skills from candidate resume
        required_skills: List of required skills for department
    
    Returns:
        Float: Percentage match (0-100)
    """
    if not candidate_skills or not required_skills:
        return 0.0
    
    # Convert to lowercase for case-insensitive comparison
    candidate_skills_lower = [skill.lower().strip() for skill in candidate_skills]
    required_skills_lower = [skill.lower().strip() for skill in required_skills]
    
    # Count exact matches
    exact_matches = sum(1 for skill in candidate_skills_lower if skill in required_skills_lower)
    
    # Count partial matches (skill contains or is contained in required skill)
    partial_matches = 0
    for c_skill in candidate_skills_lower:
        for r_skill in required_skills_lower:
            if c_skill not in [s for s in candidate_skills_lower if s in required_skills_lower]:
                if c_skill in r_skill or r_skill in c_skill:
                    if len(c_skill) > 2 and len(r_skill) > 2:
                        partial_matches += 0.5
                        break
    
    total_matches = exact_matches + partial_matches
    match_percentage = (total_matches / len(required_skills_lower)) * 100
    
    return min(100.0, match_percentage)

def check_education_match(candidate_education, required_education):
    """
    Check if candidate education matches requirements
    
    Args:
        candidate_education: String containing education details
        required_education: List of required education qualifications
    
    Returns:
        Boolean: True if match found
    """
    if not candidate_education or not required_education:
        return False
    
    education_lower = candidate_education.lower()
    
    for req_edu in required_education:
        if req_edu.lower() in education_lower:
            return True
    
    return False

def calculate_eligibility_score(candidate_data, department_name):
    """
    Calculate overall eligibility score for a candidate
    
    Args:
        candidate_data: Dictionary containing candidate information
        department_name: Name of the department
    
    Returns:
        Dictionary with detailed scoring breakdown
    """
    dept_config = get_department_config(department_name)
    if not dept_config:
        return {
            'total_score': 0,
            'breakdown': {},
            'eligible': False,
            'message': 'Invalid department'
        }
    
    weights = dept_config['weights']
    
    # Calculate skill match
    skill_match_pct = calculate_skill_match(
        candidate_data.get('skills', []),
        dept_config['required_skills']
    )
    skill_score = (skill_match_pct / 100) * weights['skill_match']
    
    # Calculate experience score
    candidate_exp = candidate_data.get('experience_years', 0)
    min_exp = dept_config['min_experience']
    if candidate_exp >= min_exp * 1.5:
        exp_score = weights['experience']
    elif candidate_exp >= min_exp:
        exp_score = weights['experience'] * 0.8
    elif candidate_exp >= min_exp * 0.5:
        exp_score = weights['experience'] * 0.5
    else:
        exp_score = weights['experience'] * 0.2
    
    # Calculate education score
    education_match = check_education_match(
        candidate_data.get('education', ''),
        dept_config['required_education']
    )
    edu_score = weights['education'] if education_match else 0
    
    # Projects/Certifications score (simplified - based on presence)
    has_projects = candidate_data.get('work_experience', '') and len(candidate_data.get('work_experience', '')) > 100
    projects_score = weights['projects_certs'] * 0.7 if has_projects else weights['projects_certs'] * 0.3
    
    # Calculate total
    total_score = skill_score + exp_score + edu_score + projects_score
    
    # Determine eligibility
    eligible = total_score >= dept_config['min_score']
    
    return {
        'total_score': round(total_score, 2),
        'skill_match_percentage': round(skill_match_pct, 2),
        'breakdown': {
            'skill_score': round(skill_score, 2),
            'experience_score': round(exp_score, 2),
            'education_score': round(edu_score, 2),
            'projects_score': round(projects_score, 2)
        },
        'eligible': eligible,
        'min_score_required': dept_config['min_score'],
        'message': 'Eligible for shortlisting' if eligible else f'Score below minimum ({dept_config["min_score"]})'
    }

def get_ai_authenticity_status(ai_score):
    """
    Get AI authenticity status based on AI generated score
    
    Args:
        ai_score: AI generated score (0-100)
    
    Returns:
        String: Status message
    """
    if ai_score >= 70:
        return "AI-Generated"
    elif ai_score >= 40:
        return "Possibly AI-Assisted"
    else:
        return "Human-Written"

def get_final_decision(ai_score, eligibility_result, fraud_score):
    """
    Determine final hiring decision
    
    Args:
        ai_score: AI generated score (0-100)
        eligibility_result: Dictionary from calculate_eligibility_score
        fraud_score: Overall fraud score (0-100)
    
    Returns:
        String: "Shortlisted" or "Rejected" with reason
    """
    ai_status = get_ai_authenticity_status(ai_score)
    
    # Reject if fraud score is too high
    if fraud_score >= 60:
        return "Rejected", "High fraud probability detected"
    
    # Reject if strongly AI-generated
    if ai_status == "AI-Generated":
        return "Rejected", "Resume appears to be AI-generated"
    
    # Check eligibility
    if not eligibility_result['eligible']:
        return "Rejected", eligibility_result['message']
    
    # Accept if all checks pass
    if ai_status in ["Human-Written", "Possibly AI-Assisted"] and eligibility_result['eligible']:
        return "Shortlisted", "Passed all criteria"
    
    return "Rejected", "Did not meet hiring criteria"
