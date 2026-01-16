"""
Clinical Test Recommendation Engine (AI Lab Order Assistant)
Recommends clinical tests, lab panels, and imaging based on genetic risk assessment
Enhances medical practicality and supports clinical decision-making
"""

from datetime import datetime

class ClinicalTestRecommender:
    """
    AI-powered clinical test recommendation engine
    Suggests appropriate diagnostic tests based on genetic risk profile
    """
    
    def __init__(self):
        # Comprehensive test database
        self.test_database = {
            # Genetic/Molecular Tests
            'genetic_sequencing': {
                'name': 'Whole Exome Sequencing (WES)',
                'category': 'genetic',
                'cost_range': '$1000-$5000',
                'turnaround_time': '4-6 weeks',
                'sample_type': 'Blood',
                'description': 'Comprehensive analysis of protein-coding genes'
            },
            'targeted_gene_panel': {
                'name': 'Targeted Gene Panel',
                'category': 'genetic',
                'cost_range': '$500-$2000',
                'turnaround_time': '2-4 weeks',
                'sample_type': 'Blood or Saliva',
                'description': 'Analysis of specific genes related to suspected condition'
            },
            'karyotype': {
                'name': 'Chromosomal Karyotype',
                'category': 'genetic',
                'cost_range': '$200-$500',
                'turnaround_time': '1-2 weeks',
                'sample_type': 'Blood',
                'description': 'Analysis of chromosome number and structure'
            },
            'fish_test': {
                'name': 'FISH (Fluorescence In Situ Hybridization)',
                'category': 'genetic',
                'cost_range': '$300-$800',
                'turnaround_time': '3-5 days',
                'sample_type': 'Blood or Tissue',
                'description': 'Detects specific chromosomal abnormalities'
            },
            
            # Blood Tests
            'cbc': {
                'name': 'Complete Blood Count (CBC)',
                'category': 'blood',
                'cost_range': '$10-$50',
                'turnaround_time': '1-2 days',
                'sample_type': 'Blood',
                'description': 'Measures blood cells, hemoglobin, and platelets'
            },
            'cmp': {
                'name': 'Comprehensive Metabolic Panel (CMP)',
                'category': 'blood',
                'cost_range': '$20-$80',
                'turnaround_time': '1-2 days',
                'sample_type': 'Blood',
                'description': 'Assesses kidney, liver function, electrolytes, glucose'
            },
            'lipid_panel': {
                'name': 'Lipid Panel',
                'category': 'blood',
                'cost_range': '$20-$60',
                'turnaround_time': '1-2 days',
                'sample_type': 'Blood (fasting)',
                'description': 'Measures cholesterol and triglycerides'
            },
            'hemoglobin_electrophoresis': {
                'name': 'Hemoglobin Electrophoresis',
                'category': 'blood',
                'cost_range': '$50-$150',
                'turnaround_time': '2-3 days',
                'sample_type': 'Blood',
                'description': 'Identifies abnormal hemoglobin variants'
            },
            'coagulation_panel': {
                'name': 'Coagulation Panel (PT/PTT/INR)',
                'category': 'blood',
                'cost_range': '$30-$100',
                'turnaround_time': '1 day',
                'sample_type': 'Blood',
                'description': 'Assesses blood clotting function'
            },
            'iron_studies': {
                'name': 'Iron Studies Panel',
                'category': 'blood',
                'cost_range': '$40-$120',
                'turnaround_time': '1-2 days',
                'sample_type': 'Blood',
                'description': 'Measures iron, ferritin, TIBC, transferrin saturation'
            },
            'creatine_kinase': {
                'name': 'Creatine Kinase (CK)',
                'category': 'blood',
                'cost_range': '$20-$60',
                'turnaround_time': '1 day',
                'sample_type': 'Blood',
                'description': 'Measures muscle enzyme levels'
            },
            
            # Imaging Tests
            'mri_brain': {
                'name': 'Brain MRI',
                'category': 'imaging',
                'cost_range': '$500-$3000',
                'turnaround_time': '1-3 days',
                'sample_type': 'N/A',
                'description': 'Detailed brain imaging for structural abnormalities'
            },
            'ct_scan': {
                'name': 'CT Scan',
                'category': 'imaging',
                'cost_range': '$300-$2000',
                'turnaround_time': '1-2 days',
                'sample_type': 'N/A',
                'description': 'Cross-sectional imaging of body structures'
            },
            'echocardiogram': {
                'name': 'Echocardiogram',
                'category': 'imaging',
                'cost_range': '$200-$1000',
                'turnaround_time': '1-2 days',
                'sample_type': 'N/A',
                'description': 'Ultrasound of heart structure and function'
            },
            'bone_density': {
                'name': 'DEXA Bone Density Scan',
                'category': 'imaging',
                'cost_range': '$100-$300',
                'turnaround_time': '1 day',
                'sample_type': 'N/A',
                'description': 'Measures bone mineral density'
            },
            
            # Specialized Tests
            'emg': {
                'name': 'Electromyography (EMG)',
                'category': 'specialized',
                'cost_range': '$200-$800',
                'turnaround_time': '1-2 days',
                'sample_type': 'N/A',
                'description': 'Tests muscle and nerve function'
            },
            'eeg': {
                'name': 'Electroencephalogram (EEG)',
                'category': 'specialized',
                'cost_range': '$200-$700',
                'turnaround_time': '1-2 days',
                'sample_type': 'N/A',
                'description': 'Records brain electrical activity'
            },
            'pulmonary_function': {
                'name': 'Pulmonary Function Tests (PFT)',
                'category': 'specialized',
                'cost_range': '$100-$400',
                'turnaround_time': '1 day',
                'sample_type': 'N/A',
                'description': 'Measures lung capacity and function'
            },
            'sweat_chloride': {
                'name': 'Sweat Chloride Test',
                'category': 'specialized',
                'cost_range': '$50-$200',
                'turnaround_time': '1-2 days',
                'sample_type': 'Sweat',
                'description': 'Diagnostic test for cystic fibrosis'
            },
            'muscle_biopsy': {
                'name': 'Muscle Biopsy',
                'category': 'specialized',
                'cost_range': '$500-$2000',
                'turnaround_time': '1-2 weeks',
                'sample_type': 'Muscle tissue',
                'description': 'Microscopic examination of muscle tissue'
            },
            
            # Tumor Markers
            'ca125': {
                'name': 'CA-125 (Ovarian Cancer Marker)',
                'category': 'tumor_marker',
                'cost_range': '$30-$100',
                'turnaround_time': '1-2 days',
                'sample_type': 'Blood',
                'description': 'Tumor marker for ovarian cancer'
            },
            'psa': {
                'name': 'PSA (Prostate-Specific Antigen)',
                'category': 'tumor_marker',
                'cost_range': '$30-$100',
                'turnaround_time': '1-2 days',
                'sample_type': 'Blood',
                'description': 'Screening for prostate cancer'
            },
            'cea': {
                'name': 'CEA (Carcinoembryonic Antigen)',
                'category': 'tumor_marker',
                'cost_range': '$30-$100',
                'turnaround_time': '1-2 days',
                'sample_type': 'Blood',
                'description': 'Tumor marker for various cancers'
            }
        }
        
        # Disorder-specific test recommendations
        self.disorder_test_map = {
            'huntington_disease': {
                'genetic': ['targeted_gene_panel'],
                'blood': ['cbc', 'cmp'],
                'imaging': ['mri_brain'],
                'specialized': ['eeg']
            },
            'cystic_fibrosis': {
                'genetic': ['targeted_gene_panel'],
                'blood': ['cbc', 'cmp'],
                'imaging': ['ct_scan'],
                'specialized': ['sweat_chloride', 'pulmonary_function']
            },
            'sickle_cell_disease': {
                'genetic': ['targeted_gene_panel'],
                'blood': ['cbc', 'hemoglobin_electrophoresis'],
                'imaging': [],
                'specialized': []
            },
            'thalassemia': {
                'genetic': ['targeted_gene_panel'],
                'blood': ['cbc', 'hemoglobin_electrophoresis', 'iron_studies'],
                'imaging': [],
                'specialized': []
            },
            'muscular_dystrophy': {
                'genetic': ['targeted_gene_panel', 'genetic_sequencing'],
                'blood': ['creatine_kinase', 'cbc'],
                'imaging': ['mri_brain'],
                'specialized': ['emg', 'muscle_biopsy']
            },
            'hemophilia': {
                'genetic': ['targeted_gene_panel'],
                'blood': ['coagulation_panel', 'cbc'],
                'imaging': [],
                'specialized': []
            },
            'breast_cancer': {
                'genetic': ['targeted_gene_panel'],
                'blood': ['cbc', 'ca125'],
                'imaging': ['mri_brain'],
                'specialized': []
            },
            'hemochromatosis': {
                'genetic': ['targeted_gene_panel'],
                'blood': ['iron_studies', 'cmp'],
                'imaging': ['mri_brain'],
                'specialized': []
            },
            'tay_sachs_disease': {
                'genetic': ['targeted_gene_panel', 'genetic_sequencing'],
                'blood': ['cbc', 'cmp'],
                'imaging': ['mri_brain'],
                'specialized': ['eeg']
            }
        }
    
    def recommend_tests(self, disorder, risk_score, symptoms=None, age=None, gender=None):
        """
        Generate comprehensive test recommendations
        
        Args:
            disorder: Predicted genetic disorder
            risk_score: Risk score (0-100)
            symptoms: List of symptoms
            age: Patient age
            gender: Patient gender
        
        Returns:
            dict with test recommendations and priorities
        """
        recommendations = {
            'disorder': disorder,
            'risk_score': risk_score,
            'priority_level': self._determine_priority(risk_score),
            'recommended_tests': [],
            'optional_tests': [],
            'follow_up_tests': [],
            'estimated_total_cost': {'min': 0, 'max': 0},
            'estimated_timeline': '',
            'insurance_coverage': {},
            'clinical_notes': []
        }
        
        # Get disorder-specific tests
        disorder_key = self._normalize_disorder(disorder)
        test_categories = self.disorder_test_map.get(disorder_key, {})
        
        # Categorize tests by priority
        if risk_score >= 60:
            # High risk - all tests recommended
            for category, tests in test_categories.items():
                for test_key in tests:
                    test_info = self.test_database.get(test_key)
                    if test_info:
                        recommendations['recommended_tests'].append({
                            'test_key': test_key,
                            'test_name': test_info['name'],
                            'category': test_info['category'],
                            'priority': 'Urgent' if category == 'genetic' else 'High',
                            'cost_range': test_info['cost_range'],
                            'turnaround_time': test_info['turnaround_time'],
                            'sample_type': test_info['sample_type'],
                            'description': test_info['description'],
                            'reason': self._get_test_reason(test_key, disorder, risk_score)
                        })
        
        elif risk_score >= 30:
            # Moderate risk - essential tests + some optional
            essential_categories = ['genetic', 'blood']
            for category in essential_categories:
                tests = test_categories.get(category, [])
                for test_key in tests:
                    test_info = self.test_database.get(test_key)
                    if test_info:
                        recommendations['recommended_tests'].append({
                            'test_key': test_key,
                            'test_name': test_info['name'],
                            'category': test_info['category'],
                            'priority': 'High' if category == 'genetic' else 'Moderate',
                            'cost_range': test_info['cost_range'],
                            'turnaround_time': test_info['turnaround_time'],
                            'sample_type': test_info['sample_type'],
                            'description': test_info['description'],
                            'reason': self._get_test_reason(test_key, disorder, risk_score)
                        })
            
            # Optional tests
            optional_categories = ['imaging', 'specialized']
            for category in optional_categories:
                tests = test_categories.get(category, [])
                for test_key in tests:
                    test_info = self.test_database.get(test_key)
                    if test_info:
                        recommendations['optional_tests'].append({
                            'test_key': test_key,
                            'test_name': test_info['name'],
                            'category': test_info['category'],
                            'priority': 'Optional',
                            'cost_range': test_info['cost_range'],
                            'turnaround_time': test_info['turnaround_time'],
                            'sample_type': test_info['sample_type'],
                            'description': test_info['description'],
                            'reason': self._get_test_reason(test_key, disorder, risk_score)
                        })
        
        else:
            # Low risk - basic screening only
            basic_tests = ['cbc', 'cmp']
            for test_key in basic_tests:
                test_info = self.test_database.get(test_key)
                if test_info:
                    recommendations['optional_tests'].append({
                        'test_key': test_key,
                        'test_name': test_info['name'],
                        'category': test_info['category'],
                        'priority': 'Optional',
                        'cost_range': test_info['cost_range'],
                        'turnaround_time': test_info['turnaround_time'],
                        'sample_type': test_info['sample_type'],
                        'description': test_info['description'],
                        'reason': 'Baseline health screening'
                    })
        
        # Add symptom-specific tests
        if symptoms:
            symptom_tests = self._get_symptom_specific_tests(symptoms)
            for test in symptom_tests:
                if test not in [t['test_key'] for t in recommendations['recommended_tests']]:
                    test_info = self.test_database.get(test)
                    if test_info:
                        recommendations['recommended_tests'].append({
                            'test_key': test,
                            'test_name': test_info['name'],
                            'category': test_info['category'],
                            'priority': 'High',
                            'cost_range': test_info['cost_range'],
                            'turnaround_time': test_info['turnaround_time'],
                            'sample_type': test_info['sample_type'],
                            'description': test_info['description'],
                            'reason': 'Symptom-specific evaluation'
                        })
        
        # Add age/gender-specific tests
        if age and gender:
            demographic_tests = self._get_demographic_tests(age, gender, disorder)
            for test in demographic_tests:
                if test not in [t['test_key'] for t in recommendations['recommended_tests'] + recommendations['optional_tests']]:
                    test_info = self.test_database.get(test)
                    if test_info:
                        recommendations['optional_tests'].append({
                            'test_key': test,
                            'test_name': test_info['name'],
                            'category': test_info['category'],
                            'priority': 'Recommended',
                            'cost_range': test_info['cost_range'],
                            'turnaround_time': test_info['turnaround_time'],
                            'sample_type': test_info['sample_type'],
                            'description': test_info['description'],
                            'reason': 'Age/gender-appropriate screening'
                        })
        
        # Calculate costs
        recommendations['estimated_total_cost'] = self._calculate_total_cost(
            recommendations['recommended_tests']
        )
        
        # Estimate timeline
        recommendations['estimated_timeline'] = self._estimate_timeline(
            recommendations['recommended_tests']
        )
        
        # Insurance coverage info
        recommendations['insurance_coverage'] = self._get_insurance_info(
            recommendations['recommended_tests'], risk_score
        )
        
        # Clinical notes
        recommendations['clinical_notes'] = self._generate_clinical_notes(
            disorder, risk_score, recommendations
        )
        
        return recommendations
    
    def _determine_priority(self, risk_score):
        """Determine overall priority level"""
        if risk_score >= 70:
            return 'URGENT - Immediate evaluation required'
        elif risk_score >= 50:
            return 'HIGH - Schedule within 1-2 weeks'
        elif risk_score >= 30:
            return 'MODERATE - Schedule within 1 month'
        else:
            return 'LOW - Routine screening'
    
    def _normalize_disorder(self, disorder):
        """Normalize disorder name"""
        if not disorder:
            return ''
        
        disorder_lower = disorder.lower().replace(' ', '_').replace('-', '_')
        
        mapping = {
            'huntingtons': 'huntington_disease',
            'cf': 'cystic_fibrosis',
            'sickle_cell': 'sickle_cell_disease',
            'md': 'muscular_dystrophy',
            'duchenne': 'muscular_dystrophy'
        }
        
        return mapping.get(disorder_lower, disorder_lower)
    
    def _get_test_reason(self, test_key, disorder, risk_score):
        """Generate reason for test recommendation"""
        reasons = {
            'genetic_sequencing': f'Comprehensive genetic analysis for {disorder}',
            'targeted_gene_panel': f'Confirm genetic diagnosis of {disorder}',
            'karyotype': 'Assess chromosomal abnormalities',
            'cbc': 'Evaluate blood cell counts and anemia',
            'hemoglobin_electrophoresis': 'Identify hemoglobin variants',
            'coagulation_panel': 'Assess blood clotting function',
            'creatine_kinase': 'Evaluate muscle damage',
            'mri_brain': 'Assess brain structure and abnormalities',
            'emg': 'Evaluate muscle and nerve function',
            'sweat_chloride': 'Diagnostic test for cystic fibrosis'
        }
        
        return reasons.get(test_key, f'Recommended for {disorder} evaluation')
    
    def _get_symptom_specific_tests(self, symptoms):
        """Get tests based on symptoms"""
        symptom_test_map = {
            'muscle_weakness': ['creatine_kinase', 'emg'],
            'breathing_difficulties': ['pulmonary_function', 'ct_scan'],
            'unusual_bleeding': ['coagulation_panel', 'cbc'],
            'seizures': ['eeg', 'mri_brain'],
            'fatigue': ['cbc', 'iron_studies', 'cmp'],
            'joint_pain': ['cbc', 'cmp'],
            'vision_problems': ['mri_brain'],
            'hearing_loss': ['mri_brain']
        }
        
        tests = []
        for symptom in symptoms:
            if symptom in symptom_test_map:
                tests.extend(symptom_test_map[symptom])
        
        return list(set(tests))
    
    def _get_demographic_tests(self, age, gender, disorder):
        """Get age/gender-specific tests"""
        tests = []
        
        # Age-based
        if age > 50:
            tests.extend(['lipid_panel', 'bone_density'])
        
        # Gender-based
        if gender and gender.lower() == 'female':
            if 'breast' in disorder.lower() or 'ovarian' in disorder.lower():
                tests.append('ca125')
        elif gender and gender.lower() == 'male':
            if age > 50:
                tests.append('psa')
        
        return tests
    
    def _calculate_total_cost(self, tests):
        """Calculate estimated total cost"""
        min_cost = 0
        max_cost = 0
        
        for test in tests:
            cost_range = test['cost_range']
            # Parse cost range like "$100-$500"
            costs = cost_range.replace('$', '').replace(',', '').split('-')
            if len(costs) == 2:
                min_cost += int(costs[0])
                max_cost += int(costs[1])
        
        return {
            'min': f'${min_cost:,}',
            'max': f'${max_cost:,}',
            'average': f'${(min_cost + max_cost) // 2:,}'
        }
    
    def _estimate_timeline(self, tests):
        """Estimate total timeline"""
        if not tests:
            return 'N/A'
        
        # Find longest turnaround time
        max_weeks = 0
        for test in tests:
            turnaround = test['turnaround_time']
            if 'week' in turnaround:
                weeks = int(turnaround.split('-')[-1].split()[0])
                max_weeks = max(max_weeks, weeks)
        
        if max_weeks > 0:
            return f'{max_weeks} weeks for complete results'
        else:
            return '1-2 weeks for complete results'
    
    def _get_insurance_info(self, tests, risk_score):
        """Get insurance coverage information"""
        coverage = {
            'likely_covered': [],
            'may_require_preauth': [],
            'likely_not_covered': []
        }
        
        for test in tests:
            category = test['category']
            if risk_score >= 60:
                # High risk - most tests covered
                if category in ['genetic', 'blood']:
                    coverage['likely_covered'].append(test['test_name'])
                else:
                    coverage['may_require_preauth'].append(test['test_name'])
            elif risk_score >= 30:
                # Moderate risk
                if category == 'blood':
                    coverage['likely_covered'].append(test['test_name'])
                else:
                    coverage['may_require_preauth'].append(test['test_name'])
            else:
                # Low risk
                coverage['likely_not_covered'].append(test['test_name'])
        
        return coverage
    
    def _generate_clinical_notes(self, disorder, risk_score, recommendations):
        """Generate clinical notes for healthcare provider"""
        notes = []
        
        notes.append(f"Patient presents with {risk_score}% risk for {disorder}")
        
        if risk_score >= 60:
            notes.append("High-risk patient requiring urgent genetic evaluation")
            notes.append("Consider referral to genetic specialist")
        elif risk_score >= 30:
            notes.append("Moderate-risk patient requiring genetic counseling")
        
        test_count = len(recommendations['recommended_tests'])
        notes.append(f"Recommended {test_count} diagnostic tests")
        
        if recommendations['estimated_total_cost']['max']:
            notes.append(f"Estimated cost: {recommendations['estimated_total_cost']['min']} - {recommendations['estimated_total_cost']['max']}")
        
        return notes
