"""
API Routes for Advanced Features:
- Risk Timeline Projections
- Family Pedigree Analysis
- Ethnicity-Aware Risk Adjustment
- Synthetic Genomic Profiles
- Clinical Test Recommendations
"""

from flask import Blueprint, request, jsonify
from src.services.risk_timeline import RiskTimelineEngine
from src.services.family_pedigree import FamilyPedigreeAI
from src.services.ethnicity_risk_adjuster import EthnicityRiskAdjuster
from src.services.genomic_profile_generator import GenomicProfileGenerator
from src.services.clinical_test_recommender import ClinicalTestRecommender

# Create blueprint
advanced_bp = Blueprint('advanced', __name__, url_prefix='/api/advanced')

# Initialize services
timeline_engine = RiskTimelineEngine()
pedigree_ai = FamilyPedigreeAI()
ethnicity_adjuster = EthnicityRiskAdjuster()
genomic_generator = GenomicProfileGenerator()
test_recommender = ClinicalTestRecommender()

@advanced_bp.route('/risk-timeline', methods=['POST'])
def generate_risk_timeline():
    """
    Generate AI-powered risk timeline with future projections
    
    Expected JSON:
    {
        "current_age": 35,
        "disorder": "Huntington Disease",
        "current_risk_score": 65,
        "family_history": {...},
        "lifestyle_data": {...}
    }
    """
    try:
        data = request.get_json()
        
        current_age = data.get('current_age', 30)
        disorder = data.get('disorder', 'Low Risk')
        current_risk_score = data.get('current_risk_score', 50)
        family_history = data.get('family_history', {})
        lifestyle_data = data.get('lifestyle_data', {})
        
        # Generate timeline
        timeline = timeline_engine.generate_risk_timeline(
            current_age=current_age,
            disorder=disorder,
            current_risk_score=current_risk_score,
            family_history=family_history,
            lifestyle_data=lifestyle_data
        )
        
        # Export chart data
        chart_data = timeline_engine.export_timeline_data(timeline)
        timeline['chart_data'] = chart_data
        
        return jsonify({
            'success': True,
            'timeline': timeline
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@advanced_bp.route('/risk-timeline/what-if', methods=['POST'])
def simulate_what_if():
    """
    Simulate what-if scenarios for lifestyle changes
    
    Expected JSON:
    {
        "current_age": 35,
        "disorder": "Huntington Disease",
        "current_risk_score": 65,
        "family_history": {...},
        "lifestyle_changes": ["weight_loss", "quit_smoking"]
    }
    """
    try:
        data = request.get_json()
        
        current_age = data.get('current_age', 30)
        disorder = data.get('disorder', 'Low Risk')
        current_risk_score = data.get('current_risk_score', 50)
        family_history = data.get('family_history', {})
        lifestyle_changes = data.get('lifestyle_changes', [])
        
        # Simulate scenario
        scenario = timeline_engine._simulate_lifestyle_change(
            scenario_name='Custom Scenario',
            current_age=current_age,
            disorder=disorder,
            current_risk=current_risk_score,
            family_history=family_history,
            changes=lifestyle_changes
        )
        
        return jsonify({
            'success': True,
            'scenario': scenario
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@advanced_bp.route('/pedigree/build', methods=['POST'])
def build_pedigree():
    """
    Build family pedigree with genetic analysis
    
    Expected JSON:
    {
        "family_data": [
            {
                "id": 1,
                "name": "John Doe",
                "gender": "male",
                "age": 35,
                "generation": 0,
                "affected": true,
                "disorders": ["Huntington Disease"],
                "parents": [2, 3],
                "siblings": [4],
                "children": []
            },
            ...
        ],
        "proband_id": 1
    }
    """
    try:
        data = request.get_json()
        
        family_data = data.get('family_data', [])
        proband_id = data.get('proband_id', 1)
        
        if not family_data:
            return jsonify({
                'success': False,
                'error': 'Family data is required'
            }), 400
        
        # Build pedigree
        pedigree = pedigree_ai.build_pedigree(family_data, proband_id)
        
        return jsonify({
            'success': True,
            'pedigree': pedigree
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@advanced_bp.route('/pedigree/simple', methods=['POST'])
def create_simple_pedigree():
    """
    Create simplified pedigree from assessment data
    
    Expected JSON:
    {
        "patient_data": {
            "name": "John Doe",
            "age": 35,
            "gender": "male",
            "disorders": ["Huntington Disease"]
        },
        "family_history": {
            "has_history": true,
            "affected_relatives": ["parent", "sibling"],
            "disorders": ["Huntington Disease"]
        }
    }
    """
    try:
        data = request.get_json()
        
        patient_data = data.get('patient_data', {})
        family_history = data.get('family_history', {})
        
        # Create simple pedigree
        pedigree = pedigree_ai.create_simple_pedigree_from_assessment(
            patient_data, family_history
        )
        
        return jsonify({
            'success': True,
            'pedigree': pedigree
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@advanced_bp.route('/pedigree/inheritance-patterns', methods=['GET'])
def get_inheritance_patterns():
    """Get information about genetic inheritance patterns"""
    try:
        return jsonify({
            'success': True,
            'patterns': pedigree_ai.inheritance_patterns
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@advanced_bp.route('/combined-analysis', methods=['POST'])
def combined_analysis():
    """
    Generate combined risk timeline and pedigree analysis
    
    Expected JSON:
    {
        "patient_data": {...},
        "family_history": {...},
        "current_risk_score": 65,
        "disorder": "Huntington Disease",
        "family_data": [...] (optional, for detailed pedigree)
    }
    """
    try:
        data = request.get_json()
        
        patient_data = data.get('patient_data', {})
        family_history = data.get('family_history', {})
        current_risk_score = data.get('current_risk_score', 50)
        disorder = data.get('disorder', 'Low Risk')
        family_data = data.get('family_data', None)
        
        # Generate risk timeline
        timeline = timeline_engine.generate_risk_timeline(
            current_age=patient_data.get('age', 30),
            disorder=disorder,
            current_risk_score=current_risk_score,
            family_history=family_history,
            lifestyle_data=patient_data.get('lifestyle', {})
        )
        
        # Generate pedigree
        if family_data:
            pedigree = pedigree_ai.build_pedigree(family_data, data.get('proband_id', 1))
        else:
            pedigree = pedigree_ai.create_simple_pedigree_from_assessment(
                patient_data, family_history
            )
        
        # Export chart data
        chart_data = timeline_engine.export_timeline_data(timeline)
        
        return jsonify({
            'success': True,
            'analysis': {
                'risk_timeline': timeline,
                'pedigree': pedigree,
                'chart_data': chart_data,
                'summary': {
                    'current_risk': current_risk_score,
                    'projected_5yr': timeline['projections']['5_year']['projected_risk_score'],
                    'projected_10yr': timeline['projections']['10_year']['projected_risk_score'],
                    'projected_20yr': timeline['projections']['20_year']['projected_risk_score'],
                    'inheritance_pattern': pedigree['inheritance_analysis']['primary_pattern'],
                    'high_risk_lines': len(pedigree['high_risk_lines'])
                }
            }
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ============================================================================
# ETHNICITY-AWARE RISK ADJUSTMENT ENDPOINTS
# ============================================================================

@advanced_bp.route('/ethnicity-risk-adjustment', methods=['POST'])
def adjust_risk_by_ethnicity():
    """
    Adjust genetic risk score based on ethnicity-specific prevalence
    
    Expected JSON:
    {
        "base_risk_score": 65,
        "disorder": "Sickle Cell Disease",
        "ethnicity": "African",
        "age": 35,
        "gender": "male"
    }
    """
    try:
        data = request.get_json()
        
        base_risk_score = data.get('base_risk_score', 50)
        disorder = data.get('disorder', '')
        ethnicity = data.get('ethnicity', '')
        age = data.get('age', None)
        gender = data.get('gender', None)
        
        if not disorder or not ethnicity:
            return jsonify({
                'success': False,
                'error': 'Disorder and ethnicity are required'
            }), 400
        
        # Adjust risk
        adjustment = ethnicity_adjuster.adjust_risk_by_ethnicity(
            base_risk_score=base_risk_score,
            disorder=disorder,
            ethnicity=ethnicity,
            age=age,
            gender=gender
        )
        
        return jsonify({
            'success': True,
            'adjustment': adjustment
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@advanced_bp.route('/population-statistics', methods=['POST'])
def get_population_statistics():
    """
    Get population-level statistics for a disorder and ethnicity
    
    Expected JSON:
    {
        "disorder": "Sickle Cell Disease",
        "ethnicity": "African"
    }
    """
    try:
        data = request.get_json()
        
        disorder = data.get('disorder', '')
        ethnicity = data.get('ethnicity', '')
        
        if not disorder or not ethnicity:
            return jsonify({
                'success': False,
                'error': 'Disorder and ethnicity are required'
            }), 400
        
        # Get statistics
        stats = ethnicity_adjuster.get_population_statistics(disorder, ethnicity)
        
        if not stats:
            return jsonify({
                'success': False,
                'error': 'No data available for this disorder/ethnicity combination'
            }), 404
        
        return jsonify({
            'success': True,
            'statistics': stats
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@advanced_bp.route('/ethnicity-comparison', methods=['POST'])
def compare_ethnicities():
    """
    Compare risk across different ethnicities for a disorder
    
    Expected JSON:
    {
        "disorder": "Thalassemia"
    }
    """
    try:
        data = request.get_json()
        
        disorder = data.get('disorder', '')
        
        if not disorder:
            return jsonify({
                'success': False,
                'error': 'Disorder is required'
            }), 400
        
        # Compare ethnicities
        comparison = ethnicity_adjuster.compare_ethnicities(disorder)
        
        return jsonify({
            'success': True,
            'comparison': comparison,
            'disorder': disorder
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ============================================================================
# SYNTHETIC GENOMIC PROFILE ENDPOINTS
# ============================================================================

@advanced_bp.route('/genomic-profile/generate', methods=['POST'])
def generate_genomic_profile():
    """
    Generate synthetic genomic profile without DNA testing
    
    Expected JSON:
    {
        "patient_data": {
            "age": 35,
            "gender": "male",
            "name": "John Doe"
        },
        "family_history": {
            "has_history": true,
            "disorders": ["Huntington Disease"],
            "affected_relatives": ["parent"]
        },
        "symptoms": ["muscle_weakness", "cognitive_impairment"],
        "ethnicity": "Caucasian"
    }
    """
    try:
        data = request.get_json()
        
        patient_data = data.get('patient_data', {})
        family_history = data.get('family_history', {})
        symptoms = data.get('symptoms', [])
        ethnicity = data.get('ethnicity', None)
        
        # Generate profile
        profile = genomic_generator.generate_profile(
            patient_data=patient_data,
            family_history=family_history,
            symptoms=symptoms,
            ethnicity=ethnicity
        )
        
        return jsonify({
            'success': True,
            'profile': profile
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@advanced_bp.route('/genomic-profile/carrier-analysis', methods=['POST'])
def analyze_carrier_status():
    """
    Analyze carrier probabilities for specific genes
    
    Expected JSON:
    {
        "genes": ["CFTR", "HBB", "BRCA1"],
        "family_history": {...},
        "ethnicity": "Caucasian"
    }
    """
    try:
        data = request.get_json()
        
        genes = data.get('genes', [])
        family_history = data.get('family_history', {})
        ethnicity = data.get('ethnicity', None)
        
        if not genes:
            return jsonify({
                'success': False,
                'error': 'At least one gene is required'
            }), 400
        
        # Calculate carrier probabilities
        carrier_probs = genomic_generator._calculate_carrier_probabilities(
            genes=genes,
            family_history=family_history,
            ethnicity=ethnicity
        )
        
        return jsonify({
            'success': True,
            'carrier_analysis': carrier_probs
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@advanced_bp.route('/genomic-profile/mutation-likelihood', methods=['POST'])
def estimate_mutation_likelihood():
    """
    Estimate likelihood of pathogenic mutations
    
    Expected JSON:
    {
        "genes": ["HTT", "BRCA1"],
        "family_history": {...},
        "symptoms": ["muscle_weakness"]
    }
    """
    try:
        data = request.get_json()
        
        genes = data.get('genes', [])
        family_history = data.get('family_history', {})
        symptoms = data.get('symptoms', [])
        
        if not genes:
            return jsonify({
                'success': False,
                'error': 'At least one gene is required'
            }), 400
        
        # Estimate mutation likelihood
        mutation_likelihood = genomic_generator._estimate_mutation_likelihood(
            genes=genes,
            family_history=family_history,
            symptoms=symptoms
        )
        
        return jsonify({
            'success': True,
            'mutation_analysis': mutation_likelihood
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@advanced_bp.route('/genomic-profile/pathway-map', methods=['POST'])
def generate_pathway_map():
    """
    Generate gene-pathway influence map
    
    Expected JSON:
    {
        "genes": ["BRCA1", "BRCA2", "HTT"]
    }
    """
    try:
        data = request.get_json()
        
        genes = data.get('genes', [])
        
        if not genes:
            return jsonify({
                'success': False,
                'error': 'At least one gene is required'
            }), 400
        
        # Generate pathway map
        pathway_map = genomic_generator._generate_pathway_map(genes)
        
        return jsonify({
            'success': True,
            'pathway_map': pathway_map
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@advanced_bp.route('/genomic-profile/chromosomal-risk', methods=['POST'])
def assess_chromosomal_risk():
    """
    Assess chromosomal anomaly risk
    
    Expected JSON:
    {
        "patient_data": {
            "age": 38,
            "gender": "female"
        },
        "family_history": {...}
    }
    """
    try:
        data = request.get_json()
        
        patient_data = data.get('patient_data', {})
        family_history = data.get('family_history', {})
        
        # Assess chromosomal risk
        chromosomal_risk = genomic_generator._assess_chromosomal_risk(
            patient_data=patient_data,
            family_history=family_history
        )
        
        return jsonify({
            'success': True,
            'chromosomal_risk': chromosomal_risk
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ============================================================================
# CLINICAL TEST RECOMMENDATION ENDPOINTS
# ============================================================================

@advanced_bp.route('/clinical-tests/recommend', methods=['POST'])
def recommend_clinical_tests():
    """
    Recommend clinical tests based on genetic risk assessment
    
    Expected JSON:
    {
        "disorder": "Huntington Disease",
        "risk_score": 65,
        "symptoms": ["muscle_weakness", "cognitive_impairment"],
        "age": 35,
        "gender": "male"
    }
    """
    try:
        data = request.get_json()
        
        disorder = data.get('disorder', '')
        risk_score = data.get('risk_score', 50)
        symptoms = data.get('symptoms', None)
        age = data.get('age', None)
        gender = data.get('gender', None)
        
        if not disorder:
            return jsonify({
                'success': False,
                'error': 'Disorder is required'
            }), 400
        
        # Recommend tests
        recommendations = test_recommender.recommend_tests(
            disorder=disorder,
            risk_score=risk_score,
            symptoms=symptoms,
            age=age,
            gender=gender
        )
        
        return jsonify({
            'success': True,
            'recommendations': recommendations
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@advanced_bp.route('/clinical-tests/test-info/<test_key>', methods=['GET'])
def get_test_info(test_key):
    """
    Get detailed information about a specific test
    """
    try:
        test_info = test_recommender.test_database.get(test_key)
        
        if not test_info:
            return jsonify({
                'success': False,
                'error': 'Test not found'
            }), 404
        
        return jsonify({
            'success': True,
            'test_info': test_info
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@advanced_bp.route('/clinical-tests/categories', methods=['GET'])
def get_test_categories():
    """
    Get all available test categories
    """
    try:
        categories = {}
        for test_key, test_data in test_recommender.test_database.items():
            category = test_data['category']
            if category not in categories:
                categories[category] = []
            categories[category].append({
                'key': test_key,
                'name': test_data['name'],
                'cost_range': test_data['cost_range']
            })
        
        return jsonify({
            'success': True,
            'categories': categories
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ============================================================================
# COMPREHENSIVE ANALYSIS ENDPOINT
# ============================================================================

@advanced_bp.route('/comprehensive-analysis', methods=['POST'])
def comprehensive_analysis():
    """
    Generate comprehensive analysis including all advanced features
    
    Expected JSON:
    {
        "patient_data": {
            "name": "John Doe",
            "age": 35,
            "gender": "male"
        },
        "family_history": {...},
        "symptoms": [...],
        "ethnicity": "Caucasian",
        "disorder": "Huntington Disease",
        "base_risk_score": 65,
        "lifestyle_data": {...}
    }
    """
    try:
        data = request.get_json()
        
        patient_data = data.get('patient_data', {})
        family_history = data.get('family_history', {})
        symptoms = data.get('symptoms', [])
        ethnicity = data.get('ethnicity', '')
        disorder = data.get('disorder', '')
        base_risk_score = data.get('base_risk_score', 50)
        lifestyle_data = data.get('lifestyle_data', {})
        
        # 1. Ethnicity-adjusted risk
        ethnicity_adjustment = ethnicity_adjuster.adjust_risk_by_ethnicity(
            base_risk_score=base_risk_score,
            disorder=disorder,
            ethnicity=ethnicity,
            age=patient_data.get('age'),
            gender=patient_data.get('gender')
        )
        
        adjusted_risk = ethnicity_adjustment['adjusted_risk_score']
        
        # 2. Risk timeline
        timeline = timeline_engine.generate_risk_timeline(
            current_age=patient_data.get('age', 30),
            disorder=disorder,
            current_risk_score=adjusted_risk,
            family_history=family_history,
            lifestyle_data=lifestyle_data
        )
        
        # 3. Genomic profile
        genomic_profile = genomic_generator.generate_profile(
            patient_data=patient_data,
            family_history=family_history,
            symptoms=symptoms,
            ethnicity=ethnicity
        )
        
        # 4. Clinical test recommendations
        test_recommendations = test_recommender.recommend_tests(
            disorder=disorder,
            risk_score=adjusted_risk,
            symptoms=symptoms,
            age=patient_data.get('age'),
            gender=patient_data.get('gender')
        )
        
        # 5. Family pedigree
        pedigree = pedigree_ai.create_simple_pedigree_from_assessment(
            patient_data, family_history
        )
        
        # Compile comprehensive report
        comprehensive_report = {
            'patient_info': patient_data,
            'risk_assessment': {
                'base_risk_score': base_risk_score,
                'ethnicity_adjusted_risk': adjusted_risk,
                'adjustment_details': ethnicity_adjustment,
                'risk_timeline': timeline
            },
            'genomic_analysis': genomic_profile,
            'clinical_recommendations': test_recommendations,
            'family_analysis': pedigree,
            'summary': {
                'overall_risk_level': timeline['projections']['5_year']['risk_level'],
                'key_genes_of_concern': list(genomic_profile['carrier_probabilities'].keys())[:5],
                'urgent_tests': len([t for t in test_recommendations['recommended_tests'] if t['priority'] == 'Urgent']),
                'total_recommended_tests': len(test_recommendations['recommended_tests']),
                'inheritance_pattern': pedigree['inheritance_analysis']['primary_pattern']['pattern'],
                'ethnicity_impact': f"{ethnicity_adjustment['adjustment_factor']}x"
            }
        }
        
        return jsonify({
            'success': True,
            'comprehensive_analysis': comprehensive_report
        })
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
