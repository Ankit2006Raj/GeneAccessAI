"""
Enhanced ML Module with Ensemble Models
Combines LightGBM, Random Forest, XGBoost, and Logistic Regression
"""
import numpy as np
import pickle
import os
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split, cross_val_score
import lightgbm as lgb
try:
    import xgboost as xgb
    XGBOOST_AVAILABLE = True
except ImportError:
    XGBOOST_AVAILABLE = False
    print("XGBoost not installed. Install with: pip install xgboost")

class EnsembleGeneticPredictor:
    def __init__(self):
        self.models = {}
        self.best_model = None
        self.best_model_name = None
        self.scaler = StandardScaler()
        self.label_encoder = LabelEncoder()
        self.disorders = [
            'Down Syndrome', 'Cystic Fibrosis', 'Sickle Cell Anemia',
            'Huntington Disease', 'Hemophilia', 'Thalassemia',
            'Muscular Dystrophy', 'BRCA Mutation', 'Low Risk'
        ]
        self.load_or_train_models()
    
    def load_or_train_models(self):
        """Load existing models or train new ones"""
        model_path = 'models/ensemble_models.pkl'
        if os.path.exists(model_path):
            with open(model_path, 'rb') as f:
                saved_data = pickle.load(f)
                self.models = saved_data['models']
                self.best_model = saved_data['best_model']
                self.best_model_name = saved_data['best_model_name']
                self.scaler = saved_data['scaler']
                self.label_encoder = saved_data['label_encoder']
        else:
            self.train_ensemble_models()
    
    def generate_synthetic_data(self, n_samples=10000):
        """Generate synthetic training data"""
        np.random.seed(42)
        
        # Features: 30 features representing various genetic and symptom indicators
        X = np.random.rand(n_samples, 30)
        
        # Add some correlation patterns for realism
        X[:, 1] = X[:, 0] * 0.7 + np.random.rand(n_samples) * 0.3
        X[:, 5] = X[:, 2] * 0.5 + X[:, 3] * 0.5
        
        # Labels
        y = np.random.choice(range(len(self.disorders)), n_samples)
        
        return X, y
    
    def train_ensemble_models(self):
        """Train multiple models and select the best"""
        os.makedirs('models', exist_ok=True)
        
        print("Training ensemble models...")
        X, y = self.generate_synthetic_data()
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Encode labels
        y_train_encoded = self.label_encoder.fit_transform(y_train)
        
        # Train individual models
        print("Training LightGBM...")
        lgb_model = lgb.LGBMClassifier(
            objective='multiclass',
            num_class=len(self.disorders),
            n_estimators=100,
            learning_rate=0.05,
            num_leaves=31,
            random_state=42
        )
        lgb_model.fit(X_train_scaled, y_train)
        self.models['lightgbm'] = lgb_model
        
        print("Training Random Forest...")
        rf_model = RandomForestClassifier(
            n_estimators=100,
            max_depth=15,
            random_state=42,
            n_jobs=-1
        )
        rf_model.fit(X_train_scaled, y_train)
        self.models['random_forest'] = rf_model
        
        if XGBOOST_AVAILABLE:
            print("Training XGBoost...")
            xgb_model = xgb.XGBClassifier(
                objective='multi:softmax',
                num_class=len(self.disorders),
                n_estimators=100,
                learning_rate=0.05,
                max_depth=6,
                random_state=42
            )
            xgb_model.fit(X_train_scaled, y_train)
            self.models['xgboost'] = xgb_model
        
        print("Training Logistic Regression (baseline)...")
        lr_model = LogisticRegression(
            multi_class='multinomial',
            max_iter=1000,
            random_state=42
        )
        lr_model.fit(X_train_scaled, y_train)
        self.models['logistic_regression'] = lr_model
        
        # Evaluate models and select best
        print("\nEvaluating models...")
        best_score = 0
        for name, model in self.models.items():
            score = model.score(X_test_scaled, y_test)
            print(f"{name}: {score:.4f}")
            if score > best_score:
                best_score = score
                self.best_model = model
                self.best_model_name = name
        
        print(f"\nBest model: {self.best_model_name} (accuracy: {best_score:.4f})")
        
        # Create ensemble voting classifier
        if XGBOOST_AVAILABLE:
            estimators = [
                ('lgb', self.models['lightgbm']),
                ('rf', self.models['random_forest']),
                ('xgb', self.models['xgboost']),
                ('lr', self.models['logistic_regression'])
            ]
        else:
            estimators = [
                ('lgb', self.models['lightgbm']),
                ('rf', self.models['random_forest']),
                ('lr', self.models['logistic_regression'])
            ]
        
        print("\nTraining ensemble voting classifier...")
        ensemble = VotingClassifier(estimators=estimators, voting='soft')
        ensemble.fit(X_train_scaled, y_train)
        ensemble_score = ensemble.score(X_test_scaled, y_test)
        print(f"Ensemble accuracy: {ensemble_score:.4f}")
        
        self.models['ensemble'] = ensemble
        if ensemble_score > best_score:
            self.best_model = ensemble
            self.best_model_name = 'ensemble'
        
        # Save models
        self.save_models()
    
    def save_models(self):
        """Save all models"""
        save_data = {
            'models': self.models,
            'best_model': self.best_model,
            'best_model_name': self.best_model_name,
            'scaler': self.scaler,
            'label_encoder': self.label_encoder
        }
        with open('models/ensemble_models.pkl', 'wb') as f:
            pickle.dump(save_data, f)
        print(f"\nModels saved to models/ensemble_models.pkl")
    
    def predict_risk(self, features, use_ensemble=True):
        """Predict genetic disorder risk"""
        # Scale features
        features_scaled = self.scaler.transform(features.reshape(1, -1))
        
        # Use best model or ensemble
        model = self.best_model if use_ensemble else self.models.get('lightgbm')
        
        # Get prediction probabilities
        probabilities = model.predict_proba(features_scaled)[0]
        predicted_class = np.argmax(probabilities)
        confidence = float(probabilities[predicted_class])
        
        disorder = self.disorders[predicted_class]
        risk_score = confidence * 100
        
        # Get predictions from all models for comparison
        all_predictions = {}
        for name, model in self.models.items():
            pred_proba = model.predict_proba(features_scaled)[0]
            pred_class = np.argmax(pred_proba)
            all_predictions[name] = {
                'disorder': self.disorders[pred_class],
                'confidence': float(pred_proba[pred_class]) * 100
            }
        
        return {
            'disorder': disorder,
            'risk_score': round(risk_score, 2),
            'confidence': round(confidence * 100, 2),
            'risk_level': self.get_risk_level(risk_score),
            'model_used': self.best_model_name,
            'all_model_predictions': all_predictions,
            'top_3_risks': self.get_top_risks(probabilities)
        }
    
    def get_top_risks(self, probabilities):
        """Get top 3 disorder risks"""
        top_3_indices = np.argsort(probabilities)[-3:][::-1]
        return [
            {
                'disorder': self.disorders[idx],
                'probability': round(float(probabilities[idx]) * 100, 2)
            }
            for idx in top_3_indices
        ]
    
    def get_risk_level(self, risk_score):
        """Categorize risk level"""
        if risk_score < 30:
            return 'Low'
        elif risk_score < 60:
            return 'Moderate'
        else:
            return 'High'
    
    def extract_features(self, symptoms, family_history):
        """Extract numerical features from symptoms and family history"""
        features = np.zeros(30)
        
        # Basic features
        features[0] = len(symptoms) if isinstance(symptoms, list) else 0
        features[1] = 1 if family_history.get('has_history', False) else 0
        features[2] = family_history.get('severity', 5) / 10
        features[3] = family_history.get('age', 30) / 100
        
        # Symptom-based features
        symptom_keywords = {
            'pain': 4, 'fatigue': 5, 'weakness': 6, 'bleeding': 7,
            'breathing': 8, 'vision': 9, 'hearing': 10, 'developmental': 11,
            'cognitive': 12, 'mobility': 13, 'infection': 14
        }
        
        if isinstance(symptoms, list):
            for symptom in symptoms:
                symptom_lower = symptom.lower()
                for keyword, idx in symptom_keywords.items():
                    if keyword in symptom_lower:
                        features[idx] = 1
        
        # Family history features
        if isinstance(family_history, dict):
            disorders_mentioned = family_history.get('disorders', [])
            if isinstance(disorders_mentioned, list):
                features[15] = len(disorders_mentioned)
        
        # Fill remaining features with synthetic data
        features[16:] = np.random.rand(14)
        
        return features

if __name__ == '__main__':
    # Train models when run directly
    predictor = EnsembleGeneticPredictor()
    print("\nEnsemble models ready!")
