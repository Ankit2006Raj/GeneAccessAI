"""
Inheritance Simulation Mode - Predict Baby's Genetic Risk
Simulates genetic inheritance patterns for family planning
"""
import random
from typing import Dict, List, Any, Tuple
from datetime import datetime


class InheritanceSimulator:
    """
    Simulates genetic inheritance patterns to predict offspring risk.
    Provides pre-marital and reproductive counseling.
    """
    
    def __init__(self):
        # Inheritance patterns
        self.inheritance_patterns = {
            'autosomal_dominant': {
                'description': 'One mutated gene from either parent causes disorder',
                'examples': ['Huntington Disease', 'Marfan Syndrome', 'Achondroplasia'],
                'risk_calculation': 'affected_parent'
            },
            'autosomal_recessive': {
                'description': 'Two mutated genes (one from each parent) required',
                'examples': ['Cystic Fibrosis', 'Sickle Cell Disease', 'Tay-Sachs'],
                'risk_calculation': 'both_carriers'
            },
            'x_linked_recessive': {
                'description': 'Mutation on X chromosome, mainly affects males',
                'examples': ['Hemophilia', 'Duchenne Muscular Dystrophy', 'Color Blindness'],
                'risk_calculation': 'x_linked'
            },
            'x_linked_dominant': {
                'description': 'Mutation on X chromosome, affects both sexes',
                'examples': ['Rett Syndrome', 'Fragile X Syndrome'],
                'risk_calculation': 'x_linked_dominant'
            },
            'mitochondrial': {
                'description': 'Inherited from mother only',
                'examples': ['MELAS', 'LHON'],
                'risk_calculation': 'maternal'
            }
        }
        
        # Disorder database with inheritance patterns
        self.disorder_database = {
            'Huntington Disease': {
                'pattern': 'autosomal_dominant',
                'penetrance': 100,
                'onset_age': '30-50 years'
            },
            'Cystic Fibrosis': {
                'pattern': 'autosomal_recessive',
                'penetrance': 100,
                'onset_age': 'Birth/early childhood'
            },
            'Sickle Cell Disease': {
                'pattern': 'autosomal_recessive',
                'penetrance': 100,
                'onset_age': 'Early childhood'
            },
            'Hemophilia A': {
                'pattern': 'x_linked_recessive',
                'penetrance': 100,
                'onset_age': 'Early childhood'
            },
            'Duchenne Muscular Dystrophy': {
                'pattern': 'x_linked_recessive',
                'penetrance': 100,
                'onset_age': '2-6 years'
            },
            'Tay-Sachs Disease': {
                'pattern': 'autosomal_recessive',
                'penetrance': 100,
                'onset_age': '6 months'
            },
            'Marfan Syndrome': {
                'pattern': 'autosomal_dominant',
                'penetrance': 100,
                'onset_age': 'Variable'
            }
        }
    
    def simulate_offspring_risk(
        self,
        parent1_data: Dict[str, Any],
        parent2_data: Dict[str, Any],
        disorder: str,
        num_simulations: int = 1000
    ) -> Dict[str, Any]:
        """
        Simulate genetic inheritance for offspring.
        
        Args:
            parent1_data: First parent's genetic data
            parent2_data: Second parent's genetic data
            disorder: Genetic disorder to simulate
            num_simulations: Number of inheritance scenarios to simulate
        
        Returns:
            Comprehensive inheritance risk assessment
        """
        
        if disorder not in self.disorder_database:
            return {
                'success': False,
                'error': f'Disorder {disorder} not in database'
            }
        
        disorder_info = self.disorder_database[disorder]
        pattern = disorder_info['pattern']
        
        # Run simulations
        results = self._run_simulations(
            parent1_data, parent2_data, disorder, pattern, num_simulations
        )
        
        # Calculate probabilities
        probabilities = self._calculate_probabilities(results, pattern)
        
        # Generate Punnett square
        punnett_square = self._generate_punnett_square(
            parent1_data, parent2_data, pattern
        )
        
        # Generate recommendations
        recommendations = self._generate_reproductive_recommendations(
            probabilities, disorder, disorder_info
        )
        
        return {
            'success': True,
            'disorder': disorder,
            'inheritance_pattern': pattern,
            'pattern_description': self.inheritance_patterns[pattern]['description'],
            'simulations_run': num_simulations,
            'probabilities': probabilities,
            'punnett_square': punnett_square,
            'recommendations': recommendations,
            'counseling_summary': self._generate_counseling_summary(
                probabilities, disorder, disorder_info
            ),
            'timestamp': datetime.now().isoformat()
        }
    
    def _run_simulations(
        self,
        parent1: Dict,
        parent2: Dict,
        disorder: str,
        pattern: str,
        num_sims: int
    ) -> Dict[str, int]:
        """Run Monte Carlo simulations of inheritance."""
        
        results = {
            'affected': 0,
            'carrier': 0,
            'unaffected': 0,
            'male_affected': 0,
            'female_affected': 0
        }
        
        for _ in range(num_sims):
            # Simulate offspring genotype
            offspring = self._simulate_single_inheritance(parent1, parent2, pattern)
            
            # Categorize result
            if offspring['affected']:
                results['affected'] += 1
                if offspring['sex'] == 'male':
                    results['male_affected'] += 1
                else:
                    results['female_affected'] += 1
            elif offspring['carrier']:
                results['carrier'] += 1
            else:
                results['unaffected'] += 1
        
        return results
    
    def _simulate_single_inheritance(
        self,
        parent1: Dict,
        parent2: Dict,
        pattern: str
    ) -> Dict[str, Any]:
        """Simulate single offspring inheritance."""
        
        # Determine offspring sex
        sex = random.choice(['male', 'female'])
        
        # Get parent genotypes
        p1_status = parent1.get('genetic_status', 'unaffected')
        p2_status = parent2.get('genetic_status', 'unaffected')
        
        if pattern == 'autosomal_dominant':
            # One affected parent = 50% chance
            affected = False
            carrier = False
            
            if p1_status == 'affected' or p2_status == 'affected':
                affected = random.random() < 0.5
            
        elif pattern == 'autosomal_recessive':
            # Both carriers = 25% affected, 50% carrier, 25% unaffected
            affected = False
            carrier = False
            
            if p1_status in ['affected', 'carrier'] and p2_status in ['affected', 'carrier']:
                rand = random.random()
                if rand < 0.25:
                    affected = True
                elif rand < 0.75:
                    carrier = True
            elif p1_status in ['affected', 'carrier'] or p2_status in ['affected', 'carrier']:
                carrier = random.random() < 0.5
        
        elif pattern == 'x_linked_recessive':
            # Mother carrier, male offspring = 50% affected
            # Mother carrier, female offspring = 50% carrier
            affected = False
            carrier = False
            
            mother = parent1 if parent1.get('sex') == 'female' else parent2
            mother_status = mother.get('genetic_status', 'unaffected')
            
            if mother_status in ['affected', 'carrier']:
                if sex == 'male':
                    affected = random.random() < 0.5
                else:
                    carrier = random.random() < 0.5
        
        elif pattern == 'mitochondrial':
            # Inherited from mother only
            mother = parent1 if parent1.get('sex') == 'female' else parent2
            affected = mother.get('genetic_status') == 'affected'
            carrier = False
        
        else:
            affected = False
            carrier = False
        
        return {
            'sex': sex,
            'affected': affected,
            'carrier': carrier
        }
    
    def _calculate_probabilities(
        self,
        results: Dict[str, int],
        pattern: str
    ) -> Dict[str, Any]:
        """Calculate inheritance probabilities from simulation results."""
        
        total = sum([results['affected'], results['carrier'], results['unaffected']])
        
        probabilities = {
            'affected': round((results['affected'] / total) * 100, 2),
            'carrier': round((results['carrier'] / total) * 100, 2),
            'unaffected': round((results['unaffected'] / total) * 100, 2)
        }
        
        if pattern == 'x_linked_recessive':
            male_total = results['male_affected'] + (total - results['affected']) / 2
            probabilities['male_affected'] = round(
                (results['male_affected'] / male_total) * 100, 2
            ) if male_total > 0 else 0
            
            female_total = results['female_affected'] + (total - results['affected']) / 2
            probabilities['female_affected'] = round(
                (results['female_affected'] / female_total) * 100, 2
            ) if female_total > 0 else 0
        
        return probabilities
    
    def _generate_punnett_square(
        self,
        parent1: Dict,
        parent2: Dict,
        pattern: str
    ) -> Dict[str, Any]:
        """Generate Punnett square for visualization."""
        
        p1_status = parent1.get('genetic_status', 'unaffected')
        p2_status = parent2.get('genetic_status', 'unaffected')
        
        if pattern == 'autosomal_dominant':
            # A = affected allele, a = normal allele
            p1_alleles = ['A', 'a'] if p1_status == 'affected' else ['a', 'a']
            p2_alleles = ['A', 'a'] if p2_status == 'affected' else ['a', 'a']
            
            square = {
                'parent1_alleles': p1_alleles,
                'parent2_alleles': p2_alleles,
                'offspring': [
                    [f'{p1_alleles[0]}{p2_alleles[0]}', f'{p1_alleles[0]}{p2_alleles[1]}'],
                    [f'{p1_alleles[1]}{p2_alleles[0]}', f'{p1_alleles[1]}{p2_alleles[1]}']
                ]
            }
        
        elif pattern == 'autosomal_recessive':
            # a = affected allele, A = normal allele
            p1_alleles = ['a', 'a'] if p1_status == 'affected' else \
                        ['A', 'a'] if p1_status == 'carrier' else ['A', 'A']
            p2_alleles = ['a', 'a'] if p2_status == 'affected' else \
                        ['A', 'a'] if p2_status == 'carrier' else ['A', 'A']
            
            square = {
                'parent1_alleles': p1_alleles,
                'parent2_alleles': p2_alleles,
                'offspring': [
                    [f'{p1_alleles[0]}{p2_alleles[0]}', f'{p1_alleles[0]}{p2_alleles[1]}'],
                    [f'{p1_alleles[1]}{p2_alleles[0]}', f'{p1_alleles[1]}{p2_alleles[1]}']
                ]
            }
        
        else:
            square = {
                'note': f'Punnett square for {pattern} requires specialized visualization'
            }
        
        return square
    
    def _generate_reproductive_recommendations(
        self,
        probabilities: Dict,
        disorder: str,
        disorder_info: Dict
    ) -> List[Dict[str, Any]]:
        """Generate reproductive counseling recommendations."""
        
        recommendations = []
        
        affected_risk = probabilities['affected']
        
        # High risk recommendations
        if affected_risk >= 50:
            recommendations.append({
                'priority': 'Critical',
                'category': 'Genetic Counseling',
                'recommendation': 'Comprehensive genetic counseling strongly recommended before conception',
                'details': [
                    'Discuss all reproductive options',
                    'Consider preimplantation genetic diagnosis (PGD)',
                    'Explore prenatal testing options',
                    'Review adoption or donor gametes'
                ]
            })
        
        elif affected_risk >= 25:
            recommendations.append({
                'priority': 'High',
                'category': 'Genetic Counseling',
                'recommendation': 'Genetic counseling recommended',
                'details': [
                    'Discuss inheritance patterns',
                    'Review testing options',
                    'Plan for prenatal care'
                ]
            })
        
        # Carrier screening
        if probabilities.get('carrier', 0) > 0:
            recommendations.append({
                'priority': 'Moderate',
                'category': 'Carrier Screening',
                'recommendation': 'Carrier screening for future generations',
                'details': [
                    'Children should be informed of carrier status',
                    'Cascade screening for extended family',
                    'Genetic counseling for carriers'
                ]
            })
        
        # Prenatal testing
        if affected_risk > 0:
            recommendations.append({
                'priority': 'High',
                'category': 'Prenatal Testing',
                'recommendation': 'Prenatal testing options available',
                'details': [
                    'Chorionic villus sampling (CVS) at 10-13 weeks',
                    'Amniocentesis at 15-20 weeks',
                    'Non-invasive prenatal testing (NIPT) if applicable',
                    'Ultrasound monitoring'
                ]
            })
        
        # PGD option
        if affected_risk >= 25:
            recommendations.append({
                'priority': 'High',
                'category': 'Assisted Reproduction',
                'recommendation': 'Preimplantation Genetic Diagnosis (PGD) available',
                'details': [
                    'IVF with genetic testing of embryos',
                    'Select unaffected embryos for implantation',
                    'High success rate for preventing disorder',
                    'Discuss with fertility specialist'
                ]
            })
        
        # Support resources
        recommendations.append({
            'priority': 'Important',
            'category': 'Support Resources',
            'recommendation': 'Connect with support organizations',
            'details': [
                f'{disorder} support groups',
                'Family planning resources',
                'Financial assistance programs',
                'Mental health support'
            ]
        })
        
        return recommendations
    
    def _generate_counseling_summary(
        self,
        probabilities: Dict,
        disorder: str,
        disorder_info: Dict
    ) -> Dict[str, Any]:
        """Generate comprehensive counseling summary."""
        
        affected_risk = probabilities['affected']
        
        # Risk interpretation
        if affected_risk >= 50:
            risk_level = 'High'
            interpretation = 'There is a high probability that offspring will be affected'
        elif affected_risk >= 25:
            risk_level = 'Moderate-High'
            interpretation = 'There is a significant probability that offspring will be affected'
        elif affected_risk >= 10:
            risk_level = 'Moderate'
            interpretation = 'There is a moderate probability that offspring will be affected'
        else:
            risk_level = 'Low'
            interpretation = 'The probability of affected offspring is low'
        
        # Key points
        key_points = [
            f'Inheritance pattern: {disorder_info["pattern"]}',
            f'Probability of affected child: {affected_risk}%',
            f'Typical onset age: {disorder_info["onset_age"]}',
            f'Penetrance: {disorder_info["penetrance"]}%'
        ]
        
        if probabilities.get('carrier', 0) > 0:
            key_points.append(
                f'Probability of carrier child: {probabilities["carrier"]}%'
            )
        
        return {
            'risk_level': risk_level,
            'interpretation': interpretation,
            'key_points': key_points,
            'discussion_topics': [
                'Understanding inheritance patterns',
                'Reproductive options and alternatives',
                'Prenatal testing and diagnosis',
                'Life with the condition',
                'Support and resources',
                'Ethical considerations',
                'Family planning decisions'
            ]
        }
    
    def compare_multiple_disorders(
        self,
        parent1_data: Dict,
        parent2_data: Dict,
        disorders: List[str]
    ) -> Dict[str, Any]:
        """Compare inheritance risks for multiple disorders."""
        
        comparisons = []
        
        for disorder in disorders:
            if disorder in self.disorder_database:
                result = self.simulate_offspring_risk(
                    parent1_data, parent2_data, disorder, num_simulations=1000
                )
                
                if result['success']:
                    comparisons.append({
                        'disorder': disorder,
                        'affected_probability': result['probabilities']['affected'],
                        'carrier_probability': result['probabilities'].get('carrier', 0),
                        'inheritance_pattern': result['inheritance_pattern'],
                        'risk_level': result['counseling_summary']['risk_level']
                    })
        
        # Sort by risk
        comparisons.sort(key=lambda x: x['affected_probability'], reverse=True)
        
        return {
            'success': True,
            'disorders_compared': len(comparisons),
            'comparisons': comparisons,
            'highest_risk': comparisons[0] if comparisons else None,
            'recommendation': 'Prioritize counseling for highest-risk disorders'
        }
    
    def generate_family_planning_report(
        self,
        parent1_data: Dict,
        parent2_data: Dict,
        disorders: List[str]
    ) -> Dict[str, Any]:
        """Generate comprehensive family planning report."""
        
        # Run simulations for all disorders
        disorder_results = []
        for disorder in disorders:
            if disorder in self.disorder_database:
                result = self.simulate_offspring_risk(
                    parent1_data, parent2_data, disorder
                )
                if result['success']:
                    disorder_results.append(result)
        
        # Calculate overall risk
        max_risk = max([r['probabilities']['affected'] for r in disorder_results]) \
                   if disorder_results else 0
        
        # Generate comprehensive recommendations
        all_recommendations = []
        for result in disorder_results:
            all_recommendations.extend(result['recommendations'])
        
        # Deduplicate recommendations
        unique_recs = []
        seen = set()
        for rec in all_recommendations:
            key = (rec['category'], rec['recommendation'])
            if key not in seen:
                seen.add(key)
                unique_recs.append(rec)
        
        return {
            'success': True,
            'report_date': datetime.now().isoformat(),
            'parents': {
                'parent1': parent1_data.get('name', 'Parent 1'),
                'parent2': parent2_data.get('name', 'Parent 2')
            },
            'disorders_assessed': len(disorder_results),
            'overall_risk_level': 'High' if max_risk >= 50 else \
                                 'Moderate' if max_risk >= 25 else 'Low',
            'maximum_risk': max_risk,
            'disorder_details': disorder_results,
            'consolidated_recommendations': unique_recs,
            'next_steps': [
                'Schedule genetic counseling appointment',
                'Discuss reproductive options',
                'Consider genetic testing if not done',
                'Review prenatal care options',
                'Connect with support resources'
            ]
        }
