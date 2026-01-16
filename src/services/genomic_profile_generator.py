"""
Synthetic Genomic Profile Generator (AI-Powered Pseudo-Genetics)
Generates probabilistic genetic trait maps without actual DNA testing
Bridges "no DNA testing" with "genetic-like insights"
"""

import random
import json
from datetime import datetime

class GenomicProfileGenerator:
    """
    Generates synthetic genomic profiles based on phenotypic data,
    family history, and population genetics
    """
    
    def __init__(self):
        # Gene-disease associations (simplified)
        self.gene_associations = {
            'BRCA1': {
                'disorders': ['Breast Cancer', 'Ovarian Cancer'],
                'inheritance': 'autosomal_dominant',
                'penetrance': 0.70,
                'chromosome': '17q21'
            },
            'BRCA2': {
                'disorders': ['Breast Cancer', 'Ovarian Cancer', 'Prostate Cancer'],
                'inheritance': 'autosomal_dominant',
                'penetrance': 0.65,
                'chromosome': '13q13'
            },
            'CFTR': {
                'disorders': ['Cystic Fibrosis'],
                'inheritance': 'autosomal_recessive',
                'penetrance': 1.0,
                'chromosome': '7q31'
            },
            'HTT': {
                'disorders': ['Huntington Disease'],
                'inheritance': 'autosomal_dominant',
                'penetrance': 1.0,
                'chromosome': '4p16'
            },
            'HBB': {
                'disorders': ['Sickle Cell Disease', 'Thalassemia'],
                'inheritance': 'autosomal_recessive',
                'penetrance': 1.0,
                'chromosome': '11p15'
            },
            'DMD': {
                'disorders': ['Duchenne Muscular Dystrophy'],
                'inheritance': 'x_linked_recessive',
                'penetrance': 1.0,
                'chromosome': 'Xp21'
            },
            'F8': {
                'disorders': ['Hemophilia A'],
                'inheritance': 'x_linked_recessive',
                'penetrance': 1.0,
                'chromosome': 'Xq28'
            },
            'F9': {
                'disorders': ['Hemophilia B'],
                'inheritance': 'x_linked_recessive',
                'penetrance': 0.95,
                'chromosome': 'Xq27'
            },
            'HEXA': {
                'disorders': ['Tay-Sachs Disease'],
                'inheritance': 'autosomal_recessive',
                'penetrance': 1.0,
                'chromosome': '15q23'
            },
            'PAH': {
                'disorders': ['Phenylketonuria'],
                'inheritance': 'autosomal_recessive',
                'penetrance': 1.0,
                'chromosome': '12q23'
            },
            'APOE': {
                'disorders': ['Alzheimer Disease'],
                'inheritance': 'complex',
                'penetrance': 0.30,
                'chromosome': '19q13'
            },
            'HFE': {
                'disorders': ['Hemochromatosis'],
                'inheritance': 'autosomal_recessive',
                'penetrance': 0.50,
                'chromosome': '6p22'
            }
        }
        
        # Mutation types and their frequencies
        self.mutation_types = {
            'missense': {'frequency': 0.45, 'severity': 'moderate'},
            'nonsense': {'frequency': 0.15, 'severity': 'severe'},
            'frameshift': {'frequency': 0.12, 'severity': 'severe'},
            'splice_site': {'frequency': 0.10, 'severity': 'moderate_severe'},
            'deletion': {'frequency': 0.08, 'severity': 'severe'},
            'insertion': {'frequency': 0.05, 'severity': 'moderate'},
            'duplication': {'frequency': 0.03, 'severity': 'moderate'},
            'inversion': {'frequency': 0.02, 'severity': 'variable'}
        }
        
        # Chromosomal anomalies
        self.chromosomal_anomalies = {
            'trisomy_21': {'name': 'Down Syndrome', 'frequency': 0.001},
            'trisomy_18': {'name': 'Edwards Syndrome', 'frequency': 0.0003},
            'trisomy_13': {'name': 'Patau Syndrome', 'frequency': 0.0002},
            'monosomy_x': {'name': 'Turner Syndrome', 'frequency': 0.0004},
            'xxy': {'name': 'Klinefelter Syndrome', 'frequency': 0.0015},
            'deletion_22q11': {'name': 'DiGeorge Syndrome', 'frequency': 0.0025}
        }
    
    def generate_profile(self, patient_data, family_history, symptoms, ethnicity=None):
        """
        Generate comprehensive synthetic genomic profile
        
        Args:
            patient_data: dict with age, gender, etc.
            family_history: dict with family disorder history
            symptoms: list of reported symptoms
            ethnicity: patient ethnicity
        
        Returns:
            dict with complete genomic profile
        """
        profile = {
            'profile_id': self._generate_profile_id(),
            'generated_at': datetime.now().isoformat(),
            'patient_info': patient_data,
            'carrier_probabilities': {},
            'mutation_likelihood': {},
            'gene_pathway_map': {},
            'chromosomal_risk': {},
            'trait_predictions': {},
            'pharmacogenomics': {},
            'summary': {}
        }
        
        # Analyze family history to identify relevant genes
        relevant_genes = self._identify_relevant_genes(family_history, symptoms)
        
        # Calculate carrier probabilities
        profile['carrier_probabilities'] = self._calculate_carrier_probabilities(
            relevant_genes, family_history, ethnicity
        )
        
        # Estimate mutation likelihood
        profile['mutation_likelihood'] = self._estimate_mutation_likelihood(
            relevant_genes, family_history, symptoms
        )
        
        # Generate gene-pathway influence map
        profile['gene_pathway_map'] = self._generate_pathway_map(relevant_genes)
        
        # Assess chromosomal anomaly risk
        profile['chromosomal_risk'] = self._assess_chromosomal_risk(
            patient_data, family_history
        )
        
        # Predict genetic traits
        profile['trait_predictions'] = self._predict_traits(
            patient_data, ethnicity
        )
        
        # Pharmacogenomic predictions
        profile['pharmacogenomics'] = self._generate_pharmacogenomics(
            relevant_genes, ethnicity
        )
        
        # Generate summary
        profile['summary'] = self._generate_summary(profile)
        
        return profile
    
    def _generate_profile_id(self):
        """Generate unique profile ID"""
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        random_suffix = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=6))
        return f'GP-{timestamp}-{random_suffix}'
    
    def _identify_relevant_genes(self, family_history, symptoms):
        """Identify genes relevant to patient's presentation"""
        relevant_genes = []
        
        # Check family history
        if family_history.get('has_history'):
            disorders = family_history.get('disorders', [])
            for gene, data in self.gene_associations.items():
                for disorder in disorders:
                    if any(d.lower() in disorder.lower() for d in data['disorders']):
                        relevant_genes.append(gene)
        
        # Check symptoms (simplified mapping)
        symptom_gene_map = {
            'muscle_weakness': ['DMD', 'HTT'],
            'breathing_difficulties': ['CFTR', 'DMD'],
            'unusual_bleeding': ['F8', 'F9'],
            'developmental_delays': ['HEXA', 'PAH'],
            'seizures': ['HEXA'],
            'cognitive_impairment': ['HTT', 'APOE']
        }
        
        for symptom in symptoms:
            if symptom in symptom_gene_map:
                relevant_genes.extend(symptom_gene_map[symptom])
        
        # Remove duplicates
        return list(set(relevant_genes))
    
    def _calculate_carrier_probabilities(self, genes, family_history, ethnicity):
        """Calculate probability of being a carrier for each gene"""
        carrier_probs = {}
        
        for gene in genes:
            gene_data = self.gene_associations.get(gene, {})
            inheritance = gene_data.get('inheritance', 'unknown')
            
            # Base carrier probability
            base_prob = 0.01  # 1% baseline
            
            # Adjust for inheritance pattern
            if inheritance == 'autosomal_recessive':
                base_prob = 0.04  # 4% for recessive
            elif inheritance == 'x_linked_recessive':
                base_prob = 0.02  # 2% for X-linked
            
            # Adjust for family history
            if family_history.get('has_history'):
                affected_relatives = family_history.get('affected_relatives', [])
                if 'parent' in affected_relatives:
                    base_prob *= 50.0  # 50x if parent affected
                elif 'sibling' in affected_relatives:
                    base_prob *= 25.0  # 25x if sibling affected
                elif 'grandparent' in affected_relatives:
                    base_prob *= 10.0  # 10x if grandparent affected
            
            # Adjust for ethnicity
            ethnicity_factors = {
                'ashkenazi_jewish': {'HEXA': 30.0, 'BRCA1': 10.0, 'BRCA2': 10.0},
                'african': {'HBB': 12.0},
                'mediterranean': {'HBB': 8.0},
                'caucasian': {'CFTR': 25.0, 'HFE': 10.0}
            }
            
            if ethnicity:
                ethnicity_key = ethnicity.lower().replace(' ', '_')
                if ethnicity_key in ethnicity_factors:
                    factor = ethnicity_factors[ethnicity_key].get(gene, 1.0)
                    base_prob *= factor
            
            # Cap at 95%
            final_prob = min(base_prob, 0.95)
            
            carrier_probs[gene] = {
                'probability': round(final_prob * 100, 2),
                'confidence': self._calculate_confidence(final_prob),
                'inheritance_pattern': inheritance,
                'chromosome': gene_data.get('chromosome', 'Unknown'),
                'status': self._determine_carrier_status(final_prob)
            }
        
        return carrier_probs
    
    def _estimate_mutation_likelihood(self, genes, family_history, symptoms):
        """Estimate likelihood of pathogenic mutations"""
        mutation_likelihood = {}
        
        for gene in genes:
            gene_data = self.gene_associations.get(gene, {})
            penetrance = gene_data.get('penetrance', 0.5)
            
            # Calculate base likelihood
            base_likelihood = 0.005  # 0.5% baseline
            
            # Adjust for family history
            if family_history.get('has_history'):
                base_likelihood *= 20.0
            
            # Adjust for symptoms
            if symptoms:
                symptom_match = len(symptoms) * 0.1
                base_likelihood *= (1.0 + symptom_match)
            
            # Adjust for penetrance
            base_likelihood *= penetrance
            
            # Cap at 90%
            final_likelihood = min(base_likelihood, 0.90)
            
            # Determine most likely mutation type
            mutation_type = self._predict_mutation_type(gene, final_likelihood)
            
            mutation_likelihood[gene] = {
                'likelihood_percentage': round(final_likelihood * 100, 2),
                'confidence': self._calculate_confidence(final_likelihood),
                'predicted_mutation_type': mutation_type,
                'pathogenicity': self._assess_pathogenicity(final_likelihood),
                'clinical_significance': self._determine_clinical_significance(final_likelihood)
            }
        
        return mutation_likelihood
    
    def _generate_pathway_map(self, genes):
        """Generate gene-pathway influence map"""
        pathway_map = {}
        
        # Biological pathways
        pathways = {
            'DNA_repair': ['BRCA1', 'BRCA2'],
            'cell_cycle_regulation': ['BRCA1', 'BRCA2'],
            'ion_transport': ['CFTR'],
            'protein_folding': ['CFTR'],
            'transcription_regulation': ['HTT'],
            'oxygen_transport': ['HBB'],
            'muscle_structure': ['DMD'],
            'blood_coagulation': ['F8', 'F9'],
            'lipid_metabolism': ['HEXA', 'APOE'],
            'amino_acid_metabolism': ['PAH'],
            'iron_metabolism': ['HFE']
        }
        
        for pathway, pathway_genes in pathways.items():
            affected_genes = [g for g in genes if g in pathway_genes]
            if affected_genes:
                pathway_map[pathway] = {
                    'affected_genes': affected_genes,
                    'impact_level': self._calculate_pathway_impact(len(affected_genes)),
                    'downstream_effects': self._predict_downstream_effects(pathway)
                }
        
        return pathway_map
    
    def _assess_chromosomal_risk(self, patient_data, family_history):
        """Assess risk of chromosomal anomalies"""
        chromosomal_risk = {}
        
        age = patient_data.get('age', 30)
        
        for anomaly, data in self.chromosomal_anomalies.items():
            base_risk = data['frequency']
            
            # Age-based adjustment (maternal age effect)
            if age > 35:
                age_factor = 1.0 + ((age - 35) * 0.1)
                base_risk *= age_factor
            
            # Family history adjustment
            if family_history.get('has_history'):
                base_risk *= 2.0
            
            risk_percentage = base_risk * 100
            
            chromosomal_risk[anomaly] = {
                'name': data['name'],
                'risk_percentage': round(risk_percentage, 4),
                'risk_category': self._categorize_chromosomal_risk(risk_percentage),
                'recommendation': self._get_chromosomal_recommendation(risk_percentage)
            }
        
        return chromosomal_risk
    
    def _predict_traits(self, patient_data, ethnicity):
        """Predict genetic traits"""
        traits = {
            'lactose_tolerance': {
                'prediction': self._predict_lactose_tolerance(ethnicity),
                'confidence': 'Moderate'
            },
            'caffeine_metabolism': {
                'prediction': random.choice(['Fast', 'Normal', 'Slow']),
                'confidence': 'Low'
            },
            'alcohol_metabolism': {
                'prediction': random.choice(['Fast', 'Normal', 'Slow']),
                'confidence': 'Low'
            },
            'vitamin_d_synthesis': {
                'prediction': self._predict_vitamin_d(ethnicity),
                'confidence': 'Moderate'
            }
        }
        
        return traits
    
    def _generate_pharmacogenomics(self, genes, ethnicity):
        """Generate pharmacogenomic predictions"""
        pharmacogenomics = {
            'drug_metabolism': {
                'CYP2D6': {
                    'predicted_phenotype': random.choice(['Normal', 'Intermediate', 'Poor', 'Ultra-rapid']),
                    'affected_drugs': ['Codeine', 'Tamoxifen', 'Antidepressants'],
                    'recommendation': 'Standard dosing may need adjustment'
                },
                'CYP2C19': {
                    'predicted_phenotype': random.choice(['Normal', 'Intermediate', 'Poor']),
                    'affected_drugs': ['Clopidogrel', 'PPIs', 'Antidepressants'],
                    'recommendation': 'Monitor therapeutic response'
                }
            },
            'drug_response': {
                'warfarin_sensitivity': random.choice(['Normal', 'Increased', 'Decreased']),
                'statin_response': random.choice(['Normal', 'Increased risk of myopathy'])
            }
        }
        
        return pharmacogenomics
    
    def _generate_summary(self, profile):
        """Generate profile summary"""
        carrier_count = len([c for c in profile['carrier_probabilities'].values() 
                           if c['probability'] > 10])
        high_risk_mutations = len([m for m in profile['mutation_likelihood'].values() 
                                  if m['likelihood_percentage'] > 20])
        
        return {
            'total_genes_analyzed': len(profile['carrier_probabilities']),
            'high_probability_carrier_status': carrier_count,
            'high_risk_mutations': high_risk_mutations,
            'pathways_affected': len(profile['gene_pathway_map']),
            'chromosomal_anomalies_assessed': len(profile['chromosomal_risk']),
            'overall_genetic_risk': self._calculate_overall_risk(profile),
            'key_findings': self._extract_key_findings(profile),
            'recommendations': self._generate_recommendations(profile)
        }
    
    def _predict_mutation_type(self, gene, likelihood):
        """Predict most likely mutation type"""
        # Weight by frequency and likelihood
        weighted_types = []
        for mut_type, data in self.mutation_types.items():
            weight = data['frequency'] * likelihood
            weighted_types.append((mut_type, weight))
        
        weighted_types.sort(key=lambda x: x[1], reverse=True)
        return weighted_types[0][0] if weighted_types else 'unknown'
    
    def _calculate_confidence(self, probability):
        """Calculate confidence level"""
        if probability > 0.5:
            return 'High'
        elif probability > 0.2:
            return 'Moderate'
        else:
            return 'Low'
    
    def _determine_carrier_status(self, probability):
        """Determine carrier status"""
        if probability > 0.5:
            return 'Likely Carrier'
        elif probability > 0.2:
            return 'Possible Carrier'
        else:
            return 'Unlikely Carrier'
    
    def _assess_pathogenicity(self, likelihood):
        """Assess mutation pathogenicity"""
        if likelihood > 0.5:
            return 'Likely Pathogenic'
        elif likelihood > 0.2:
            return 'Uncertain Significance'
        else:
            return 'Likely Benign'
    
    def _determine_clinical_significance(self, likelihood):
        """Determine clinical significance"""
        if likelihood > 0.5:
            return 'High - Genetic testing recommended'
        elif likelihood > 0.2:
            return 'Moderate - Consider genetic counseling'
        else:
            return 'Low - Routine monitoring'
    
    def _calculate_pathway_impact(self, gene_count):
        """Calculate pathway impact level"""
        if gene_count >= 3:
            return 'High'
        elif gene_count >= 2:
            return 'Moderate'
        else:
            return 'Low'
    
    def _predict_downstream_effects(self, pathway):
        """Predict downstream effects of pathway disruption"""
        effects = {
            'DNA_repair': ['Increased cancer risk', 'Genomic instability'],
            'cell_cycle_regulation': ['Uncontrolled cell growth', 'Tumor formation'],
            'ion_transport': ['Electrolyte imbalance', 'Organ dysfunction'],
            'oxygen_transport': ['Anemia', 'Tissue hypoxia'],
            'muscle_structure': ['Progressive weakness', 'Mobility impairment'],
            'blood_coagulation': ['Bleeding disorders', 'Clotting abnormalities']
        }
        return effects.get(pathway, ['Unknown effects'])
    
    def _categorize_chromosomal_risk(self, risk_percentage):
        """Categorize chromosomal risk"""
        if risk_percentage > 1.0:
            return 'High'
        elif risk_percentage > 0.1:
            return 'Moderate'
        else:
            return 'Low'
    
    def _get_chromosomal_recommendation(self, risk_percentage):
        """Get recommendation based on chromosomal risk"""
        if risk_percentage > 1.0:
            return 'Prenatal testing strongly recommended'
        elif risk_percentage > 0.1:
            return 'Consider prenatal screening'
        else:
            return 'Routine prenatal care'
    
    def _predict_lactose_tolerance(self, ethnicity):
        """Predict lactose tolerance based on ethnicity"""
        intolerant_populations = ['east_asian', 'african', 'hispanic']
        if ethnicity and any(pop in ethnicity.lower() for pop in intolerant_populations):
            return 'Likely Intolerant'
        return 'Likely Tolerant'
    
    def _predict_vitamin_d(self, ethnicity):
        """Predict vitamin D synthesis efficiency"""
        if ethnicity and 'african' in ethnicity.lower():
            return 'Reduced (darker skin)'
        return 'Normal'
    
    def _calculate_overall_risk(self, profile):
        """Calculate overall genetic risk score"""
        carrier_risk = sum(c['probability'] for c in profile['carrier_probabilities'].values())
        mutation_risk = sum(m['likelihood_percentage'] for m in profile['mutation_likelihood'].values())
        
        total_risk = (carrier_risk + mutation_risk) / 2
        
        if total_risk > 50:
            return 'High'
        elif total_risk > 20:
            return 'Moderate'
        else:
            return 'Low'
    
    def _extract_key_findings(self, profile):
        """Extract key findings from profile"""
        findings = []
        
        # High probability carriers
        for gene, data in profile['carrier_probabilities'].items():
            if data['probability'] > 25:
                findings.append(f"High carrier probability for {gene} ({data['probability']}%)")
        
        # High risk mutations
        for gene, data in profile['mutation_likelihood'].items():
            if data['likelihood_percentage'] > 20:
                findings.append(f"Elevated mutation risk in {gene} ({data['likelihood_percentage']}%)")
        
        return findings[:5]  # Top 5 findings
    
    def _generate_recommendations(self, profile):
        """Generate clinical recommendations"""
        recommendations = []
        
        # Check carrier probabilities
        high_carrier = [g for g, d in profile['carrier_probabilities'].items() 
                       if d['probability'] > 25]
        if high_carrier:
            recommendations.append(f"Genetic testing recommended for: {', '.join(high_carrier)}")
        
        # Check mutation likelihood
        high_mutation = [g for g, d in profile['mutation_likelihood'].items() 
                        if d['likelihood_percentage'] > 20]
        if high_mutation:
            recommendations.append("Genetic counseling strongly advised")
        
        # Pathway analysis
        if len(profile['gene_pathway_map']) > 2:
            recommendations.append("Multi-system evaluation recommended")
        
        return recommendations
