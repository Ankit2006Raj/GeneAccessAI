"""
API Routes for New Advanced Features:
- Psychosocial Risk Modulator
- Clinical Knowledge Updater
- Adverse Drug Reaction Predictor
- Inheritance Simulator
"""
from flask import Blueprint, request, jsonify
from src.services.psychosocial_risk_modulator import PsychosocialRiskModulator
from src.services.clinical_knowledge_updater import ClinicalKnowledgeUpdater
from src.services.adverse_drug_reaction_predictor import AdverseDrugReactionPredictor
from src.services.inheritance_simulator import InheritanceSimulator

new_advanced_bp = Blueprint('new_advanced', __name__, url_prefix='/api/advanced')

# Initialize services
psychosocial_modulator = PsychosocialRiskModulator()
knowledge_updater = ClinicalKnowledgeUpdater()
drug_predictor = AdverseDrugReactionPredictor()
inheritance_sim = InheritanceSimulator()


# ============================================================================
# PSYCHOSOCIAL RISK MODULATOR ROUTES
# ============================================================================

@new_advanced_bp.route('/psychosocial/adjust-risk', methods=['POST'])
def psychosocial_adjust_risk():
    """Calculate psychosocial-adjusted genetic risk."""
    try:
        data = request.get_json()
        
        base_risk_score = data.get('base_risk_score', 50)
        disorder_category = data.get('disorder_category', 'general')
        mental_health_data = data.get('mental_health', {})
        lifestyle_data = data.get('lifestyle', {})
        
        result = psychosocial_modulator.calculate_psychosocial_adjustment(
            base_risk_score,
            disorder_category,
            mental_health_data,
            lifestyle_data
        )
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@new_advanced_bp.route('/psychosocial/tri-model-analysis', methods=['POST'])
def psychosocial_tri_model():
    """Generate tri-model analysis (Genetics × Mental Health × Lifestyle)."""
    try:
        data = request.get_json()
        
        genetic_data = data.get('genetic_data', {})
        mental_health_data = data.get('mental_health', {})
        lifestyle_data = data.get('lifestyle', {})
        
        result = psychosocial_modulator.generate_tri_model_analysis(
            genetic_data,
            mental_health_data,
            lifestyle_data
        )
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ============================================================================
# CLINICAL KNOWLEDGE UPDATER ROUTES
# ============================================================================

@new_advanced_bp.route('/knowledge/check-updates', methods=['GET'])
def check_knowledge_updates():
    """Check for new medical research updates."""
    try:
        disorder = request.args.get('disorder')
        result = knowledge_updater.check_for_updates(disorder)
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@new_advanced_bp.route('/knowledge/apply-update', methods=['POST'])
def apply_knowledge_update():
    """Apply a research update to knowledge base."""
    try:
        data = request.get_json()
        update = data.get('update', {})
        
        result = knowledge_updater.apply_update(update)
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@new_advanced_bp.route('/knowledge/disorder-info/<disorder>', methods=['GET'])
def get_disorder_knowledge(disorder):
    """Get current knowledge base information for a disorder."""
    try:
        result = knowledge_updater.get_disorder_info(disorder)
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@new_advanced_bp.route('/knowledge/update-history', methods=['GET'])
def get_update_history():
    """Get history of knowledge base updates."""
    try:
        disorder = request.args.get('disorder')
        limit = int(request.args.get('limit', 10))
        
        result = knowledge_updater.get_update_history(disorder, limit)
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@new_advanced_bp.route('/knowledge/update-report', methods=['GET'])
def get_knowledge_update_report():
    """Generate comprehensive update report."""
    try:
        result = knowledge_updater.generate_update_report()
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@new_advanced_bp.route('/knowledge/research-trends', methods=['GET'])
def get_research_trends():
    """Get current research trends."""
    try:
        result = knowledge_updater.get_research_trends()
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ============================================================================
# ADVERSE DRUG REACTION PREDICTOR ROUTES
# ============================================================================

@new_advanced_bp.route('/drug-reactions/predict', methods=['POST'])
def predict_drug_reactions():
    """Predict adverse drug reactions."""
    try:
        data = request.get_json()
        
        patient_data = data.get('patient_data', {})
        medications = data.get('medications', [])
        genetic_disorders = data.get('genetic_disorders', [])
        
        result = drug_predictor.predict_drug_reactions(
            patient_data,
            medications,
            genetic_disorders
        )
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@new_advanced_bp.route('/drug-reactions/anesthesia-risk', methods=['POST'])
def get_anesthesia_risk():
    """Get anesthesia risk profile."""
    try:
        data = request.get_json()
        
        genetic_disorders = data.get('genetic_disorders', [])
        surgery_type = data.get('surgery_type', 'General')
        
        result = drug_predictor.get_anesthesia_risk_profile(
            genetic_disorders,
            surgery_type
        )
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@new_advanced_bp.route('/drug-reactions/check-interactions', methods=['POST'])
def check_drug_interactions():
    """Check for drug-drug interactions."""
    try:
        data = request.get_json()
        medications = data.get('medications', [])
        
        result = drug_predictor.check_drug_interactions(medications)
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ============================================================================
# INHERITANCE SIMULATOR ROUTES
# ============================================================================

@new_advanced_bp.route('/inheritance/simulate', methods=['POST'])
def simulate_inheritance():
    """Simulate offspring genetic risk."""
    try:
        data = request.get_json()
        
        parent1_data = data.get('parent1', {})
        parent2_data = data.get('parent2', {})
        disorder = data.get('disorder', '')
        num_simulations = data.get('num_simulations', 1000)
        
        result = inheritance_sim.simulate_offspring_risk(
            parent1_data,
            parent2_data,
            disorder,
            num_simulations
        )
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@new_advanced_bp.route('/inheritance/compare-disorders', methods=['POST'])
def compare_inheritance_disorders():
    """Compare inheritance risks for multiple disorders."""
    try:
        data = request.get_json()
        
        parent1_data = data.get('parent1', {})
        parent2_data = data.get('parent2', {})
        disorders = data.get('disorders', [])
        
        result = inheritance_sim.compare_multiple_disorders(
            parent1_data,
            parent2_data,
            disorders
        )
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@new_advanced_bp.route('/inheritance/family-planning-report', methods=['POST'])
def generate_family_planning_report():
    """Generate comprehensive family planning report."""
    try:
        data = request.get_json()
        
        parent1_data = data.get('parent1', {})
        parent2_data = data.get('parent2', {})
        disorders = data.get('disorders', [])
        
        result = inheritance_sim.generate_family_planning_report(
            parent1_data,
            parent2_data,
            disorders
        )
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
