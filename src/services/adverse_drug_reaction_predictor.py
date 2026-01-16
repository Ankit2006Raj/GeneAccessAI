"""
Adverse Drug Reaction Predictor - Pharmacogenetic Estimator
Predicts potential drug reactions based on genetic patterns
"""
from typing import Dict, List, Any, Optional
from datetime import datetime


class AdverseDrugReactionPredictor:
    """
    Predicts patient's potential adverse reactions to common drugs
    based on hereditary patterns and pharmacogenetic markers.
    """
    
    def __init__(self):
        # CYP450 enzyme variants and drug metabolism
        self.cyp450_variants = {
            'CYP2D6': {
                'poor_metabolizer': {
                    'frequency': '5-10% Caucasian, 1-2% Asian',
                    'affected_drugs': [
                        'Codeine', 'Tramadol', 'Metoprolol', 'Fluoxetine', 'Paroxetine'
                    ],
                    'risk': 'High - Increased drug levels, toxicity risk'
                },
                'intermediate_metabolizer': {
                    'frequency': '10-15% population',
                    'affected_drugs': ['Same as poor metabolizer'],
                    'risk': 'Moderate - May need dose adjustment'
                },
                'extensive_metabolizer': {
                    'frequency': '70-80% population',
                    'affected_drugs': [],
                    'risk': 'Low - Normal metabolism'
                },
                'ultra_rapid_metabolizer': {
                    'frequency': '5-10% population',
                    'affected_drugs': ['Codeine', 'Tramadol'],
                    'risk': 'High - Rapid conversion to active metabolites'
                }
            },
            'CYP2C9': {
                'poor_metabolizer': {
                    'frequency': '1-3% Caucasian',
                    'affected_drugs': ['Warfarin', 'Phenytoin', 'NSAIDs'],
                    'risk': 'High - Bleeding risk with warfarin'
                }
            },
            'CYP2C19': {
                'poor_metabolizer': {
                    'frequency': '2-5% Caucasian, 15-20% Asian',
                    'affected_drugs': ['Clopidogrel', 'Omeprazole', 'Diazepam'],
                    'risk': 'High - Reduced drug efficacy'
                }
            },
            'CYP3A4': {
                'poor_metabolizer': {
                    'frequency': 'Rare',
                    'affected_drugs': ['Statins', 'Immunosuppressants', 'Many others'],
                    'risk': 'High - Metabolizes 50% of drugs'
                }
            }
        }
        
        # Genetic disorder-specific drug risks
        self.disorder_drug_risks = {
            'Hemophilia': {
                'high_risk_drugs': [
                    {
                        'drug': 'Aspirin',
                        'risk_level': 'Contraindicated',
                        'reason': 'Antiplatelet effect increases bleeding risk',
                        'alternatives': ['Acetaminophen for pain']
                    },
                    {
                        'drug': 'NSAIDs (Ibuprofen, Naproxen)',
                        'risk_level': 'Contraindicated',
                        'reason': 'Inhibits platelet function',
                        'alternatives': ['Acetaminophen', 'COX-2 inhibitors with caution']
                    },
                    {
                        'drug': 'Warfarin',
                        'risk_level': 'High Risk',
                        'reason': 'Anticoagulant effect compounds bleeding disorder',
                        'alternatives': ['Avoid unless absolutely necessary']
                    }
                ],
                'anesthesia_concerns': [
                    'Regional anesthesia requires factor replacement',
                    'Avoid intramuscular injections',
                    'Careful monitoring during surgery'
                ]
            },
            'Sickle Cell Disease': {
                'high_risk_drugs': [
                    {
                        'drug': 'Decongestants (Pseudoephedrine)',
                        'risk_level': 'Moderate Risk',
                        'reason': 'May trigger vaso-occlusive crisis',
                        'alternatives': ['Saline nasal spray']
                    },
                    {
                        'drug': 'High-altitude medications',
                        'risk_level': 'High Risk',
                        'reason': 'Hypoxia risk',
                        'alternatives': ['Oxygen supplementation']
                    }
                ],
                'anesthesia_concerns': [
                    'Maintain oxygenation >95%',
                    'Avoid hypothermia',
                    'Adequate hydration critical'
                ]
            },
            'G6PD Deficiency': {
                'high_risk_drugs': [
                    {
                        'drug': 'Sulfonamides',
                        'risk_level': 'Contraindicated',
                        'reason': 'Triggers hemolytic anemia',
                        'alternatives': ['Alternative antibiotics']
                    },
                    {
                        'drug': 'Antimalarials (Primaquine)',
                        'risk_level': 'Contraindicated',
                        'reason': 'Severe hemolysis',
                        'alternatives': ['Alternative antimalarials']
                    },
                    {
                        'drug': 'Aspirin (high dose)',
                        'risk_level': 'High Risk',
                        'reason': 'May trigger hemolysis',
                        'alternatives': ['Low-dose may be tolerated']
                    }
                ],
                'anesthesia_concerns': [
                    'Avoid oxidative stress',
                    'Monitor for hemolysis post-op'
                ]
            },
            'Thalassemia': {
                'high_risk_drugs': [
                    {
                        'drug': 'Iron supplements (if not deficient)',
                        'risk_level': 'Contraindicated',
                        'reason': 'Iron overload risk',
                        'alternatives': ['Iron chelation therapy if overloaded']
                    }
                ],
                'anesthesia_concerns': [
                    'Cardiac assessment pre-op',
                    'Monitor for arrhythmias'
                ]
            },
            'Cystic Fibrosis': {
                'high_risk_drugs': [
                    {
                        'drug': 'Aminoglycosides',
                        'risk_level': 'Moderate Risk',
                        'reason': 'Ototoxicity and nephrotoxicity',
                        'alternatives': ['Monitor levels closely']
                    }
                ],
                'anesthesia_concerns': [
                    'Pulmonary function assessment',
                    'Aggressive chest physiotherapy post-op'
                ]
            }
        }
        
        # Common drug interactions
        self.drug_interactions = {
            'Warfarin': [
                'Antibiotics', 'NSAIDs', 'Aspirin', 'Vitamin K', 'Alcohol'
            ],
            'Statins': [
                'Grapefruit juice', 'Fibrates', 'Macrolide antibiotics'
            ],
            'SSRIs': [
                'MAO inhibitors', 'NSAIDs', 'Anticoagulants'
            ]
        }
    
    def predict_drug_reactions(
        self,
        patient_data: Dict[str, Any],
        medications: List[str],
        genetic_disorders: List[str]
    ) -> Dict[str, Any]:
        """
        Predict adverse drug reactions based on patient profile.
        
        Args:
            patient_data: Patient demographics and history
            medications: List of current/proposed medications
            genetic_disorders: List of diagnosed genetic disorders
        
        Returns:
            Comprehensive drug reaction risk assessment
        """
        
        predictions = []
        high_risk_count = 0
        moderate_risk_count = 0
        
        # Check each medication
        for medication in medications:
            risk_assessment = self._assess_medication_risk(
                medication, patient_data, genetic_disorders
            )
            predictions.append(risk_assessment)
            
            if risk_assessment['risk_level'] == 'High' or \
               risk_assessment['risk_level'] == 'Contraindicated':
                high_risk_count += 1
            elif risk_assessment['risk_level'] == 'Moderate':
                moderate_risk_count += 1
        
        # Generate overall assessment
        overall_risk = self._calculate_overall_risk(high_risk_count, moderate_risk_count)
        
        # Generate recommendations
        recommendations = self._generate_drug_recommendations(
            predictions, genetic_disorders
        )
        
        return {
            'success': True,
            'patient_id': patient_data.get('id', 'Unknown'),
            'assessment_date': datetime.now().isoformat(),
            'medications_assessed': len(medications),
            'overall_risk': overall_risk,
            'risk_summary': {
                'high_risk': high_risk_count,
                'moderate_risk': moderate_risk_count,
                'low_risk': len(medications) - high_risk_count - moderate_risk_count
            },
            'predictions': predictions,
            'recommendations': recommendations,
            'requires_pharmacist_review': high_risk_count > 0,
            'requires_genetic_testing': self._needs_genetic_testing(patient_data)
        }
    
    def _assess_medication_risk(
        self,
        medication: str,
        patient_data: Dict[str, Any],
        genetic_disorders: List[str]
    ) -> Dict[str, Any]:
        """Assess risk for a specific medication."""
        
        risk_factors = []
        risk_level = 'Low'
        warnings = []
        alternatives = []
        
        # Check disorder-specific risks
        for disorder in genetic_disorders:
            if disorder in self.disorder_drug_risks:
                disorder_risks = self.disorder_drug_risks[disorder]['high_risk_drugs']
                
                for drug_risk in disorder_risks:
                    if medication.lower() in drug_risk['drug'].lower() or \
                       drug_risk['drug'].lower() in medication.lower():
                        risk_level = drug_risk['risk_level']
                        risk_factors.append({
                            'factor': f'{disorder} interaction',
                            'description': drug_risk['reason']
                        })
                        warnings.append(drug_risk['reason'])
                        alternatives.extend(drug_risk['alternatives'])
        
        # Check CYP450 metabolism (simulated based on ethnicity)
        cyp_risk = self._assess_cyp450_risk(medication, patient_data.get('ethnicity'))
        if cyp_risk:
            risk_factors.append(cyp_risk)
            if cyp_risk['severity'] in ['High', 'Contraindicated']:
                risk_level = 'High'
        
        # Check age-related risks
        age = patient_data.get('age', 0)
        if age < 18 or age > 65:
            age_risk = self._assess_age_risk(medication, age)
            if age_risk:
                risk_factors.append(age_risk)
        
        return {
            'medication': medication,
            'risk_level': risk_level,
            'risk_factors': risk_factors,
            'warnings': warnings,
            'alternatives': list(set(alternatives)),
            'monitoring_required': risk_level in ['Moderate', 'High'],
            'genetic_testing_recommended': cyp_risk is not None
        }
    
    def _assess_cyp450_risk(
        self,
        medication: str,
        ethnicity: Optional[str]
    ) -> Optional[Dict[str, Any]]:
        """Assess CYP450-related metabolism risk."""
        
        # Simplified CYP450 assessment
        high_risk_meds = {
            'Warfarin': 'CYP2C9',
            'Clopidogrel': 'CYP2C19',
            'Codeine': 'CYP2D6',
            'Tramadol': 'CYP2D6',
            'Omeprazole': 'CYP2C19'
        }
        
        for drug, enzyme in high_risk_meds.items():
            if drug.lower() in medication.lower():
                return {
                    'factor': f'{enzyme} metabolism',
                    'description': f'{medication} is metabolized by {enzyme}. Genetic variants may affect drug levels.',
                    'severity': 'Moderate',
                    'recommendation': f'Consider {enzyme} genetic testing'
                }
        
        return None
    
    def _assess_age_risk(self, medication: str, age: int) -> Optional[Dict[str, Any]]:
        """Assess age-related medication risks."""
        
        if age < 18:
            pediatric_caution = ['Aspirin', 'Tetracycline', 'Fluoroquinolones']
            for drug in pediatric_caution:
                if drug.lower() in medication.lower():
                    return {
                        'factor': 'Pediatric use',
                        'description': f'{medication} requires caution in children',
                        'severity': 'Moderate'
                    }
        
        if age > 65:
            geriatric_caution = ['Benzodiazepines', 'Anticholinergics', 'NSAIDs']
            for drug in geriatric_caution:
                if drug.lower() in medication.lower():
                    return {
                        'factor': 'Geriatric use',
                        'description': f'{medication} requires dose adjustment in elderly',
                        'severity': 'Moderate'
                    }
        
        return None
    
    def _calculate_overall_risk(self, high_risk: int, moderate_risk: int) -> str:
        """Calculate overall medication risk level."""
        
        if high_risk > 0:
            return 'High - Immediate review required'
        elif moderate_risk > 2:
            return 'Moderate-High - Careful monitoring needed'
        elif moderate_risk > 0:
            return 'Moderate - Standard monitoring'
        else:
            return 'Low - Routine care'
    
    def _generate_drug_recommendations(
        self,
        predictions: List[Dict],
        genetic_disorders: List[str]
    ) -> List[Dict[str, Any]]:
        """Generate medication recommendations."""
        
        recommendations = []
        
        # High-risk medications
        high_risk_meds = [p for p in predictions if p['risk_level'] in ['High', 'Contraindicated']]
        if high_risk_meds:
            recommendations.append({
                'priority': 'Urgent',
                'category': 'Medication Review',
                'recommendation': 'Immediate consultation with pharmacist or physician required',
                'details': f'{len(high_risk_meds)} high-risk medication(s) identified',
                'medications': [m['medication'] for m in high_risk_meds]
            })
        
        # Genetic testing
        needs_testing = [p for p in predictions if p.get('genetic_testing_recommended')]
        if needs_testing:
            recommendations.append({
                'priority': 'High',
                'category': 'Genetic Testing',
                'recommendation': 'Pharmacogenetic testing recommended',
                'details': 'CYP450 genotyping can optimize medication selection',
                'tests': ['CYP2D6', 'CYP2C9', 'CYP2C19']
            })
        
        # Monitoring
        needs_monitoring = [p for p in predictions if p.get('monitoring_required')]
        if needs_monitoring:
            recommendations.append({
                'priority': 'Moderate',
                'category': 'Monitoring',
                'recommendation': 'Enhanced medication monitoring required',
                'details': 'Regular lab work and symptom tracking',
                'frequency': 'Monthly initially, then quarterly'
            })
        
        # Disorder-specific
        for disorder in genetic_disorders:
            if disorder in self.disorder_drug_risks:
                anesthesia = self.disorder_drug_risks[disorder].get('anesthesia_concerns', [])
                if anesthesia:
                    recommendations.append({
                        'priority': 'Important',
                        'category': 'Anesthesia Precautions',
                        'recommendation': f'Special considerations for {disorder}',
                        'details': anesthesia
                    })
        
        return recommendations
    
    def _needs_genetic_testing(self, patient_data: Dict) -> bool:
        """Determine if genetic testing is recommended."""
        
        # Recommend testing if:
        # - Family history of adverse drug reactions
        # - Ethnicity with known CYP450 variants
        # - Previous unexplained drug reactions
        
        family_history = patient_data.get('family_drug_reactions', False)
        ethnicity = patient_data.get('ethnicity', '')
        previous_reactions = patient_data.get('previous_adverse_reactions', False)
        
        return family_history or previous_reactions or ethnicity in ['Asian', 'African']
    
    def get_anesthesia_risk_profile(
        self,
        genetic_disorders: List[str],
        surgery_type: str
    ) -> Dict[str, Any]:
        """Generate anesthesia risk profile for surgery."""
        
        risks = []
        precautions = []
        
        for disorder in genetic_disorders:
            if disorder in self.disorder_drug_risks:
                concerns = self.disorder_drug_risks[disorder].get('anesthesia_concerns', [])
                for concern in concerns:
                    precautions.append({
                        'disorder': disorder,
                        'precaution': concern
                    })
                
                # Add specific risks
                if disorder == 'Hemophilia':
                    risks.append({
                        'risk': 'Bleeding complications',
                        'severity': 'High',
                        'mitigation': 'Factor replacement before and after surgery'
                    })
                elif disorder == 'Sickle Cell Disease':
                    risks.append({
                        'risk': 'Vaso-occlusive crisis',
                        'severity': 'High',
                        'mitigation': 'Maintain oxygenation, hydration, normothermia'
                    })
        
        return {
            'success': True,
            'surgery_type': surgery_type,
            'overall_risk': 'High' if len(risks) > 0 else 'Moderate',
            'specific_risks': risks,
            'precautions': precautions,
            'recommendations': [
                'Pre-operative hematology consultation',
                'Anesthesiologist briefing on genetic conditions',
                'Post-operative monitoring protocol',
                'Emergency response plan'
            ]
        }
    
    def check_drug_interactions(
        self,
        medications: List[str]
    ) -> Dict[str, Any]:
        """Check for drug-drug interactions."""
        
        interactions = []
        
        for i, med1 in enumerate(medications):
            for med2 in medications[i+1:]:
                interaction = self._check_interaction(med1, med2)
                if interaction:
                    interactions.append(interaction)
        
        return {
            'success': True,
            'medications_checked': len(medications),
            'interactions_found': len(interactions),
            'interactions': interactions,
            'severity': 'High' if any(i['severity'] == 'Major' for i in interactions) else 'Moderate'
        }
    
    def _check_interaction(self, med1: str, med2: str) -> Optional[Dict[str, Any]]:
        """Check interaction between two medications."""
        
        # Simplified interaction checking
        known_interactions = {
            ('Warfarin', 'Aspirin'): {
                'severity': 'Major',
                'description': 'Increased bleeding risk',
                'recommendation': 'Avoid combination or monitor INR closely'
            },
            ('Warfarin', 'NSAIDs'): {
                'severity': 'Major',
                'description': 'Increased bleeding risk',
                'recommendation': 'Use alternative pain reliever'
            }
        }
        
        # Check both directions
        for (drug1, drug2), interaction in known_interactions.items():
            if (drug1.lower() in med1.lower() and drug2.lower() in med2.lower()) or \
               (drug1.lower() in med2.lower() and drug2.lower() in med1.lower()):
                return {
                    'medication_1': med1,
                    'medication_2': med2,
                    'severity': interaction['severity'],
                    'description': interaction['description'],
                    'recommendation': interaction['recommendation']
                }
        
        return None
