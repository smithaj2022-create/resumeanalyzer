import numpy as np
from datetime import datetime

class ResumeRanker:
    def __init__(self):
        self.department_weights = {
            'IT': {'technical_skills': 0.4, 'experience': 0.3, 'education': 0.2, 'certifications': 0.1},
            'HR': {'experience': 0.4, 'soft_skills': 0.3, 'education': 0.2, 'certifications': 0.1},
            'Finance': {'experience': 0.5, 'education': 0.3, 'certifications': 0.2},
            'Marketing': {'experience': 0.4, 'soft_skills': 0.3, 'education': 0.2, 'portfolio': 0.1},
            'Engineering': {'technical_skills': 0.5, 'experience': 0.3, 'education': 0.2},
            'Operations': {'experience': 0.5, 'soft_skills': 0.3, 'education': 0.2},
            'Sales': {'experience': 0.4, 'soft_skills': 0.4, 'education': 0.2},
            'General': {'experience': 0.4, 'skills': 0.4, 'education': 0.2}
        }
    
    def calculate_department_score(self, candidate, department):
        """Calculate score for a candidate in a specific department"""
        if department not in self.department_weights:
            department = 'General'
        
        weights = self.department_weights[department]
        score = 0
        
        # Experience component
        experience_years = candidate.get('experience_years', 0)
        score += min(experience_years / 10.0, 1.0) * weights.get('experience', 0.3) * 100
        
        # Skills component
        skills = candidate.get('skills', {})
        total_skills = sum(len(skills[cat]) for cat in skills)
        
        if 'technical_skills' in weights:
            tech_skills = len(skills.get('Programming', [])) + len(skills.get('AI/ML', [])) + len(skills.get('Web Development', []))
            score += min(tech_skills / 10.0, 1.0) * weights['technical_skills'] * 100
        elif 'soft_skills' in weights:
            soft_skills = len(skills.get('Soft Skills', []))
            score += min(soft_skills / 5.0, 1.0) * weights['soft_skills'] * 100
        else:
            score += min(total_skills / 15.0, 1.0) * weights.get('skills', 0.3) * 100
        
        # Education component
        education_level = candidate.get('education_level', 'Unknown')
        education_score = 0
        if education_level == 'PhD':
            education_score = 1.0
        elif education_level == 'Masters':
            education_score = 0.8
        elif education_level == 'Bachelors':
            education_score = 0.6
        elif education_level == 'Diploma':
            education_score = 0.4
        
        score += education_score * weights.get('education', 0.2) * 100
        
        return min(score, 100)
    
    def rank_candidates_by_department(self, candidates, department, top_n=5):
        """Rank candidates within a specific department"""
        dept_candidates = [c for c in candidates if c.get('department') == department]
        
        # Calculate department-specific scores
        for candidate in dept_candidates:
            candidate['department_score'] = self.calculate_department_score(candidate, department)
        
        # Sort by department score (primary) and overall ranking score (secondary)
        ranked_candidates = sorted(
            dept_candidates, 
            key=lambda x: (x.get('department_score', 0), x.get('ranking_score', 0)), 
            reverse=True
        )
        
        return ranked_candidates[:top_n]
    
    def get_top_candidates_all_departments(self, candidates, top_n=5):
        """Get top candidates from all departments"""
        departments = set(candidate.get('department', 'General') for candidate in candidates)
        top_candidates = {}
        
        for department in departments:
            top_candidates[department] = self.rank_candidates_by_department(candidates, department, top_n)
        
        return top_candidates
    
    def get_overall_ranking(self, candidates, top_n=10):
        """Get overall ranking across all departments"""
        # Calculate overall scores considering department fit
        for candidate in candidates:
            department = candidate.get('department', 'General')
            department_score = self.calculate_department_score(candidate, department)
            ranking_score = candidate.get('ranking_score', 0)
            
            # Combined score: 60% ranking score + 40% department fit
            candidate['overall_score'] = (ranking_score * 0.6) + (department_score * 0.4)
        
        # Sort by overall score
        ranked_candidates = sorted(candidates, key=lambda x: x.get('overall_score', 0), reverse=True)
        
        return ranked_candidates[:top_n]

# Test the ranker
if __name__ == "__main__":
    print("🧪 Testing Resume Ranker...")
    
    ranker = ResumeRanker()
    
    # Test with sample candidates
    test_candidates = [
        {
            'candidate_name': 'John Doe',
            'department': 'IT',
            'ranking_score': 85,
            'experience_years': 5,
            'education_level': 'Bachelors',
            'skills': {
                'Programming': ['python', 'java'],
                'Web Development': ['html', 'css', 'javascript'],
                'Database': ['sql']
            }
        },
        {
            'candidate_name': 'Jane Smith',
            'department': 'HR',
            'ranking_score': 78,
            'experience_years': 3,
            'education_level': 'Masters',
            'skills': {
                'Soft Skills': ['communication', 'leadership', 'teamwork']
            }
        }
    ]
    
    top_by_dept = ranker.get_top_candidates_all_departments(test_candidates)
    overall_ranking = ranker.get_overall_ranking(test_candidates)
    
    print("✅ Ranker tested successfully!")
    print(f"Departments: {list(top_by_dept.keys())}")
    print(f"Overall top: {len(overall_ranking)} candidates")