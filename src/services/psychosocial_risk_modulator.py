"""
Psychosocial Risk Modulator - Mental Health × Genetic Interaction Modeling
Integrates psychology + genetics for holistic risk assessment
"""
import random
from datetime import datetime
from typing import Dict, List, Any


class PsychosocialRiskModulator:
    """
    Models the interaction between mental health, lifestyle, and genetic risk.
    Provides holistic assessment considering psychological factors.
    """
    
    def __init__(self):
        # Stress impact multipliers on genetic expression
        self.stress_impact_factors = {
            'none': 0.9,
            'low': 1.0,
            'moderate': 1.15,
            'high': 1.3,
            'severe': 1.5
        }
        
        # Mental health condition impacts
        self.mental_health_modifiers = {
            'depression': {
                'immune_disorders': 1.25,
                'cardiovascular': 1.35,
                'metabolic': 1.20,
                'neurological': 1.40
            },
            'anxiety': {
                'cardiovascular': 1.30,
                'gastrointestinal': 1.25,
                'immune_disorders': 1.20,
                'neurological': 1.15
            },
            'ptsd': {
                'neurological': 1.45,
                'cardiovascular': 1.30,
                'immune_disorders': 1.35
            },
            'bipolar': {
                'neurological': 1.40,
                'metabolic': 1.25,
                'cardiovascular': 1.20
            }
        }
        
        # Lifestyle factors
        self.lifestyle_factors = {
            'sleep_quality': {
                'poor': 1.25,
                'fair': 1.10,
                'good': 1.0,
                'excellent': 0.90
            },
            'social_support': {
                'isolated': 1.30,
                'limited': 1.15,
                'moderate': 1.0,
                'strong': 0.85
            },
            'work_stress': {
                'overwhelming': 1.35,
                'high': 1.20,
                'moderate': 1.05,
                'low': 0.95
            },
            'coping_mechanisms': {
                'poor': 1.30,
                'developing': 1.15,
                'adequate': 1.0,
                'strong': 0.85
            }
        }
    
    def calculate_psychosocial_adjustment(
        self,
        base_risk_score: float,
        disorder_category: str,
        mental_health_data: Dict[str, Any],
        lifestyle_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Calculate adjusted risk score considering psychosocial factors.
        
        Args:
            base_risk_score: Initial genetic risk score (0-100)
            disorder_category: Category of disorder (neurological, cardiovascular, etc.)
            mental_health_data: Mental health assessment data
            lifestyle_data: Lifestyle and stress factors
        
        Returns:
            Comprehensive psychosocial risk assessment
        """
        
        # Extract data
        stress_level = mental_health_data.get('stress_level', 'moderate')
        mental_conditions = mental_health_data.get('conditions', [])
        sleep_quality = lifestyle_data.get('sleep_quality', 'fair')
        social_support = lifestyle_data.get('social_support', 'moderate')
        work_stress = lifestyle_data.get('work_stress', 'moderate')
        coping = lifestyle_data.get('coping_mechanisms', 'adequate')
        
        # Start with base risk
        adjusted_risk = base_risk_score
        
        # Apply stress impact
        stress_multiplier = self.stress_impact_factors.get(stress_level, 1.0)
        adjusted_risk *= stress_multiplier
        
        # Apply mental health condition impacts
        mental_health_multiplier = 1.0
        for condition in mental_conditions:
            if condition in self.mental_health_modifiers:
                condition_impact = self.mental_health_modifiers[condition].get(
                    disorder_category, 1.0
                )
                mental_health_multiplier *= condition_impact
        
        adjusted_risk *= mental_health_multiplier
        
        # Apply lifestyle factors
        lifestyle_multiplier = 1.0
        lifestyle_multiplier *= self.lifestyle_factors['sleep_quality'].get(sleep_quality, 1.0)
        lifestyle_multiplier *= self.lifestyle_factors['social_support'].get(social_support, 1.0)
        lifestyle_multiplier *= self.lifestyle_factors['work_stress'].get(work_stress, 1.0)
        lifestyle_multiplier *= self.lifestyle_factors['coping_mechanisms'].get(coping, 1.0)
        
        adjusted_risk *= lifestyle_multiplier
        
        # Cap at 100
        adjusted_risk = min(adjusted_risk, 100)
        
        # Calculate individual contributions
        stress_contribution = (stress_multiplier - 1.0) * base_risk_score
        mental_health_contribution = (mental_health_multiplier - 1.0) * base_risk_score
        lifestyle_contribution = (lifestyle_multiplier - 1.0) * base_risk_score
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            stress_level, mental_conditions, lifestyle_data
        )
        
        # Calculate protective factors
        protective_factors = self._identify_protective_factors(lifestyle_data)
        
        # Calculate risk factors
        risk_factors = self._identify_risk_factors(
            stress_level, mental_conditions, lifestyle_data
        )
        
        return {
            'success': True,
            'base_risk_score': round(base_risk_score, 2),
            'adjusted_risk_score': round(adjusted_risk, 2),
            'risk_change': round(adjusted_risk - base_risk_score, 2),
            'risk_change_percentage': round(
                ((adjusted_risk - base_risk_score) / base_risk_score * 100), 2
            ) if base_risk_score > 0 else 0,
            'multipliers': {
                'stress_impact': round(stress_multiplier, 3),
                'mental_health_impact': round(mental_health_multiplier, 3),
                'lifestyle_impact': round(lifestyle_multiplier, 3),
                'combined_impact': round(
                    stress_multiplier * mental_health_multiplier * lifestyle_multiplier, 3
                )
            },
            'contributions': {
                'stress': round(stress_contribution, 2),
                'mental_health': round(mental_health_contribution, 2),
                'lifestyle': round(lifestyle_contribution, 2)
            },
            'protective_factors': protective_factors,
            'risk_factors': risk_factors,
            'recommendations': recommendations,
            'intervention_priority': self._determine_priority(adjusted_risk),
            'holistic_score': self._calculate_holistic_score(
                adjusted_risk, protective_factors, risk_factors
            ),
            'timestamp': datetime.now().isoformat()
        }
    
    def _generate_recommendations(
        self,
        stress_level: str,
        mental_conditions: List[str],
        lifestyle_data: Dict[str, Any]
    ) -> List[Dict[str, str]]:
        """Generate personalized psychosocial recommendations."""
        recommendations = []
        
        # Stress management
        if stress_level in ['high', 'severe']:
            recommendations.append({
                'category': 'Stress Management',
                'priority': 'High',
                'recommendation': 'Immediate stress reduction intervention recommended',
                'actions': [
                    'Consider professional counseling or therapy',
                    'Practice daily mindfulness or meditation (20 minutes)',
                    'Engage in regular physical activity (30 minutes daily)',
                    'Explore stress management workshops or programs'
                ]
            })
        
        # Mental health support
        if mental_conditions:
            recommendations.append({
                'category': 'Mental Health',
                'priority': 'High',
                'recommendation': 'Continue mental health treatment and monitoring',
                'actions': [
                    'Maintain regular appointments with mental health professional',
                    'Consider medication review if applicable',
                    'Join support groups for peer connection',
                    'Practice self-care routines daily'
                ]
            })
        
        # Sleep improvement
        if lifestyle_data.get('sleep_quality') in ['poor', 'fair']:
            recommendations.append({
                'category': 'Sleep Hygiene',
                'priority': 'Moderate',
                'recommendation': 'Improve sleep quality to reduce genetic risk expression',
                'actions': [
                    'Establish consistent sleep schedule (7-9 hours)',
                    'Create relaxing bedtime routine',
                    'Limit screen time before bed',
                    'Consider sleep study if problems persist'
                ]
            })
        
        # Social support
        if lifestyle_data.get('social_support') in ['isolated', 'limited']:
            recommendations.append({
                'category': 'Social Connection',
                'priority': 'Moderate',
                'recommendation': 'Build stronger social support network',
                'actions': [
                    'Join community groups or clubs',
                    'Reconnect with friends and family',
                    'Consider group therapy or support groups',
                    'Volunteer for meaningful causes'
                ]
            })
        
        # Coping skills
        if lifestyle_data.get('coping_mechanisms') in ['poor', 'developing']:
            recommendations.append({
                'category': 'Coping Skills',
                'priority': 'Moderate',
                'recommendation': 'Develop healthier coping mechanisms',
                'actions': [
                    'Learn and practice relaxation techniques',
                    'Develop problem-solving skills',
                    'Engage in creative or expressive activities',
                    'Consider cognitive-behavioral therapy (CBT)'
                ]
            })
        
        return recommendations
    
    def _identify_protective_factors(
        self,
        lifestyle_data: Dict[str, Any]
    ) -> List[Dict[str, str]]:
        """Identify protective psychosocial factors."""
        protective = []
        
        if lifestyle_data.get('sleep_quality') in ['good', 'excellent']:
            protective.append({
                'factor': 'Quality Sleep',
                'impact': 'Reduces genetic risk expression by 10-15%',
                'description': 'Good sleep supports DNA repair and immune function'
            })
        
        if lifestyle_data.get('social_support') in ['moderate', 'strong']:
            protective.append({
                'factor': 'Strong Social Support',
                'impact': 'Reduces stress-related genetic activation',
                'description': 'Social connections buffer against stress and improve health outcomes'
            })
        
        if lifestyle_data.get('coping_mechanisms') in ['adequate', 'strong']:
            protective.append({
                'factor': 'Effective Coping Skills',
                'impact': 'Mitigates stress impact on gene expression',
                'description': 'Healthy coping reduces inflammation and oxidative stress'
            })
        
        if lifestyle_data.get('work_stress') == 'low':
            protective.append({
                'factor': 'Low Work Stress',
                'impact': 'Maintains healthy stress hormone levels',
                'description': 'Reduced cortisol levels support overall health'
            })
        
        return protective
    
    def _identify_risk_factors(
        self,
        stress_level: str,
        mental_conditions: List[str],
        lifestyle_data: Dict[str, Any]
    ) -> List[Dict[str, str]]:
        """Identify psychosocial risk factors."""
        risks = []
        
        if stress_level in ['high', 'severe']:
            risks.append({
                'factor': 'Chronic Stress',
                'impact': 'Increases genetic risk expression by 30-50%',
                'description': 'Chronic stress activates inflammatory pathways and affects gene expression'
            })
        
        if mental_conditions:
            risks.append({
                'factor': f'Mental Health Conditions ({len(mental_conditions)})',
                'impact': 'Amplifies genetic susceptibility',
                'description': 'Mental health conditions can trigger or worsen genetic predispositions'
            })
        
        if lifestyle_data.get('sleep_quality') == 'poor':
            risks.append({
                'factor': 'Poor Sleep Quality',
                'impact': 'Increases risk by 25%',
                'description': 'Sleep deprivation impairs DNA repair and immune function'
            })
        
        if lifestyle_data.get('social_support') == 'isolated':
            risks.append({
                'factor': 'Social Isolation',
                'impact': 'Increases risk by 30%',
                'description': 'Isolation increases stress hormones and inflammation'
            })
        
        return risks
    
    def _determine_priority(self, adjusted_risk: float) -> str:
        """Determine intervention priority level."""
        if adjusted_risk >= 70:
            return 'Urgent - Immediate psychosocial intervention recommended'
        elif adjusted_risk >= 50:
            return 'High - Psychosocial support strongly recommended'
        elif adjusted_risk >= 30:
            return 'Moderate - Preventive psychosocial care beneficial'
        else:
            return 'Low - Maintain current healthy practices'
    
    def _calculate_holistic_score(
        self,
        adjusted_risk: float,
        protective_factors: List[Dict],
        risk_factors: List[Dict]
    ) -> Dict[str, Any]:
        """Calculate overall holistic health score."""
        
        # Base score from adjusted risk (inverted)
        base_score = 100 - adjusted_risk
        
        # Bonus for protective factors
        protective_bonus = len(protective_factors) * 5
        
        # Penalty for risk factors
        risk_penalty = len(risk_factors) * 5
        
        holistic_score = base_score + protective_bonus - risk_penalty
        holistic_score = max(0, min(100, holistic_score))
        
        return {
            'score': round(holistic_score, 2),
            'rating': self._get_rating(holistic_score),
            'protective_count': len(protective_factors),
            'risk_count': len(risk_factors),
            'balance': 'Positive' if len(protective_factors) > len(risk_factors) else 'Negative'
        }
    
    def _get_rating(self, score: float) -> str:
        """Get rating based on holistic score."""
        if score >= 80:
            return 'Excellent'
        elif score >= 60:
            return 'Good'
        elif score >= 40:
            return 'Fair'
        elif score >= 20:
            return 'Poor'
        else:
            return 'Critical'
    
    def generate_tri_model_analysis(
        self,
        genetic_data: Dict[str, Any],
        mental_health_data: Dict[str, Any],
        lifestyle_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate comprehensive tri-model analysis:
        Genetics × Mental Health × Lifestyle
        """
        
        base_risk = genetic_data.get('risk_score', 50)
        disorder_category = genetic_data.get('category', 'general')
        
        # Calculate adjusted risk
        adjustment = self.calculate_psychosocial_adjustment(
            base_risk, disorder_category, mental_health_data, lifestyle_data
        )
        
        # Generate interaction insights
        interactions = self._analyze_interactions(
            genetic_data, mental_health_data, lifestyle_data
        )
        
        return {
            'success': True,
            'tri_model_analysis': {
                'genetic_component': {
                    'base_risk': base_risk,
                    'disorder': genetic_data.get('disorder', 'Unknown'),
                    'category': disorder_category
                },
                'mental_health_component': {
                    'stress_level': mental_health_data.get('stress_level'),
                    'conditions': mental_health_data.get('conditions', []),
                    'impact_multiplier': adjustment['multipliers']['mental_health_impact']
                },
                'lifestyle_component': {
                    'sleep_quality': lifestyle_data.get('sleep_quality'),
                    'social_support': lifestyle_data.get('social_support'),
                    'work_stress': lifestyle_data.get('work_stress'),
                    'impact_multiplier': adjustment['multipliers']['lifestyle_impact']
                },
                'integrated_risk': adjustment['adjusted_risk_score'],
                'interactions': interactions,
                'holistic_assessment': adjustment['holistic_score']
            },
            'recommendations': adjustment['recommendations'],
            'priority': adjustment['intervention_priority']
        }
    
    def _analyze_interactions(
        self,
        genetic_data: Dict,
        mental_health_data: Dict,
        lifestyle_data: Dict
    ) -> List[Dict[str, str]]:
        """Analyze interactions between the three components."""
        interactions = []
        
        # Genetics × Mental Health
        if mental_health_data.get('conditions'):
            interactions.append({
                'type': 'Genetics × Mental Health',
                'description': 'Mental health conditions may amplify genetic predispositions through stress pathways',
                'strength': 'Strong',
                'recommendation': 'Integrated care addressing both genetic and mental health factors'
            })
        
        # Mental Health × Lifestyle
        if mental_health_data.get('stress_level') in ['high', 'severe'] and \
           lifestyle_data.get('sleep_quality') in ['poor', 'fair']:
            interactions.append({
                'type': 'Mental Health × Lifestyle',
                'description': 'Poor sleep quality exacerbates stress and mental health symptoms',
                'strength': 'Moderate',
                'recommendation': 'Prioritize sleep hygiene to improve mental health outcomes'
            })
        
        # Genetics × Lifestyle
        if lifestyle_data.get('social_support') in ['isolated', 'limited']:
            interactions.append({
                'type': 'Genetics × Lifestyle',
                'description': 'Social isolation may trigger genetic risk factors through chronic stress',
                'strength': 'Moderate',
                'recommendation': 'Build social connections to buffer genetic vulnerabilities'
            })
        
        # Three-way interaction
        if mental_health_data.get('stress_level') in ['high', 'severe'] and \
           lifestyle_data.get('coping_mechanisms') in ['poor', 'developing']:
            interactions.append({
                'type': 'Genetics × Mental Health × Lifestyle',
                'description': 'High stress with poor coping skills creates optimal conditions for genetic risk expression',
                'strength': 'Very Strong',
                'recommendation': 'Comprehensive intervention addressing all three domains simultaneously'
            })
        
        return interactions
