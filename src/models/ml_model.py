import numpy as np
import lightgbm as lgb
import pickle
import os
from sklearn.preprocessing import LabelEncoder

class GeneticRiskPredictor:
    def __init__(self):
        self.model = None
        self.label_encoder = LabelEncoder()
        self.conversation_data = {}
        self.load_or_train_model()
        
    def load_or_train_model(self):
        """Load existing model or train a new one"""
        if os.path.exists('models/genetic_model.pkl'):
            with open('models/genetic_model.pkl', 'rb') as f:
                self.model = pickle.load(f)
        else:
            self.train_model()
    
    def train_model(self):
        """Train LightGBM model with synthetic genetic disorder data"""
        os.makedirs('models', exist_ok=True)
        
        # Synthetic training data (in production, use real medical datasets)
        np.random.seed(42)
        n_samples = 5000
        
        # Features: age, num_symptoms, family_history_count, severity_score
        X_train = np.random.rand(n_samples, 20)
        
        # Labels: genetic disorders
        disorders = ['Down Syndrome', 'Cystic Fibrosis', 'Sickle Cell Anemia', 
                    'Huntington Disease', 'Hemophilia', 'Thalassemia', 
                    'Muscular Dystrophy', 'Low Risk']
        y_train = np.random.choice(range(len(disorders)), n_samples)
        
        # Train LightGBM
        train_data = lgb.Dataset(X_train, label=y_train)
        params = {
            'objective': 'multiclass',
            'num_class': len(disorders),
            'metric': 'multi_logloss',
            'boosting_type': 'gbdt',
            'num_leaves': 31,
            'learning_rate': 0.05,
            'feature_fraction': 0.9
        }
        
        self.model = lgb.train(params, train_data, num_boost_round=100)
        
        # Save model
        with open('models/genetic_model.pkl', 'wb') as f:
            pickle.dump(self.model, f)
        
        self.disorders = disorders
    
    def process_chat_message(self, message, state):
        """Process chatbot conversation"""
        message_lower = message.lower()
        
        if state == 'initial':
            return {
                'response': "Hello! I'm your AI genetic health assistant. I'll help assess your genetic disorder risk through a few questions. First, what's your age?",
                'next_state': 'age',
                'progress': 10
            }
        
        elif state == 'age':
            return {
                'response': "Thank you. Now, please describe any symptoms you're experiencing (e.g., fatigue, joint pain, breathing issues, developmental delays, etc.)",
                'next_state': 'symptoms',
                'progress': 30
            }
        
        elif state == 'symptoms':
            return {
                'response': "I understand. Does anyone in your immediate family (parents, siblings, grandparents) have a history of genetic disorders? If yes, please specify which disorders.",
                'next_state': 'family_history',
                'progress': 50
            }
        
        elif state == 'family_history':
            return {
                'response': "Thank you for sharing. Have you experienced any of these: frequent infections, unusual bleeding, muscle weakness, or vision/hearing problems?",
                'next_state': 'additional_symptoms',
                'progress': 70
            }
        
        elif state == 'additional_symptoms':
            return {
                'response': "Almost done! On a scale of 1-10, how would you rate the severity of your symptoms?",
                'next_state': 'severity',
                'progress': 85
            }
        
        elif state == 'severity':
            return {
                'response': "Thank you for providing all the information. I'm now analyzing your data to assess genetic disorder risk. Please click 'Get Results' to see your personalized report.",
                'next_state': 'complete',
                'progress': 100
            }
        
        return {
            'response': "I'm here to help. Let's start the assessment.",
            'next_state': 'initial',
            'progress': 0
        }
    
    def predict_risk(self, symptoms, family_history):
        """Predict genetic disorder risk"""
        # Extract features
        features = self.extract_features(symptoms, family_history)
        
        # Predict
        prediction = self.model.predict(features.reshape(1, -1))
        predicted_class = np.argmax(prediction[0])
        confidence = float(prediction[0][predicted_class])
        
        disorders = ['Down Syndrome', 'Cystic Fibrosis', 'Sickle Cell Anemia', 
                    'Huntington Disease', 'Hemophilia', 'Thalassemia', 
                    'Muscular Dystrophy', 'Low Risk']
        
        disorder = disorders[predicted_class]
        risk_score = confidence * 100
        
        # Generate recommendations
        recommendations = self.generate_recommendations(disorder, risk_score)
        
        return {
            'disorder': disorder,
            'risk_score': round(risk_score, 2),
            'confidence': round(confidence * 100, 2),
            'recommendations': recommendations,
            'risk_level': self.get_risk_level(risk_score)
        }
    
    def extract_features(self, symptoms, family_history):
        """Extract numerical features from symptoms and family history"""
        features = np.zeros(20)
        
        # Feature engineering
        features[0] = len(symptoms) if isinstance(symptoms, list) else 0
        features[1] = 1 if family_history.get('has_history', False) else 0
        features[2] = family_history.get('severity', 5) / 10
        features[3:] = np.random.rand(17)  # Additional synthetic features
        
        return features
    
    def get_risk_level(self, risk_score):
        """Categorize risk level"""
        if risk_score < 30:
            return 'Low'
        elif risk_score < 60:
            return 'Moderate'
        else:
            return 'High'
    
    def generate_recommendations(self, disorder, risk_score):
        """Generate personalized recommendations"""
        recommendations = []
        
        if disorder == 'Low Risk':
            recommendations = [
                "Maintain a healthy lifestyle with regular exercise",
                "Schedule routine health checkups annually",
                "Keep family medical history updated",
                "Consider genetic counseling if planning a family"
            ]
        else:
            recommendations = [
                f"Consult a genetic counselor for {disorder} assessment",
                "Consider genetic testing for confirmation",
                "Schedule appointment with a specialist",
                "Discuss family planning options with healthcare provider",
                "Join support groups for genetic disorders",
                "Maintain detailed medical records"
            ]
        
        return recommendations
