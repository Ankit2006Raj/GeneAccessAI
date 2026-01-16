"""
Utility functions for GeneAccessAI
"""

import re
from datetime import datetime
from functools import wraps
from flask import session, redirect, url_for, flash

def login_required(f):
    """Decorator to require login for routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def validate_password(password):
    """
    Validate password strength
    Returns: (bool, str) - (is_valid, message)
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter"
    
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter"
    
    if not re.search(r"\d", password):
        return False, "Password must contain at least one number"
    
    return True, "Password is valid"

def validate_email(email):
    """
    Validate email format
    Returns: bool
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def format_datetime(dt):
    """Format datetime for display"""
    if isinstance(dt, str):
        dt = datetime.fromisoformat(dt)
    return dt.strftime('%B %d, %Y at %I:%M %p')

def calculate_risk_level(risk_score):
    """Calculate risk level from score"""
    if risk_score < 30:
        return 'Low', 'success'
    elif risk_score < 60:
        return 'Moderate', 'warning'
    else:
        return 'High', 'danger'

def sanitize_input(text):
    """Sanitize user input"""
    if not text:
        return ""
    # Remove potentially dangerous characters
    text = re.sub(r'[<>\"\'&]', '', text)
    return text.strip()

def generate_report_filename(assessment_id, username):
    """Generate unique report filename"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    safe_username = re.sub(r'[^a-zA-Z0-9]', '_', username)
    return f"genetic_report_{safe_username}_{assessment_id}_{timestamp}.pdf"

def parse_symptoms(symptom_text):
    """Parse symptom text into list"""
    if not symptom_text:
        return []
    
    # Split by common delimiters
    symptoms = re.split(r'[,;.\n]', symptom_text)
    
    # Clean and filter
    symptoms = [s.strip() for s in symptoms if s.strip()]
    
    return symptoms

def get_disorder_info(disorder_name):
    """Get information about a genetic disorder"""
    disorders_info = {
        'Down Syndrome': {
            'description': 'A genetic disorder caused by the presence of all or part of a third copy of chromosome 21.',
            'prevalence': '1 in 700 births',
            'symptoms': ['Intellectual disability', 'Distinctive facial features', 'Heart defects']
        },
        'Cystic Fibrosis': {
            'description': 'An inherited disorder that causes severe damage to the lungs, digestive system and other organs.',
            'prevalence': '1 in 2,500 to 3,500 births',
            'symptoms': ['Persistent cough', 'Frequent lung infections', 'Poor growth']
        },
        'Sickle Cell Anemia': {
            'description': 'A group of disorders that cause red blood cells to become misshapen and break down.',
            'prevalence': '1 in 365 African American births',
            'symptoms': ['Anemia', 'Pain episodes', 'Swelling of hands and feet']
        },
        'Huntington Disease': {
            'description': 'An inherited condition that causes progressive breakdown of nerve cells in the brain.',
            'prevalence': '1 in 10,000 to 20,000 people',
            'symptoms': ['Movement disorders', 'Cognitive decline', 'Psychiatric problems']
        },
        'Hemophilia': {
            'description': 'A rare disorder in which blood doesn\'t clot normally due to lack of clotting factors.',
            'prevalence': '1 in 5,000 male births',
            'symptoms': ['Excessive bleeding', 'Easy bruising', 'Joint pain and swelling']
        },
        'Thalassemia': {
            'description': 'An inherited blood disorder characterized by less hemoglobin and fewer red blood cells.',
            'prevalence': 'Varies by region',
            'symptoms': ['Fatigue', 'Weakness', 'Pale or yellowish skin']
        },
        'Muscular Dystrophy': {
            'description': 'A group of diseases that cause progressive weakness and loss of muscle mass.',
            'prevalence': 'Varies by type',
            'symptoms': ['Progressive muscle weakness', 'Difficulty walking', 'Frequent falls']
        },
        'Low Risk': {
            'description': 'No significant genetic disorder risk detected based on current assessment.',
            'prevalence': 'N/A',
            'symptoms': []
        }
    }
    
    return disorders_info.get(disorder_name, {
        'description': 'Information not available',
        'prevalence': 'Unknown',
        'symptoms': []
    })

class RateLimiter:
    """Simple rate limiter for API endpoints"""
    def __init__(self):
        self.requests = {}
    
    def is_allowed(self, key, max_requests=10, window=60):
        """Check if request is allowed"""
        now = datetime.now().timestamp()
        
        if key not in self.requests:
            self.requests[key] = []
        
        # Remove old requests outside the window
        self.requests[key] = [
            req_time for req_time in self.requests[key]
            if now - req_time < window
        ]
        
        # Check if limit exceeded
        if len(self.requests[key]) >= max_requests:
            return False
        
        # Add current request
        self.requests[key].append(now)
        return True

# Global rate limiter instance
rate_limiter = RateLimiter()
