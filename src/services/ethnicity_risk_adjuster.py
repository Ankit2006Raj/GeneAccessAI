"""
Population-Level Genetic Risk Adjuster (Ethnicity-Aware Risk Model)
Industry-grade risk adjustment based on population genetics and ethnicity-specific prevalence
"""

class EthnicityRiskAdjuster:
    """
    Adjusts genetic risk scores based on ethnicity-specific disease prevalence
    Similar to 23andMe's population-based risk models
    """
    
    def __init__(self):
        # Population-specific disease prevalence data (per 100,000)
        self.ethnicity_prevalence = {
            'south_asian': {
                'type_2_diabetes': {'prevalence': 15.5, 'relative_risk': 2.5},
                'coronary_artery_disease': {'prevalence': 12.3, 'relative_risk': 2.0},
                'thalassemia': {'prevalence': 8.5, 'relative_risk': 3.5},
                'g6pd_deficiency': {'prevalence': 6.2, 'relative_risk': 2.8},
                'familial_hypercholesterolemia': {'prevalence': 4.1, 'relative_risk': 1.8}
            },
            'african': {
                'sickle_cell_disease': {'prevalence': 25.0, 'relative_risk': 50.0},
                'sickle_cell_trait': {'prevalence': 80.0, 'relative_risk': 10.0},
                'hypertension': {'prevalence': 18.5, 'relative_risk': 2.2},
                'prostate_cancer': {'prevalence': 14.2, 'relative_risk': 2.4},
                'g6pd_deficiency': {'prevalence': 12.0, 'relative_risk': 4.0},
                'keloid_formation': {'prevalence': 6.5, 'relative_risk': 3.0}
            },
            'caucasian': {
                'cystic_fibrosis': {'prevalence': 3.5, 'relative_risk': 25.0},
                'hemochromatosis': {'prevalence': 5.0, 'relative_risk': 10.0},
                'celiac_disease': {'prevalence': 10.0, 'relative_risk': 3.0},
                'multiple_sclerosis': {'prevalence': 8.5, 'relative_risk': 2.5},
                'melanoma': {'prevalence': 12.0, 'relative_risk': 3.5},
                'type_1_diabetes': {'prevalence': 6.0, 'relative_risk': 2.0}
            },
            'hispanic': {
                'type_2_diabetes': {'prevalence': 14.0, 'relative_risk': 2.2},
                'gallbladder_disease': {'prevalence': 8.5, 'relative_risk': 2.8},
                'obesity': {'prevalence': 22.0, 'relative_risk': 1.8},
                'thalassemia': {'prevalence': 4.5, 'relative_risk': 2.0},
                'lactose_intolerance': {'prevalence': 50.0, 'relative_risk': 5.0}
            },
            'east_asian': {
                'thalassemia': {'prevalence': 15.0, 'relative_risk': 5.0},
                'g6pd_deficiency': {'prevalence': 10.0, 'relative_risk': 3.5},
                'lactose_intolerance': {'prevalence': 90.0, 'relative_risk': 9.0},
                'nasopharyngeal_carcinoma': {'prevalence': 3.5, 'relative_risk': 10.0},
                'hepatitis_b': {'prevalence': 8.0, 'relative_risk': 4.0}
            },
            'middle_eastern': {
                'thalassemia': {'prevalence': 12.0, 'relative_risk': 4.5},
                'familial_mediterranean_fever': {'prevalence': 10.0, 'relative_risk': 20.0},
                'g6pd_deficiency': {'prevalence': 8.5, 'relative_risk': 3.0},
                'consanguinity_related_disorders': {'prevalence': 15.0, 'relative_risk': 5.0},
                'behcets_disease': {'prevalence': 4.2, 'relative_risk': 8.0}
            },
            'ashkenazi_jewish': {
                'tay_sachs_disease': {'prevalence': 3.0, 'relative_risk': 100.0},
                'gaucher_disease': {'prevalence': 2.5, 'relative_risk': 50.0},
                'familial_dysautonomia': {'prevalence': 1.5, 'relative_risk': 80.0},
                'breast_cancer_brca': {'prevalence': 12.0, 'relative_risk': 5.0},
                'canavan_disease': {'prevalence': 2.0, 'relative_risk': 60.0}
            }
        }
        
        # General population baseline (per 100,000)
        self.baseline_prevalence = {
            'type_2_diabetes': 6.2,
            'coronary_artery_disease': 6.0,
            'thalassemia': 2.5,
            'sickle_cell_disease': 0.5,
            'cystic_fibrosis': 0.14,
            'hemochromatosis': 0.5,
            'hypertension': 8.5,
            'celiac_disease': 3.3,
            'multiple_sclerosis': 3.5,
            'g6pd_deficiency': 2.0,
            'familial_mediterranean_fever': 0.5,
            'tay_sachs_disease': 0.03,
            'gaucher_disease': 0.05,
            'breast_cancer_brca': 2.5,
            'melanoma': 3.5,
            'prostate_cancer': 6.0
        }
    
    def adjust_risk_by_ethnicity(self, base_risk_score, disorder, ethnicity, age=None, gender=None):
        """
        Adjust risk score based on ethnicity-specific prevalence
        
        Args:
            base_risk_score: Initial risk score (0-100)
            disorder: Genetic disorder name
            ethnicity: Patient ethnicity
            age: Patient age (optional)
            gender: Patient gender (optional)
        
        Returns:
            dict with adjusted risk and explanation
        """
        ethnicity_key = self._normalize_ethnicity(ethnicity)
        disorder_key = self._normalize_disorder(disorder)
        
        # Get ethnicity-specific data
        ethnicity_data = self.ethnicity_prevalence.get(ethnicity_key, {})
        disorder_data = ethnicity_data.get(disorder_key, None)
        
        if not disorder_data:
            # No specific data, return base risk
            return {
                'adjusted_risk_score': base_risk_score,
                'adjustment_factor': 1.0,
                'ethnicity': ethnicity,
                'population_prevalence': 'Unknown',
                'relative_risk': 1.0,
                'explanation': f'No ethnicity-specific data available for {disorder}',
                'confidence': 'Low'
            }
        
        # Calculate adjustment factor
        relative_risk = disorder_data['relative_risk']
        prevalence = disorder_data['prevalence']
        
        # Apply logarithmic adjustment to avoid extreme values
        import math
        adjustment_factor = 1.0 + (math.log10(relative_risk) * 0.3)
        
        # Age-based adjustment
        if age:
            age_factor = self._calculate_age_factor(disorder_key, age)
            adjustment_factor *= age_factor
        
        # Gender-based adjustment
        if gender:
            gender_factor = self._calculate_gender_factor(disorder_key, gender)
            adjustment_factor *= gender_factor
        
        # Calculate adjusted risk
        adjusted_risk = min(base_risk_score * adjustment_factor, 100.0)
        
        # Determine confidence level
        confidence = self._calculate_confidence(ethnicity_key, disorder_key, prevalence)
        
        # Generate explanation
        explanation = self._generate_explanation(
            ethnicity, disorder, relative_risk, prevalence, 
            adjustment_factor, base_risk_score, adjusted_risk
        )
        
        return {
            'adjusted_risk_score': round(adjusted_risk, 1),
            'adjustment_factor': round(adjustment_factor, 2),
            'ethnicity': ethnicity,
            'population_prevalence': f'{prevalence} per 100,000',
            'relative_risk': relative_risk,
            'explanation': explanation,
            'confidence': confidence,
            'baseline_prevalence': self.baseline_prevalence.get(disorder_key, 'Unknown')
        }
    
    def get_population_statistics(self, disorder, ethnicity):
        """Get detailed population statistics for a disorder and ethnicity"""
        ethnicity_key = self._normalize_ethnicity(ethnicity)
        disorder_key = self._normalize_disorder(disorder)
        
        ethnicity_data = self.ethnicity_prevalence.get(ethnicity_key, {})
        disorder_data = ethnicity_data.get(disorder_key, None)
        
        if not disorder_data:
            return None
        
        baseline = self.baseline_prevalence.get(disorder_key, 0)
        
        return {
            'disorder': disorder,
            'ethnicity': ethnicity,
            'prevalence_per_100k': disorder_data['prevalence'],
            'baseline_prevalence_per_100k': baseline,
            'relative_risk': disorder_data['relative_risk'],
            'fold_increase': round(disorder_data['prevalence'] / baseline, 1) if baseline > 0 else 'N/A',
            'carrier_frequency': self._estimate_carrier_frequency(disorder_key, disorder_data['prevalence'])
        }
    
    def compare_ethnicities(self, disorder):
        """Compare risk across different ethnicities for a disorder"""
        disorder_key = self._normalize_disorder(disorder)
        comparison = []
        
        for ethnicity, disorders in self.ethnicity_prevalence.items():
            if disorder_key in disorders:
                data = disorders[disorder_key]
                comparison.append({
                    'ethnicity': ethnicity.replace('_', ' ').title(),
                    'prevalence': data['prevalence'],
                    'relative_risk': data['relative_risk'],
                    'risk_category': self._categorize_risk(data['relative_risk'])
                })
        
        # Sort by prevalence
        comparison.sort(key=lambda x: x['prevalence'], reverse=True)
        
        return comparison
    
    def _normalize_ethnicity(self, ethnicity):
        """Normalize ethnicity string to match keys"""
        if not ethnicity:
            return 'caucasian'  # Default
        
        ethnicity_lower = ethnicity.lower().replace(' ', '_')
        
        # Map variations
        mapping = {
            'asian': 'east_asian',
            'indian': 'south_asian',
            'pakistani': 'south_asian',
            'bangladeshi': 'south_asian',
            'black': 'african',
            'african_american': 'african',
            'white': 'caucasian',
            'european': 'caucasian',
            'latino': 'hispanic',
            'latina': 'hispanic',
            'arab': 'middle_eastern',
            'persian': 'middle_eastern',
            'jewish': 'ashkenazi_jewish'
        }
        
        return mapping.get(ethnicity_lower, ethnicity_lower)
    
    def _normalize_disorder(self, disorder):
        """Normalize disorder name to match keys"""
        if not disorder:
            return ''
        
        disorder_lower = disorder.lower().replace(' ', '_').replace('-', '_')
        
        # Map variations
        mapping = {
            'diabetes': 'type_2_diabetes',
            'heart_disease': 'coronary_artery_disease',
            'sickle_cell': 'sickle_cell_disease',
            'cf': 'cystic_fibrosis',
            'ms': 'multiple_sclerosis',
            'fmf': 'familial_mediterranean_fever'
        }
        
        return mapping.get(disorder_lower, disorder_lower)
    
    def _calculate_age_factor(self, disorder, age):
        """Calculate age-based risk adjustment"""
        # Age-dependent disorders
        age_curves = {
            'type_2_diabetes': {'peak_age': 55, 'curve': 'increasing'},
            'coronary_artery_disease': {'peak_age': 60, 'curve': 'increasing'},
            'prostate_cancer': {'peak_age': 65, 'curve': 'increasing'},
            'breast_cancer_brca': {'peak_age': 50, 'curve': 'peak'},
            'huntingtons_disease': {'peak_age': 40, 'curve': 'peak'},
            'tay_sachs_disease': {'peak_age': 2, 'curve': 'early_onset'}
        }
        
        if disorder not in age_curves:
            return 1.0
        
        curve_data = age_curves[disorder]
        peak_age = curve_data['peak_age']
        curve_type = curve_data['curve']
        
        if curve_type == 'increasing':
            # Risk increases with age
            return 1.0 + (age / 100.0)
        elif curve_type == 'peak':
            # Risk peaks at certain age
            distance = abs(age - peak_age)
            return 1.0 + (0.5 * (1.0 - distance / 50.0))
        elif curve_type == 'early_onset':
            # Risk highest in early life
            return 2.0 if age < 10 else 1.0
        
        return 1.0
    
    def _calculate_gender_factor(self, disorder, gender):
        """Calculate gender-based risk adjustment"""
        gender_specific = {
            'prostate_cancer': {'male': 100.0, 'female': 0.0},
            'breast_cancer_brca': {'male': 0.1, 'female': 1.5},
            'hemophilia': {'male': 2.0, 'female': 0.1},
            'fragile_x': {'male': 1.5, 'female': 0.8}
        }
        
        if disorder not in gender_specific:
            return 1.0
        
        gender_key = gender.lower() if gender else 'male'
        return gender_specific[disorder].get(gender_key, 1.0)
    
    def _calculate_confidence(self, ethnicity, disorder, prevalence):
        """Calculate confidence level based on data quality"""
        # Higher prevalence = more data = higher confidence
        if prevalence > 10.0:
            return 'High'
        elif prevalence > 3.0:
            return 'Moderate'
        else:
            return 'Low'
    
    def _generate_explanation(self, ethnicity, disorder, relative_risk, 
                            prevalence, adjustment_factor, base_risk, adjusted_risk):
        """Generate human-readable explanation"""
        risk_change = adjusted_risk - base_risk
        direction = 'increased' if risk_change > 0 else 'decreased'
        
        explanation = f"Based on {ethnicity} population data, {disorder} has a prevalence of "
        explanation += f"{prevalence} per 100,000 individuals, which is {relative_risk}x higher "
        explanation += f"than the general population. Your risk has been {direction} by "
        explanation += f"{abs(risk_change):.1f} points (adjustment factor: {adjustment_factor:.2f}x) "
        explanation += f"to account for ethnicity-specific genetic predispositions."
        
        return explanation
    
    def _estimate_carrier_frequency(self, disorder, prevalence):
        """Estimate carrier frequency using Hardy-Weinberg equilibrium"""
        # For recessive disorders
        recessive_disorders = ['cystic_fibrosis', 'sickle_cell_disease', 'tay_sachs_disease']
        
        if any(d in disorder for d in recessive_disorders):
            # q^2 = prevalence/100000, carrier frequency = 2pq ≈ 2q
            import math
            q = math.sqrt(prevalence / 100000.0)
            carrier_freq = 2 * q * (1 - q)
            return f"~1 in {int(1/carrier_freq)}" if carrier_freq > 0 else "Unknown"
        
        return "N/A (not recessive)"
    
    def _categorize_risk(self, relative_risk):
        """Categorize relative risk level"""
        if relative_risk >= 10.0:
            return 'Very High'
        elif relative_risk >= 5.0:
            return 'High'
        elif relative_risk >= 2.0:
            return 'Moderate'
        else:
            return 'Low'
