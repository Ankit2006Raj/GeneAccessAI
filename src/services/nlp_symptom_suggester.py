"""
NLP-based Symptom Auto-Suggestion System
Suggests related symptoms based on user input
"""
import re
from difflib import get_close_matches

class SymptomSuggester:
    def __init__(self):
        # Comprehensive symptom database with related symptoms
        self.symptom_database = {
            # Joint and Musculoskeletal
            'joint pain': ['stiffness', 'swelling', 'mobility difficulty', 'redness', 'warmth', 'limited range of motion'],
            'muscle pain': ['weakness', 'cramping', 'stiffness', 'tenderness', 'fatigue'],
            'muscle weakness': ['fatigue', 'difficulty walking', 'difficulty lifting', 'muscle atrophy', 'tremors'],
            'back pain': ['stiffness', 'limited mobility', 'numbness', 'tingling', 'radiating pain'],
            'stiffness': ['joint pain', 'limited mobility', 'morning stiffness', 'difficulty moving'],
            
            # Respiratory
            'breathing difficulty': ['shortness of breath', 'wheezing', 'chest tightness', 'rapid breathing', 'coughing'],
            'shortness of breath': ['fatigue', 'chest pain', 'dizziness', 'rapid heartbeat', 'anxiety'],
            'coughing': ['chest pain', 'wheezing', 'mucus production', 'sore throat', 'fatigue'],
            'wheezing': ['breathing difficulty', 'chest tightness', 'coughing', 'rapid breathing'],
            
            # Cardiovascular
            'chest pain': ['shortness of breath', 'rapid heartbeat', 'dizziness', 'sweating', 'nausea'],
            'rapid heartbeat': ['palpitations', 'dizziness', 'shortness of breath', 'chest discomfort', 'anxiety'],
            'palpitations': ['rapid heartbeat', 'chest discomfort', 'dizziness', 'shortness of breath'],
            
            # Neurological
            'headache': ['dizziness', 'nausea', 'sensitivity to light', 'vision problems', 'neck pain'],
            'dizziness': ['balance problems', 'nausea', 'lightheadedness', 'fainting', 'blurred vision'],
            'numbness': ['tingling', 'weakness', 'loss of sensation', 'difficulty moving'],
            'tingling': ['numbness', 'burning sensation', 'weakness', 'pins and needles'],
            'tremors': ['shaking', 'muscle weakness', 'difficulty with fine motor skills', 'balance problems'],
            'seizures': ['loss of consciousness', 'muscle spasms', 'confusion', 'staring spells'],
            
            # Cognitive and Developmental
            'memory problems': ['confusion', 'difficulty concentrating', 'disorientation', 'forgetfulness'],
            'confusion': ['disorientation', 'memory problems', 'difficulty thinking', 'agitation'],
            'developmental delay': ['speech delay', 'motor skill delay', 'learning difficulties', 'social difficulties'],
            'learning difficulties': ['memory problems', 'attention problems', 'reading difficulties', 'writing difficulties'],
            
            # Vision and Hearing
            'vision problems': ['blurred vision', 'double vision', 'sensitivity to light', 'eye pain', 'difficulty seeing at night'],
            'blurred vision': ['eye strain', 'headache', 'dizziness', 'difficulty focusing'],
            'hearing loss': ['ringing in ears', 'difficulty understanding speech', 'ear pain', 'balance problems'],
            'ringing in ears': ['hearing loss', 'dizziness', 'ear fullness', 'sensitivity to sound'],
            
            # Gastrointestinal
            'nausea': ['vomiting', 'loss of appetite', 'abdominal pain', 'dizziness', 'weakness'],
            'vomiting': ['nausea', 'dehydration', 'abdominal pain', 'weakness', 'dizziness'],
            'abdominal pain': ['nausea', 'bloating', 'cramping', 'diarrhea', 'constipation'],
            'diarrhea': ['abdominal pain', 'cramping', 'dehydration', 'urgency', 'bloating'],
            
            # Bleeding and Hematological
            'unusual bleeding': ['easy bruising', 'nosebleeds', 'bleeding gums', 'prolonged bleeding', 'blood in urine'],
            'easy bruising': ['unusual bleeding', 'petechiae', 'bleeding gums', 'fatigue'],
            'nosebleeds': ['unusual bleeding', 'easy bruising', 'dry nasal passages', 'sinus problems'],
            'bleeding gums': ['easy bruising', 'unusual bleeding', 'swollen gums', 'tooth sensitivity'],
            
            # Fatigue and General
            'fatigue': ['weakness', 'exhaustion', 'difficulty concentrating', 'sleepiness', 'low energy'],
            'weakness': ['fatigue', 'muscle weakness', 'dizziness', 'difficulty moving', 'exhaustion'],
            'fever': ['chills', 'sweating', 'body aches', 'fatigue', 'headache'],
            'weight loss': ['loss of appetite', 'fatigue', 'weakness', 'nausea'],
            
            # Skin
            'rash': ['itching', 'redness', 'swelling', 'dry skin', 'blisters'],
            'itching': ['rash', 'dry skin', 'redness', 'irritation', 'hives'],
            'pale skin': ['fatigue', 'weakness', 'dizziness', 'shortness of breath', 'cold hands and feet'],
            
            # Infections
            'frequent infections': ['fever', 'fatigue', 'weakness', 'swollen lymph nodes', 'slow healing'],
            'swollen lymph nodes': ['fever', 'sore throat', 'fatigue', 'night sweats'],
            
            # Growth and Development
            'growth delay': ['developmental delay', 'short stature', 'delayed puberty', 'weight issues'],
            'delayed puberty': ['growth delay', 'hormonal imbalance', 'lack of secondary sexual characteristics']
        }
        
        # Flatten all symptoms for fuzzy matching
        self.all_symptoms = set()
        for key, values in self.symptom_database.items():
            self.all_symptoms.add(key)
            self.all_symptoms.update(values)
        self.all_symptoms = list(self.all_symptoms)
    
    def suggest_symptoms(self, user_input, max_suggestions=5):
        """
        Suggest related symptoms based on user input
        Returns a list of suggested symptoms
        """
        user_input = user_input.lower().strip()
        
        if not user_input:
            return []
        
        suggestions = set()
        
        # Direct match in database
        if user_input in self.symptom_database:
            suggestions.update(self.symptom_database[user_input][:max_suggestions])
        
        # Partial match
        for symptom, related in self.symptom_database.items():
            if user_input in symptom or symptom in user_input:
                suggestions.update(related[:max_suggestions])
        
        # Fuzzy matching for typos
        close_matches = get_close_matches(user_input, self.all_symptoms, n=3, cutoff=0.6)
        for match in close_matches:
            if match in self.symptom_database:
                suggestions.update(self.symptom_database[match][:max_suggestions])
        
        # Limit results
        return list(suggestions)[:max_suggestions]
    
    def get_symptom_category(self, symptom):
        """Categorize symptom into body system"""
        symptom = symptom.lower()
        
        categories = {
            'Musculoskeletal': ['joint', 'muscle', 'bone', 'back', 'stiffness', 'mobility'],
            'Respiratory': ['breathing', 'breath', 'cough', 'wheez', 'lung', 'chest'],
            'Cardiovascular': ['heart', 'chest pain', 'palpitation', 'blood pressure'],
            'Neurological': ['headache', 'dizz', 'numb', 'tingl', 'tremor', 'seizure', 'memory', 'confusion'],
            'Vision/Hearing': ['vision', 'eye', 'hearing', 'ear', 'blind', 'deaf'],
            'Gastrointestinal': ['nausea', 'vomit', 'abdominal', 'stomach', 'diarrhea', 'constipation'],
            'Hematological': ['bleeding', 'bruising', 'blood', 'anemia'],
            'General': ['fatigue', 'weakness', 'fever', 'weight', 'tired'],
            'Dermatological': ['skin', 'rash', 'itch', 'pale'],
            'Immune': ['infection', 'lymph', 'swollen']
        }
        
        for category, keywords in categories.items():
            for keyword in keywords:
                if keyword in symptom:
                    return category
        
        return 'Other'
    
    def get_symptom_severity_questions(self, symptom):
        """Generate follow-up questions for symptom severity"""
        return [
            f"How long have you been experiencing {symptom}?",
            f"On a scale of 1-10, how severe is the {symptom}?",
            f"Does the {symptom} interfere with daily activities?",
            f"Have you noticed any triggers for the {symptom}?"
        ]
    
    def search_symptoms(self, query, limit=10):
        """Search symptoms database"""
        query = query.lower()
        results = []
        
        for symptom in self.all_symptoms:
            if query in symptom:
                results.append({
                    'symptom': symptom,
                    'category': self.get_symptom_category(symptom),
                    'related': self.symptom_database.get(symptom, [])[:3]
                })
        
        return results[:limit]

# Initialize global instance
symptom_suggester = SymptomSuggester()

if __name__ == '__main__':
    # Test the suggester
    suggester = SymptomSuggester()
    
    test_inputs = ['joint pain', 'breathing', 'fatigue', 'headache']
    
    for test in test_inputs:
        suggestions = suggester.suggest_symptoms(test)
        print(f"\nInput: '{test}'")
        print(f"Suggestions: {suggestions}")
        print(f"Category: {suggester.get_symptom_category(test)}")
