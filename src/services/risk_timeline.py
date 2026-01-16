"""
AI-Generated Personal Genetic Risk Timeline (Future Projection Engine)
Generates risk progression curves and lifestyle-based simulations
"""

import numpy as np
from datetime import datetime, timedelta
import json

class RiskTimelineEngine:
    """
    Advanced risk projection engine that generates:
    - Risk progression curves over 5, 10, 20 years
    - Age-adjusted disorder probability trajectories
    - Lifestyle-based future risk simulations
    - What-if scenario analysis
    """
    
    def __init__(self):
        # Age-based risk multipliers for different genetic disorders
        self.age_risk_factors = {
            'Down Syndrome': {'base': 0.1, 'progression': 0.02},
            'Cystic Fibrosis': {'base': 1.0, 'progression': 0.05},
            'Sickle Cell Anemia': {'base': 1.0, 'progression': 0.08},
            'Huntington Disease': {'base': 0.3, 'progression': 0.15},
            'Hemophilia': {'base': 1.0, 'progression': 0.03},
            'Thalassemia': {'base': 1.0, 'progression': 0.06},
            'Muscular Dystrophy': {'base': 0.8, 'progression': 0.12},
            'Hemoglobinopathy': {'base': 1.0, 'progression': 0.07},
            'Neurodevelopmental Genetic Disorder': {'base': 0.5, 'progression': 0.08},
            'Low Risk': {'base': 0.1, 'progression': 0.01}
        }
        
        # Lifestyle impact factors (percentage change in risk)
        self.lifestyle_factors = {
            'weight_loss': -0.15,  # 15% risk reduction
            'weight_gain': 0.12,
            'quit_smoking': -0.25,
            'start_smoking': 0.30,
            'regular_exercise': -0.20,
            'stop_exercise': 0.15,
            'healthy_diet': -0.18,
            'poor_diet': 0.14,
            'stress_reduction': -0.10,
            'high_stress': 0.12,
            'medication_adherence': -0.22,
            'skip_medication': 0.25
        }
    
    def generate_risk_timeline(self, current_age, disorder, current_risk_score, family_history, lifestyle_data=None):
        """
        Generate comprehensive risk timeline with projections
        
        Args:
            current_age: Patient's current age
            disorder: Predicted genetic disorder
            current_risk_score: Current risk score (0-100)
            family_history: Family history data
            lifestyle_data: Current lifestyle factors
        
        Returns:
            Dictionary with timeline projections and analysis
        """
        # Generate projections for 5, 10, 20 years
        projections = {
            '5_year': self._calculate_projection(current_age, disorder, current_risk_score, 5, family_history),
            '10_year': self._calculate_projection(current_age, disorder, current_risk_score, 10, family_history),
            '20_year': self._calculate_projection(current_age, disorder, current_risk_score, 20, family_history)
        }
        
        # Generate year-by-year progression curve
        progression_curve = self._generate_progression_curve(
            current_age, disorder, current_risk_score, 20, family_history
        )
        
        # Generate what-if scenarios
        what_if_scenarios = self._generate_what_if_scenarios(
            current_age, disorder, current_risk_score, family_history, lifestyle_data
        )
        
        # Calculate critical age milestones
        milestones = self._calculate_milestones(current_age, disorder, progression_curve)
        
        # Generate lifestyle recommendations with impact
        lifestyle_recommendations = self._generate_lifestyle_impact(disorder, current_risk_score)
        
        return {
            'current_age': current_age,
            'disorder': disorder,
            'current_risk_score': current_risk_score,
            'projections': projections,
            'progression_curve': progression_curve,
            'what_if_scenarios': what_if_scenarios,
            'milestones': milestones,
            'lifestyle_recommendations': lifestyle_recommendations,
            'generated_at': datetime.now().isoformat()
        }
    
    def _calculate_projection(self, current_age, disorder, current_risk, years, family_history):
        """Calculate risk projection for specific time period"""
        # Get disorder-specific factors
        factors = self.age_risk_factors.get(disorder, self.age_risk_factors['Low Risk'])
        
        # Base progression
        age_factor = (current_age + years) / 100
        progression_rate = factors['progression']
        
        # Family history impact
        family_multiplier = 1.0
        if family_history.get('has_history', False):
            family_multiplier = 1.3
            if 'parent' in family_history.get('affected_relatives', []):
                family_multiplier = 1.5
        
        # Calculate projected risk
        projected_risk = current_risk * (1 + (progression_rate * years * family_multiplier))
        projected_risk = min(projected_risk, 100)  # Cap at 100
        
        # Calculate probability of manifestation
        manifestation_probability = self._calculate_manifestation_probability(
            current_age + years, disorder, projected_risk
        )
        
        # Risk level
        risk_level = self._get_risk_level(projected_risk)
        
        return {
            'years_ahead': years,
            'projected_age': current_age + years,
            'projected_risk_score': round(projected_risk, 2),
            'risk_level': risk_level,
            'manifestation_probability': round(manifestation_probability, 2),
            'risk_increase': round(projected_risk - current_risk, 2),
            'confidence_interval': {
                'lower': round(projected_risk * 0.85, 2),
                'upper': round(projected_risk * 1.15, 2)
            }
        }
    
    def _generate_progression_curve(self, current_age, disorder, current_risk, years, family_history):
        """Generate year-by-year risk progression curve"""
        curve = []
        
        for year in range(years + 1):
            projection = self._calculate_projection(current_age, disorder, current_risk, year, family_history)
            curve.append({
                'year': year,
                'age': current_age + year,
                'risk_score': projection['projected_risk_score'],
                'manifestation_probability': projection['manifestation_probability']
            })
        
        return curve
    
    def _calculate_manifestation_probability(self, age, disorder, risk_score):
        """Calculate probability of disorder manifestation at given age"""
        # Age-specific manifestation curves
        if disorder == 'Huntington Disease':
            # Typically manifests 30-50 years
            if age < 30:
                age_factor = 0.1
            elif age < 50:
                age_factor = 0.8
            else:
                age_factor = 0.95
        elif disorder in ['Muscular Dystrophy', 'Cystic Fibrosis']:
            # Early onset
            if age < 10:
                age_factor = 0.7
            elif age < 30:
                age_factor = 0.9
            else:
                age_factor = 0.95
        else:
            # General curve
            age_factor = min(age / 100, 0.9)
        
        # Combine with risk score
        probability = (risk_score / 100) * age_factor * 100
        return min(probability, 95)  # Cap at 95%
    
    def _generate_what_if_scenarios(self, current_age, disorder, current_risk, family_history, lifestyle_data):
        """Generate what-if scenario simulations"""
        scenarios = []
        
        # Scenario 1: Weight reduction
        scenarios.append(self._simulate_lifestyle_change(
            'Weight Loss (10-15%)',
            current_age, disorder, current_risk, family_history,
            ['weight_loss', 'regular_exercise', 'healthy_diet']
        ))
        
        # Scenario 2: Quit smoking
        scenarios.append(self._simulate_lifestyle_change(
            'Quit Smoking',
            current_age, disorder, current_risk, family_history,
            ['quit_smoking', 'regular_exercise']
        ))
        
        # Scenario 3: Comprehensive lifestyle improvement
        scenarios.append(self._simulate_lifestyle_change(
            'Comprehensive Lifestyle Improvement',
            current_age, disorder, current_risk, family_history,
            ['weight_loss', 'quit_smoking', 'regular_exercise', 'healthy_diet', 'stress_reduction']
        ))
        
        # Scenario 4: Medication adherence
        scenarios.append(self._simulate_lifestyle_change(
            'Strict Medication Adherence',
            current_age, disorder, current_risk, family_history,
            ['medication_adherence', 'healthy_diet', 'regular_exercise']
        ))
        
        # Scenario 5: No lifestyle changes (baseline)
        scenarios.append(self._simulate_lifestyle_change(
            'No Changes (Current Trajectory)',
            current_age, disorder, current_risk, family_history,
            []
        ))
        
        # Scenario 6: Negative lifestyle changes
        scenarios.append(self._simulate_lifestyle_change(
            'Negative Lifestyle Changes',
            current_age, disorder, current_risk, family_history,
            ['weight_gain', 'stop_exercise', 'poor_diet', 'high_stress']
        ))
        
        return scenarios
    
    def _simulate_lifestyle_change(self, scenario_name, current_age, disorder, current_risk, family_history, changes):
        """Simulate impact of lifestyle changes on risk"""
        # Calculate cumulative impact
        total_impact = sum(self.lifestyle_factors.get(change, 0) for change in changes)
        
        # Apply impact to current risk
        modified_risk = current_risk * (1 + total_impact)
        modified_risk = max(5, min(modified_risk, 100))  # Keep between 5-100
        
        # Generate 10-year projection with modified risk
        projection_10yr = self._calculate_projection(
            current_age, disorder, modified_risk, 10, family_history
        )
        
        # Calculate benefit
        baseline_10yr = self._calculate_projection(
            current_age, disorder, current_risk, 10, family_history
        )
        
        risk_reduction = baseline_10yr['projected_risk_score'] - projection_10yr['projected_risk_score']
        
        return {
            'scenario': scenario_name,
            'changes': changes,
            'impact_percentage': round(total_impact * 100, 1),
            'modified_current_risk': round(modified_risk, 2),
            'projected_10yr_risk': projection_10yr['projected_risk_score'],
            'baseline_10yr_risk': baseline_10yr['projected_risk_score'],
            'risk_reduction': round(risk_reduction, 2),
            'years_of_life_quality_gained': round(abs(risk_reduction) / 5, 1) if risk_reduction > 0 else 0
        }
    
    def _calculate_milestones(self, current_age, disorder, progression_curve):
        """Calculate critical age milestones"""
        milestones = []
        
        # Find when risk crosses thresholds
        thresholds = [
            {'level': 'Moderate', 'value': 30},
            {'level': 'High', 'value': 60},
            {'level': 'Critical', 'value': 80}
        ]
        
        for threshold in thresholds:
            for point in progression_curve:
                if point['risk_score'] >= threshold['value']:
                    milestones.append({
                        'age': point['age'],
                        'years_from_now': point['year'],
                        'risk_level': threshold['level'],
                        'risk_score': point['risk_score'],
                        'description': f"Risk reaches {threshold['level']} level"
                    })
                    break
        
        # Add disorder-specific milestones
        if disorder == 'Huntington Disease':
            milestones.append({
                'age': 40,
                'years_from_now': max(0, 40 - current_age),
                'risk_level': 'Critical',
                'description': 'Typical onset age for Huntington Disease'
            })
        
        return milestones
    
    def _generate_lifestyle_impact(self, disorder, current_risk):
        """Generate lifestyle recommendations with quantified impact"""
        recommendations = []
        
        # Weight management
        recommendations.append({
            'category': 'Weight Management',
            'action': 'Achieve and maintain healthy BMI (18.5-24.9)',
            'impact': 'Up to 15% risk reduction',
            'priority': 'High',
            'timeframe': '6-12 months',
            'expected_benefit': round(current_risk * 0.15, 1)
        })
        
        # Exercise
        recommendations.append({
            'category': 'Physical Activity',
            'action': '150 minutes moderate exercise per week',
            'impact': 'Up to 20% risk reduction',
            'priority': 'High',
            'timeframe': '3-6 months',
            'expected_benefit': round(current_risk * 0.20, 1)
        })
        
        # Smoking cessation
        recommendations.append({
            'category': 'Smoking Cessation',
            'action': 'Complete smoking cessation',
            'impact': 'Up to 25% risk reduction',
            'priority': 'Critical',
            'timeframe': 'Immediate',
            'expected_benefit': round(current_risk * 0.25, 1)
        })
        
        # Diet
        recommendations.append({
            'category': 'Nutrition',
            'action': 'Mediterranean or DASH diet',
            'impact': 'Up to 18% risk reduction',
            'priority': 'High',
            'timeframe': '3-6 months',
            'expected_benefit': round(current_risk * 0.18, 1)
        })
        
        # Stress management
        recommendations.append({
            'category': 'Stress Management',
            'action': 'Regular meditation, yoga, or counseling',
            'impact': 'Up to 10% risk reduction',
            'priority': 'Moderate',
            'timeframe': '1-3 months',
            'expected_benefit': round(current_risk * 0.10, 1)
        })
        
        # Medication adherence
        if current_risk > 50:
            recommendations.append({
                'category': 'Medical Management',
                'action': 'Strict medication adherence and regular monitoring',
                'impact': 'Up to 22% risk reduction',
                'priority': 'Critical',
                'timeframe': 'Ongoing',
                'expected_benefit': round(current_risk * 0.22, 1)
            })
        
        return recommendations
    
    def _get_risk_level(self, risk_score):
        """Categorize risk level"""
        if risk_score < 30:
            return 'Low'
        elif risk_score < 60:
            return 'Moderate'
        elif risk_score < 80:
            return 'High'
        else:
            return 'Critical'
    
    def export_timeline_data(self, timeline_data):
        """Export timeline data for visualization"""
        return {
            'chart_data': {
                'labels': [point['age'] for point in timeline_data['progression_curve']],
                'risk_scores': [point['risk_score'] for point in timeline_data['progression_curve']],
                'manifestation_prob': [point['manifestation_probability'] for point in timeline_data['progression_curve']]
            },
            'scenarios_comparison': [
                {
                    'name': scenario['scenario'],
                    'risk_10yr': scenario['projected_10yr_risk']
                }
                for scenario in timeline_data['what_if_scenarios']
            ]
        }
