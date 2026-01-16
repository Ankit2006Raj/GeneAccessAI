"""
GeneAccessAI - AI-Powered Genetic Health Assessment Platform
Integrates: Ensemble ML, NLP Suggestions, Disease Encyclopedia,
Multi-language Support, and Genetic Counseling
"""
from flask import Flask, render_template, request, jsonify, session, send_file
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import secrets
import os
import json

# Import ML and service modules
try:
    from src.models.ml_ensemble import EnsembleGeneticPredictor
    from src.services.nlp_symptom_suggester import SymptomSuggester
    from src.services.disease_encyclopedia import DiseaseEncyclopedia
    from src.services.multilingual_support import MultilingualTranslator
    from src.services.genetic_counseling import GeneticCounselor
    ENHANCED_FEATURES = True
except ImportError:
    from src.models.ml_model import GeneticRiskPredictor
    ENHANCED_FEATURES = False

from src.services.report_generator import PDFReportGenerator
from src.api.advanced_features_routes import advanced_bp
from src.api.new_advanced_features_routes import new_advanced_bp

app = Flask(__name__)
app.register_blueprint(advanced_bp)
app.register_blueprint(new_advanced_bp)
app.config['SECRET_KEY'] = secrets.token_hex(16)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///geneaccess.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Initialize components
if ENHANCED_FEATURES:
    predictor = EnsembleGeneticPredictor()
    symptom_suggester = SymptomSuggester()
    disease_encyclopedia = DiseaseEncyclopedia()
    translator = MultilingualTranslator()
    counselor = GeneticCounselor()
else:
    predictor = GeneticRiskPredictor()

report_gen = PDFReportGenerator()

# Database Models
class Assessment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    symptoms = db.Column(db.Text, nullable=False)
    family_history = db.Column(db.Text, nullable=False)
    risk_score = db.Column(db.Float, nullable=False)
    predicted_disorder = db.Column(db.String(200), nullable=False)
    recommendations = db.Column(db.Text, nullable=False)
    model_used = db.Column(db.String(50), default='ensemble')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    report_path = db.Column(db.String(300))

# Routes
@app.route('/')
def index():
    if ENHANCED_FEATURES:
        lang = session.get('language', 'en')
        translations = translator.get_all_translations(lang)
        return render_template('index.html', t=translations, lang=lang)
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    assessments = Assessment.query.order_by(Assessment.created_at.desc()).all()
    if ENHANCED_FEATURES:
        lang = session.get('language', 'en')
        translations = translator.get_all_translations(lang)
        return render_template('dashboard.html', assessments=assessments, t=translations, lang=lang)
    return render_template('dashboard.html', assessments=assessments)

@app.route('/assessment')
def assessment():
    if ENHANCED_FEATURES:
        lang = session.get('language', 'en')
        translations = translator.get_all_translations(lang)
        return render_template('assessment.html', t=translations, lang=lang)
    return render_template('assessment.html')

@app.route('/assessment-form')
def assessment_form():
    if ENHANCED_FEATURES:
        lang = session.get('language', 'en')
        translations = translator.get_all_translations(lang)
        return render_template('assessment_form.html', t=translations, lang=lang)
    return render_template('assessment_form.html')

@app.route('/assessment-chat')
def assessment_chat():
    if ENHANCED_FEATURES:
        lang = session.get('language', 'en')
        translations = translator.get_all_translations(lang)
        return render_template('assessment_chat.html', t=translations, lang=lang)
    return render_template('assessment_chat.html')

@app.route('/about')
def about():
    if ENHANCED_FEATURES:
        lang = session.get('language', 'en')
        translations = translator.get_all_translations(lang)
        return render_template('about.html', t=translations, lang=lang)
    return render_template('about.html')

@app.route('/risk-timeline')
def risk_timeline():
    """Risk Timeline page"""
    if ENHANCED_FEATURES:
        lang = session.get('language', 'en')
        translations = translator.get_all_translations(lang)
        return render_template('risk_timeline.html', t=translations, lang=lang)
    return render_template('risk_timeline.html')

@app.route('/family-pedigree')
def family_pedigree():
    """Family Pedigree page"""
    if ENHANCED_FEATURES:
        lang = session.get('language', 'en')
        translations = translator.get_all_translations(lang)
        return render_template('family_pedigree.html', t=translations, lang=lang)
    return render_template('family_pedigree.html')

@app.route('/ethnicity-risk')
def ethnicity_risk():
    """Ethnicity Risk Adjuster page"""
    if ENHANCED_FEATURES:
        lang = session.get('language', 'en')
        translations = translator.get_all_translations(lang)
        return render_template('ethnicity_risk.html', t=translations, lang=lang)
    return render_template('ethnicity_risk.html')

@app.route('/genomic-profile')
def genomic_profile():
    """Genomic Profile Generator page"""
    if ENHANCED_FEATURES:
        lang = session.get('language', 'en')
        translations = translator.get_all_translations(lang)
        return render_template('genomic_profile.html', t=translations, lang=lang)
    return render_template('genomic_profile.html')

@app.route('/clinical-tests')
def clinical_tests():
    """Clinical Test Recommender page"""
    if ENHANCED_FEATURES:
        lang = session.get('language', 'en')
        translations = translator.get_all_translations(lang)
        return render_template('clinical_tests.html', t=translations, lang=lang)
    return render_template('clinical_tests.html')

@app.route('/advanced-features')
def advanced_features():
    """Advanced Features Overview page"""
    if ENHANCED_FEATURES:
        lang = session.get('language', 'en')
        translations = translator.get_all_translations(lang)
        return render_template('advanced_features_overview.html', t=translations, lang=lang)
    return render_template('advanced_features_overview.html')

@app.route('/psychosocial-risk')
def psychosocial_risk():
    """Psychosocial Risk Modulator page"""
    if ENHANCED_FEATURES:
        lang = session.get('language', 'en')
        translations = translator.get_all_translations(lang)
        return render_template('psychosocial_risk.html', t=translations, lang=lang)
    return render_template('psychosocial_risk.html')

@app.route('/clinical-knowledge')
def clinical_knowledge():
    """Clinical Knowledge Updater page"""
    if ENHANCED_FEATURES:
        lang = session.get('language', 'en')
        translations = translator.get_all_translations(lang)
        return render_template('clinical_knowledge.html', t=translations, lang=lang)
    return render_template('clinical_knowledge.html')

@app.route('/drug-reactions')
def drug_reactions():
    """Adverse Drug Reaction Predictor page"""
    if ENHANCED_FEATURES:
        lang = session.get('language', 'en')
        translations = translator.get_all_translations(lang)
        return render_template('drug_reactions.html', t=translations, lang=lang)
    return render_template('drug_reactions.html')

@app.route('/inheritance-simulator')
def inheritance_simulator():
    """Inheritance Simulation Mode page"""
    if ENHANCED_FEATURES:
        lang = session.get('language', 'en')
        translations = translator.get_all_translations(lang)
        return render_template('inheritance_simulator.html', t=translations, lang=lang)
    return render_template('inheritance_simulator.html')

# Enhanced feature routes
if ENHANCED_FEATURES:
    @app.route('/encyclopedia')
    def encyclopedia():
        lang = session.get('language', 'en')
        translations = translator.get_all_translations(lang)
        diseases = disease_encyclopedia.list_all_diseases()
        return render_template('encyclopedia.html', t=translations, lang=lang, diseases=diseases)

    @app.route('/api/suggest-symptoms', methods=['POST'])
    def suggest_symptoms():
        data = request.get_json()
        user_input = data.get('input', '')
        suggestions = symptom_suggester.suggest_symptoms(user_input, max_suggestions=5)
        category = symptom_suggester.get_symptom_category(user_input)
        return jsonify({'suggestions': suggestions, 'category': category, 'input': user_input})

    @app.route('/api/search-symptoms', methods=['POST'])
    def search_symptoms():
        data = request.get_json()
        query = data.get('query', '')
        results = symptom_suggester.search_symptoms(query, limit=10)
        return jsonify({'results': results})

    @app.route('/api/disease-info', methods=['POST'])
    def disease_info():
        data = request.get_json()
        disease_name = data.get('disease', '')
        info = disease_encyclopedia.get_disease_info(disease_name)
        return jsonify(info)

    @app.route('/api/ask-disease', methods=['POST'])
    def ask_disease():
        data = request.get_json()
        question = data.get('question', '')
        answer = disease_encyclopedia.answer_question(question)
        return jsonify({'question': question, 'answer': answer})

    @app.route('/api/diseases')
    def list_diseases():
        diseases = disease_encyclopedia.list_all_diseases()
        return jsonify({'diseases': diseases})

    @app.route('/api/change-language', methods=['POST'])
    def change_language():
        data = request.get_json()
        language = data.get('language', 'en')
        if language in translator.supported_languages:
            session['language'] = language
            return jsonify({'success': True, 'language': language, 'translations': translator.get_all_translations(language)})
        return jsonify({'success': False, 'message': 'Language not supported'}), 400

    @app.route('/api/languages')
    def get_languages():
        return jsonify({'languages': translator.get_supported_languages()})

    @app.route('/api/counseling/<disorder>')
    def get_counseling(disorder):
        risk_level = request.args.get('risk_level', 'moderate')
        counseling_info = counselor.get_counseling(disorder, risk_level)
        return jsonify(counseling_info)

    @app.route('/api/counseling-summary', methods=['POST'])
    def counseling_summary():
        data = request.get_json()
        disorder = data.get('disorder', 'Low Risk')
        risk_level = data.get('risk_level', 'moderate')
        summary = counselor.generate_counseling_summary(disorder, risk_level)
        return jsonify({'summary': summary})

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    message = data.get('message', '')
    conversation_state = data.get('state', 'initial')
    
    if ENHANCED_FEATURES and any(word in message.lower() for word in ['what is', 'what\'s', 'tell me about', 'explain']):
        answer = disease_encyclopedia.answer_question(message)
        return jsonify({'response': answer, 'next_state': conversation_state, 'progress': data.get('progress', 0), 'type': 'encyclopedia'})
    
    response = process_chat_message(message, conversation_state)
    return jsonify(response)

def process_chat_message(message, state):
    if state == 'initial':
        return {'response': "Hello! I'm your AI genetic health assistant. I'll help assess your genetic disorder risk through a few questions. First, may I have your name?", 'next_state': 'patient_name', 'progress': 5}
    elif state == 'patient_name':
        return {'response': "Nice to meet you! Now, what's your age?", 'next_state': 'age', 'progress': 15}
    elif state == 'age':
        return {'response': "Thank you. Now, please describe any symptoms you're experiencing. You can type symptoms and I'll suggest related ones.", 'next_state': 'symptoms', 'progress': 30}
    elif state == 'symptoms':
        return {'response': "I understand. Does anyone in your immediate family (parents, siblings, grandparents) have a history of genetic disorders? If yes, please specify which disorders.", 'next_state': 'family_history', 'progress': 50}
    elif state == 'family_history':
        return {'response': "Thank you for sharing. Have you experienced any of these: frequent infections, unusual bleeding, muscle weakness, or vision/hearing problems?", 'next_state': 'additional_symptoms', 'progress': 70}
    elif state == 'additional_symptoms':
        return {'response': "Almost done! On a scale of 1-10, how would you rate the severity of your symptoms?", 'next_state': 'severity', 'progress': 85}
    elif state == 'severity':
        return {'response': "Thank you for providing all the information. I'm now analyzing your data using our ML models. Please click 'Get Results' to see your personalized report.", 'next_state': 'complete', 'progress': 100}
    return {'response': "I'm here to help. Let's start the assessment.", 'next_state': 'initial', 'progress': 0}

@app.route('/api/predict', methods=['POST'])
def predict():
    """Prediction endpoint for chat-based assessment"""
    try:
        data = request.get_json()
        symptoms = data.get('symptoms', [])
        family_history = data.get('family_history', {})
        patient_name = data.get('patient_name', 'Guest')  # Get patient name from request
        
        # Debug logging
        print(f"DEBUG: Received patient_name: '{patient_name}'")
        print(f"DEBUG: Full data: {data}")
        
        if ENHANCED_FEATURES:
            try:
                features = predictor.extract_features(symptoms, family_history)
                prediction = predictor.predict_risk(features, use_ensemble=True)
                counseling_info = counselor.get_counseling(prediction['disorder'], prediction['risk_level'])
                prediction['counseling'] = counseling_info
                prediction['recommendations'] = counseling_info['preventive_care'][:5]
            except Exception as e:
                print(f"Enhanced prediction error: {e}")
                prediction = create_basic_prediction(symptoms, family_history)
        else:
            prediction = create_basic_prediction(symptoms, family_history)
        
        assessment = Assessment(
            symptoms=json.dumps(symptoms),
            family_history=json.dumps(family_history),
            risk_score=prediction['risk_score'],
            predicted_disorder=prediction['disorder'],
            recommendations=json.dumps(prediction['recommendations']),
            model_used=prediction.get('model_used', 'basic')
        )
        db.session.add(assessment)
        db.session.commit()
        
        try:
            # Use patient name from request data
            print(f"DEBUG: Generating report with patient_name: '{patient_name}'")
            report_path = report_gen.generate_report(assessment_id=assessment.id, username=patient_name, prediction=prediction)
            assessment.report_path = report_path
            db.session.commit()
            print(f"DEBUG: Report generated successfully at: {report_path}")
        except Exception as e:
            print(f"Report generation error: {e}")
            import traceback
            traceback.print_exc()
        
        prediction['assessment_id'] = assessment.id
        return jsonify(prediction)
    
    except Exception as e:
        print(f"Prediction error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/predict-form', methods=['POST'])
def predict_form():
    """Prediction endpoint for form-based assessment"""
    try:
        data = request.get_json()
        
        # Extract patient name
        patient_name = data.get('patient_name', 'Guest')
        
        # Debug logging
        print(f"DEBUG FORM: Received patient_name: '{patient_name}'")
        print(f"DEBUG FORM: Full data keys: {data.keys()}")
        
        # Extract form data with enhanced fields
        age = data.get('age', 0)
        gender = data.get('gender', '')
        ethnicity = data.get('ethnicity', '')
        height = data.get('height', 0)
        weight = data.get('weight', 0)
        
        # Calculate BMI
        bmi = 0
        if height > 0 and weight > 0:
            bmi = round(weight / ((height / 100) ** 2), 1)
        
        symptoms_list = data.get('symptoms', [])
        symptom_onset = data.get('symptom_onset', '')
        
        family_history_data = {
            'has_history': data.get('has_family_history', False),
            'disorders': data.get('family_disorders', []),
            'affected_relatives': data.get('affected_relatives', []),
            'severity': data.get('symptom_severity', 5)
        }
        
        lifestyle_data = {
            'smoking': data.get('smoking_status', ''),
            'alcohol': data.get('alcohol_consumption', ''),
            'exercise': data.get('exercise_frequency', ''),
            'previous_testing': data.get('previous_testing', ''),
            'chronic_conditions': data.get('chronic_conditions', [])
        }
        
        # Convert to format expected by predictor
        symptoms = symptoms_list
        family_history = family_history_data
        
        if ENHANCED_FEATURES:
            try:
                features = predictor.extract_features(symptoms, family_history)
                prediction = predictor.predict_risk(features, use_ensemble=True)
                counseling_info = counselor.get_counseling(prediction['disorder'], prediction['risk_level'])
                prediction['counseling'] = counseling_info
                prediction['recommendations'] = counseling_info['preventive_care'][:5]
            except Exception as e:
                print(f"Enhanced prediction error: {e}")
                # Fallback to enhanced basic prediction
                prediction = create_enhanced_prediction(
                    symptoms, family_history, age, ethnicity, bmi, lifestyle_data, symptom_onset
                )
        else:
            prediction = create_enhanced_prediction(
                symptoms, family_history, age, ethnicity, bmi, lifestyle_data, symptom_onset
            )
        
        # Save assessment with enhanced data
        assessment = Assessment(
            symptoms=json.dumps({
                'symptoms': symptoms,
                'onset': symptom_onset,
                'severity': data.get('symptom_severity', 5)
            }),
            family_history=json.dumps(family_history),
            risk_score=prediction['risk_score'],
            predicted_disorder=prediction['disorder'],
            recommendations=json.dumps(prediction['recommendations']),
            model_used=prediction.get('model_used', 'enhanced_basic')
        )
        db.session.add(assessment)
        db.session.commit()
        
        # Generate PDF report
        try:
            # Use patient name from form data
            print(f"DEBUG FORM: Generating report with patient_name: '{patient_name}'")
            report_path = report_gen.generate_report(assessment_id=assessment.id, username=patient_name, prediction=prediction)
            assessment.report_path = report_path
            db.session.commit()
            print(f"DEBUG FORM: Report generated successfully at: {report_path}")
        except Exception as e:
            print(f"Report generation error: {e}")
            import traceback
            traceback.print_exc()
            # Continue without report
        
        prediction['assessment_id'] = assessment.id
        prediction['bmi'] = bmi
        return jsonify(prediction)
    
    except Exception as e:
        print(f"Prediction error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

def create_basic_prediction(symptoms, family_history):
    """Create a basic prediction when ML models fail"""
    # Calculate basic risk score
    risk_score = 0
    
    # Add points for symptoms
    risk_score += len(symptoms) * 10
    
    # Add points for family history
    if family_history.get('has_history', False):
        risk_score += 30
        risk_score += len(family_history.get('disorders', [])) * 10
    
    # Add severity factor
    severity = family_history.get('severity', 5)
    risk_score += severity * 2
    
    # Cap at 100
    risk_score = min(risk_score, 100)
    
    # Determine risk level and disorder
    if risk_score < 30:
        risk_level = 'Low'
        disorder = 'Low Risk - No Significant Genetic Disorder Detected'
    elif risk_score < 60:
        risk_level = 'Moderate'
        disorder = 'Moderate Risk - Further Evaluation Recommended'
    else:
        risk_level = 'High'
        disorder = 'High Risk - Genetic Counseling Strongly Recommended'
    
    return {
        'risk_score': risk_score,
        'risk_level': risk_level,
        'disorder': disorder,
        'confidence': 75,
        'model_used': 'basic',
        'recommendations': [
            'Consult with a healthcare professional',
            'Consider genetic counseling',
            'Maintain a healthy lifestyle',
            'Regular health check-ups',
            'Monitor symptoms closely'
        ]
    }

def create_enhanced_prediction(symptoms, family_history, age, ethnicity, bmi, lifestyle, symptom_onset):
    """Create an enhanced prediction with more realistic risk assessment"""
    risk_score = 0
    risk_factors = []
    disorder_type = None
    
    # Age-based risk (certain genetic conditions manifest at different ages)
    if age < 18:
        risk_score += 5
        risk_factors.append("Pediatric age group")
    elif age > 50:
        risk_score += 10
        risk_factors.append("Advanced age")
    
    # Ethnicity-based risk (some genetic disorders are more common in certain populations)
    ethnicity_risks = {
        'african': {'sickle_cell': 15, 'thalassemia': 5},
        'asian': {'thalassemia': 15, 'g6pd_deficiency': 10},
        'caucasian': {'cystic_fibrosis': 10, 'hemochromatosis': 8},
        'hispanic': {'thalassemia': 8, 'g6pd_deficiency': 5},
        'middle_eastern': {'thalassemia': 12, 'familial_mediterranean_fever': 10}
    }
    
    # Symptom analysis with pattern matching
    symptom_patterns = {
        'respiratory': ['breathing_difficulties', 'frequent_infections'],
        'neurological': ['seizures', 'cognitive_impairment', 'developmental_delays'],
        'musculoskeletal': ['muscle_weakness', 'joint_pain', 'bone_deformities'],
        'hematological': ['unusual_bleeding', 'fatigue'],
        'sensory': ['vision_problems', 'hearing_loss'],
        'cardiac': ['heart_palpitations', 'fatigue'],
        'metabolic': ['growth_abnormalities', 'developmental_delays']
    }
    
    detected_patterns = []
    for pattern_name, pattern_symptoms in symptom_patterns.items():
        if any(s in symptoms for s in pattern_symptoms):
            detected_patterns.append(pattern_name)
            risk_score += 8
    
    # Symptom count and severity
    symptom_count = len(symptoms)
    if symptom_count > 0:
        risk_score += symptom_count * 5
        risk_factors.append(f"{symptom_count} symptoms reported")
    
    severity = family_history.get('severity', 5)
    risk_score += severity * 3
    
    # Symptom onset timing
    if symptom_onset in ['birth', 'childhood']:
        risk_score += 15
        risk_factors.append("Early symptom onset")
    
    # Family history analysis
    family_disorders = family_history.get('disorders', [])
    affected_relatives = family_history.get('affected_relatives', [])
    
    if family_history.get('has_history', False):
        risk_score += 25
        risk_factors.append("Positive family history")
        
        # First-degree relatives increase risk more
        if 'parent' in affected_relatives or 'sibling' in affected_relatives:
            risk_score += 15
            risk_factors.append("First-degree relative affected")
        
        # Multiple family members
        if len(affected_relatives) > 2:
            risk_score += 10
            risk_factors.append("Multiple family members affected")
        
        # Specific disorder patterns
        if 'sickle_cell' in family_disorders or 'thalassemia' in family_disorders:
            disorder_type = 'Hemoglobinopathy'
            risk_score += 10
        elif 'cystic_fibrosis' in family_disorders:
            disorder_type = 'Cystic Fibrosis'
            risk_score += 12
        elif 'muscular_dystrophy' in family_disorders:
            disorder_type = 'Muscular Dystrophy'
            risk_score += 12
        elif 'huntingtons' in family_disorders:
            disorder_type = 'Huntington\'s Disease'
            risk_score += 15
    
    # BMI considerations
    if bmi > 0:
        if bmi < 18.5 or bmi > 30:
            risk_score += 5
            risk_factors.append("BMI outside normal range")
    
    # Lifestyle factors
    if lifestyle.get('smoking') == 'current':
        risk_score += 8
        risk_factors.append("Current smoker")
    
    if lifestyle.get('alcohol') in ['frequent']:
        risk_score += 5
    
    if lifestyle.get('exercise') == 'none':
        risk_score += 3
    
    # Chronic conditions
    chronic_conditions = lifestyle.get('chronic_conditions', [])
    if len(chronic_conditions) > 0 and 'none' not in chronic_conditions:
        risk_score += len(chronic_conditions) * 5
        risk_factors.append(f"{len(chronic_conditions)} chronic condition(s)")
    
    # Previous testing
    if lifestyle.get('previous_testing') == 'yes_abnormal':
        risk_score += 20
        risk_factors.append("Previous abnormal genetic test")
    elif lifestyle.get('previous_testing') == 'yes_carrier':
        risk_score += 10
        risk_factors.append("Known carrier status")
    
    # Cap at 100
    risk_score = min(risk_score, 100)
    
    # Determine risk level and disorder
    if risk_score < 30:
        risk_level = 'Low'
        if not disorder_type:
            disorder = 'Low Risk - No Significant Genetic Disorder Detected'
        else:
            disorder = f'Low Risk - {disorder_type} (Monitoring Recommended)'
        confidence = 85
        recommendations = [
            'Continue regular health check-ups',
            'Maintain a healthy lifestyle with balanced diet and exercise',
            'Stay informed about family medical history',
            'Consider genetic counseling if planning a family',
            'Monitor for any new symptoms'
        ]
    elif risk_score < 60:
        risk_level = 'Moderate'
        if not disorder_type:
            if 'neurological' in detected_patterns:
                disorder = 'Moderate Risk - Neurological Genetic Disorder Possible'
            elif 'hematological' in detected_patterns:
                disorder = 'Moderate Risk - Blood Disorder Possible'
            elif 'musculoskeletal' in detected_patterns:
                disorder = 'Moderate Risk - Musculoskeletal Disorder Possible'
            else:
                disorder = 'Moderate Risk - Further Genetic Evaluation Recommended'
        else:
            disorder = f'Moderate Risk - {disorder_type} Suspected'
        confidence = 78
        recommendations = [
            'Schedule consultation with a genetic counselor',
            'Consider comprehensive genetic testing',
            'Document all symptoms and family history in detail',
            'Regular monitoring by healthcare provider',
            'Discuss preventive measures with your doctor',
            'Join support groups for genetic conditions'
        ]
    else:
        risk_level = 'High'
        if not disorder_type:
            if 'neurological' in detected_patterns and 'developmental_delays' in symptoms:
                disorder = 'High Risk - Neurodevelopmental Genetic Disorder Likely'
            elif 'hematological' in detected_patterns and family_disorders:
                disorder = 'High Risk - Inherited Blood Disorder Likely'
            elif 'musculoskeletal' in detected_patterns and 'muscle_weakness' in symptoms:
                disorder = 'High Risk - Muscular Dystrophy or Related Disorder Likely'
            else:
                disorder = 'High Risk - Significant Genetic Disorder Likely'
        else:
            disorder = f'High Risk - {disorder_type} Highly Suspected'
        confidence = 72
        recommendations = [
            'URGENT: Schedule immediate consultation with genetic specialist',
            'Comprehensive genetic testing strongly recommended',
            'Detailed family pedigree analysis needed',
            'Consider referral to specialized treatment center',
            'Discuss treatment and management options',
            'Genetic counseling for family members',
            'Explore clinical trials and research studies',
            'Connect with patient advocacy organizations'
        ]
    
    return {
        'risk_score': risk_score,
        'risk_level': risk_level,
        'disorder': disorder,
        'confidence': confidence,
        'model_used': 'enhanced_basic',
        'risk_factors': risk_factors,
        'detected_patterns': detected_patterns,
        'recommendations': recommendations
    }

@app.route('/api/download-report/<int:assessment_id>')
def download_report(assessment_id):
    assessment = Assessment.query.get_or_404(assessment_id)
    if assessment.report_path and os.path.exists(assessment.report_path):
        return send_file(assessment.report_path, as_attachment=True)
    return jsonify({'error': 'Report not found'}), 404

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    print(f"\n{'='*60}")
    print(f"GeneAccessAI Server Starting...")
    print(f"Enhanced Features: {'Enabled' if ENHANCED_FEATURES else 'Disabled (Basic Mode)'}")
    print(f"{'='*60}\n")
    app.run(debug=True, host='0.0.0.0', port=5000)
