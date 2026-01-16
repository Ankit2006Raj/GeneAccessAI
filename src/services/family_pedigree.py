"""
Family Pedigree AI - Automatic Pedigree Chart Builder
Generates multi-generation family trees with genetic inheritance analysis
"""

import json
from datetime import datetime
from collections import defaultdict

class FamilyPedigreeAI:
    """
    Advanced pedigree analysis system that:
    - Auto-creates multi-generation family trees
    - Detects genetic inheritance patterns (autosomal dominant/recessive, X-linked)
    - Colors risk levels across family members
    - Flags high-risk hereditary lines
    - Calculates carrier probabilities
    """
    
    def __init__(self):
        # Inheritance pattern definitions
        self.inheritance_patterns = {
            'autosomal_dominant': {
                'description': 'One mutated gene from either parent causes disorder',
                'transmission_probability': 0.5,
                'examples': ['Huntington Disease', 'Marfan Syndrome', 'Neurofibromatosis']
            },
            'autosomal_recessive': {
                'description': 'Two mutated genes (one from each parent) needed',
                'transmission_probability': 0.25,
                'carrier_probability': 0.5,
                'examples': ['Cystic Fibrosis', 'Sickle Cell Anemia', 'Thalassemia']
            },
            'x_linked_recessive': {
                'description': 'Mutation on X chromosome, mainly affects males',
                'male_affected_probability': 0.5,
                'female_carrier_probability': 0.5,
                'examples': ['Hemophilia', 'Duchenne Muscular Dystrophy', 'Color Blindness']
            },
            'x_linked_dominant': {
                'description': 'Mutation on X chromosome, affects both sexes',
                'transmission_probability': 0.5,
                'examples': ['Rett Syndrome', 'Fragile X Syndrome']
            },
            'mitochondrial': {
                'description': 'Inherited through maternal line only',
                'transmission_probability': 1.0,
                'examples': ['MELAS', 'LHON']
            }
        }
        
        # Risk color coding
        self.risk_colors = {
            'affected': '#FF4444',      # Red - Has disorder
            'high_risk': '#FF8800',     # Orange - High genetic risk
            'carrier': '#FFBB00',       # Yellow - Carrier
            'moderate_risk': '#88CCFF', # Light blue - Moderate risk
            'low_risk': '#88FF88',      # Light green - Low risk
            'unknown': '#CCCCCC'        # Gray - Unknown status
        }
    
    def build_pedigree(self, family_data, proband_id):
        """
        Build comprehensive family pedigree from family data
        
        Args:
            family_data: List of family members with relationships
            proband_id: ID of the person being assessed (index case)
        
        Returns:
            Complete pedigree structure with analysis
        """
        # Parse and structure family tree
        pedigree_tree = self._structure_family_tree(family_data, proband_id)
        
        # Detect inheritance patterns
        inheritance_analysis = self._analyze_inheritance_patterns(pedigree_tree)
        
        # Calculate risk for each family member
        risk_analysis = self._calculate_family_risks(pedigree_tree, inheritance_analysis)
        
        # Identify high-risk hereditary lines
        high_risk_lines = self._identify_high_risk_lines(pedigree_tree, risk_analysis)
        
        # Generate carrier probability calculations
        carrier_analysis = self._calculate_carrier_probabilities(pedigree_tree, inheritance_analysis)
        
        # Create visualization data
        visualization_data = self._generate_visualization_data(pedigree_tree, risk_analysis)
        
        return {
            'pedigree_tree': pedigree_tree,
            'inheritance_analysis': inheritance_analysis,
            'risk_analysis': risk_analysis,
            'high_risk_lines': high_risk_lines,
            'carrier_analysis': carrier_analysis,
            'visualization_data': visualization_data,
            'recommendations': self._generate_pedigree_recommendations(inheritance_analysis, high_risk_lines),
            'generated_at': datetime.now().isoformat()
        }
    
    def _structure_family_tree(self, family_data, proband_id):
        """Structure family members into generational tree"""
        tree = {
            'proband': None,
            'generations': defaultdict(list),
            'relationships': {},
            'members': {}
        }
        
        # Process each family member
        for member in family_data:
            member_id = member.get('id')
            tree['members'][member_id] = {
                'id': member_id,
                'name': member.get('name', f'Individual {member_id}'),
                'gender': member.get('gender', 'unknown'),
                'age': member.get('age'),
                'generation': member.get('generation', 0),
                'affected': member.get('affected', False),
                'disorders': member.get('disorders', []),
                'carrier_status': member.get('carrier_status', 'unknown'),
                'deceased': member.get('deceased', False),
                'relationship_to_proband': member.get('relationship', 'unknown')
            }
            
            # Add to generation
            generation = member.get('generation', 0)
            tree['generations'][generation].append(member_id)
            
            # Track proband
            if member_id == proband_id:
                tree['proband'] = member_id
            
            # Store relationships
            if 'parents' in member:
                tree['relationships'][member_id] = {
                    'parents': member['parents'],
                    'siblings': member.get('siblings', []),
                    'children': member.get('children', [])
                }
        
        return tree
    
    def _analyze_inheritance_patterns(self, pedigree_tree):
        """Detect inheritance patterns from pedigree"""
        patterns_detected = []
        
        # Analyze affected members across generations
        affected_members = [
            member for member in pedigree_tree['members'].values()
            if member['affected']
        ]
        
        if not affected_members:
            return {
                'detected_patterns': [],
                'confidence': 0,
                'primary_pattern': None
            }
        
        # Check for autosomal dominant pattern
        if self._check_autosomal_dominant(pedigree_tree, affected_members):
            patterns_detected.append({
                'pattern': 'autosomal_dominant',
                'confidence': 0.85,
                'evidence': 'Multiple generations affected, both sexes equally'
            })
        
        # Check for autosomal recessive pattern
        if self._check_autosomal_recessive(pedigree_tree, affected_members):
            patterns_detected.append({
                'pattern': 'autosomal_recessive',
                'confidence': 0.80,
                'evidence': 'Skips generations, consanguinity possible'
            })
        
        # Check for X-linked pattern
        if self._check_x_linked(pedigree_tree, affected_members):
            patterns_detected.append({
                'pattern': 'x_linked_recessive',
                'confidence': 0.90,
                'evidence': 'Predominantly affects males, transmitted through females'
            })
        
        # Check for mitochondrial pattern
        if self._check_mitochondrial(pedigree_tree, affected_members):
            patterns_detected.append({
                'pattern': 'mitochondrial',
                'confidence': 0.95,
                'evidence': 'Maternal transmission only'
            })
        
        # Determine primary pattern
        primary_pattern = None
        if patterns_detected:
            primary_pattern = max(patterns_detected, key=lambda x: x['confidence'])
        
        return {
            'detected_patterns': patterns_detected,
            'primary_pattern': primary_pattern,
            'confidence': primary_pattern['confidence'] if primary_pattern else 0
        }
    
    def _check_autosomal_dominant(self, tree, affected):
        """Check for autosomal dominant inheritance pattern"""
        # Characteristics: appears in every generation, affects both sexes equally
        generations_affected = set(member['generation'] for member in affected)
        
        # Check if multiple consecutive generations affected
        if len(generations_affected) >= 2:
            # Check sex distribution
            males = sum(1 for m in affected if m['gender'] == 'male')
            females = sum(1 for m in affected if m['gender'] == 'female')
            
            # Roughly equal distribution suggests autosomal
            if males > 0 and females > 0:
                return True
        
        return False
    
    def _check_autosomal_recessive(self, tree, affected):
        """Check for autosomal recessive inheritance pattern"""
        # Characteristics: skips generations, siblings affected, consanguinity
        
        # Check if pattern skips generations
        generations_affected = sorted(set(member['generation'] for member in affected))
        
        if len(generations_affected) >= 2:
            # Check for generation gaps
            for i in range(len(generations_affected) - 1):
                if generations_affected[i+1] - generations_affected[i] > 1:
                    return True
        
        # Check for affected siblings with unaffected parents
        for member_id, relationships in tree['relationships'].items():
            if member_id in [m['id'] for m in affected]:
                parents = relationships.get('parents', [])
                if parents:
                    parents_affected = any(
                        tree['members'][p]['affected'] for p in parents if p in tree['members']
                    )
                    if not parents_affected:
                        return True
        
        return False
    
    def _check_x_linked(self, tree, affected):
        """Check for X-linked inheritance pattern"""
        # Characteristics: predominantly males affected, no male-to-male transmission
        
        males_affected = [m for m in affected if m['gender'] == 'male']
        females_affected = [m for m in affected if m['gender'] == 'female']
        
        # X-linked recessive: mostly males
        if len(males_affected) > len(females_affected) * 2:
            # Check for no male-to-male transmission
            for male in males_affected:
                male_id = male['id']
                if male_id in tree['relationships']:
                    children = tree['relationships'][male_id].get('children', [])
                    male_children_affected = [
                        c for c in children
                        if c in tree['members'] and
                        tree['members'][c]['gender'] == 'male' and
                        tree['members'][c]['affected']
                    ]
                    if male_children_affected:
                        return False  # Male-to-male transmission rules out X-linked
            
            return True
        
        return False
    
    def _check_mitochondrial(self, tree, affected):
        """Check for mitochondrial inheritance pattern"""
        # Characteristics: maternal transmission only, all children of affected mother are affected
        
        for member in affected:
            if member['gender'] == 'female' and member['id'] in tree['relationships']:
                children = tree['relationships'][member['id']].get('children', [])
                if children:
                    # All children should be affected in mitochondrial inheritance
                    all_affected = all(
                        tree['members'][c]['affected']
                        for c in children if c in tree['members']
                    )
                    if all_affected:
                        return True
        
        return False
    
    def _calculate_family_risks(self, pedigree_tree, inheritance_analysis):
        """Calculate genetic risk for each family member"""
        risk_scores = {}
        
        primary_pattern = inheritance_analysis.get('primary_pattern')
        if not primary_pattern:
            # No clear pattern, use general risk assessment
            for member_id, member in pedigree_tree['members'].items():
                risk_scores[member_id] = self._calculate_general_risk(member, pedigree_tree)
            return risk_scores
        
        pattern_type = primary_pattern['pattern']
        pattern_info = self.inheritance_patterns.get(pattern_type, {})
        
        # Calculate risk based on inheritance pattern
        for member_id, member in pedigree_tree['members'].items():
            if member['affected']:
                risk_scores[member_id] = {
                    'risk_level': 'affected',
                    'risk_score': 100,
                    'carrier_probability': 100 if pattern_type == 'autosomal_recessive' else 0,
                    'color': self.risk_colors['affected']
                }
            else:
                risk = self._calculate_pattern_based_risk(
                    member, pedigree_tree, pattern_type, pattern_info
                )
                risk_scores[member_id] = risk
        
        return risk_scores
    
    def _calculate_pattern_based_risk(self, member, tree, pattern_type, pattern_info):
        """Calculate risk based on specific inheritance pattern"""
        risk_score = 0
        carrier_prob = 0
        
        # Get affected relatives
        relationships = tree['relationships'].get(member['id'], {})
        parents = relationships.get('parents', [])
        siblings = relationships.get('siblings', [])
        
        parents_affected = sum(
            1 for p in parents
            if p in tree['members'] and tree['members'][p]['affected']
        )
        
        siblings_affected = sum(
            1 for s in siblings
            if s in tree['members'] and tree['members'][s]['affected']
        )
        
        if pattern_type == 'autosomal_dominant':
            if parents_affected > 0:
                risk_score = 50  # 50% chance if one parent affected
            elif siblings_affected > 0:
                risk_score = 25  # Lower risk if sibling affected but not parents
            else:
                risk_score = 5
        
        elif pattern_type == 'autosomal_recessive':
            if parents_affected >= 2:
                risk_score = 100  # Both parents affected
            elif parents_affected == 1:
                carrier_prob = 100
                risk_score = 0
            elif siblings_affected > 0:
                risk_score = 25  # 25% risk if sibling affected
                carrier_prob = 50  # 50% carrier probability
            else:
                carrier_prob = 2  # Population carrier frequency
                risk_score = 1
        
        elif pattern_type == 'x_linked_recessive':
            if member['gender'] == 'male':
                # Males: either affected or not
                if parents_affected > 0 or siblings_affected > 0:
                    risk_score = 50
                else:
                    risk_score = 5
            else:
                # Females: usually carriers
                if parents_affected > 0:
                    carrier_prob = 50
                    risk_score = 10
                else:
                    carrier_prob = 10
                    risk_score = 2
        
        elif pattern_type == 'mitochondrial':
            # Check if mother is affected
            mother_affected = any(
                p in tree['members'] and
                tree['members'][p]['gender'] == 'female' and
                tree['members'][p]['affected']
                for p in parents
            )
            if mother_affected:
                risk_score = 100  # All children of affected mother inherit
            else:
                risk_score = 1
        
        # Determine risk level and color
        if risk_score >= 75:
            risk_level = 'high_risk'
            color = self.risk_colors['high_risk']
        elif risk_score >= 40:
            risk_level = 'moderate_risk'
            color = self.risk_colors['moderate_risk']
        elif carrier_prob >= 50:
            risk_level = 'carrier'
            color = self.risk_colors['carrier']
        else:
            risk_level = 'low_risk'
            color = self.risk_colors['low_risk']
        
        return {
            'risk_level': risk_level,
            'risk_score': risk_score,
            'carrier_probability': carrier_prob,
            'color': color
        }
    
    def _calculate_general_risk(self, member, tree):
        """Calculate general risk when no clear pattern detected"""
        risk_score = 0
        
        # Count affected relatives
        relationships = tree['relationships'].get(member['id'], {})
        parents = relationships.get('parents', [])
        siblings = relationships.get('siblings', [])
        
        for p in parents:
            if p in tree['members'] and tree['members'][p]['affected']:
                risk_score += 30
        
        for s in siblings:
            if s in tree['members'] and tree['members'][s]['affected']:
                risk_score += 15
        
        risk_score = min(risk_score, 100)
        
        if risk_score >= 60:
            risk_level = 'high_risk'
            color = self.risk_colors['high_risk']
        elif risk_score >= 30:
            risk_level = 'moderate_risk'
            color = self.risk_colors['moderate_risk']
        else:
            risk_level = 'low_risk'
            color = self.risk_colors['low_risk']
        
        return {
            'risk_level': risk_level,
            'risk_score': risk_score,
            'carrier_probability': 0,
            'color': color
        }
    
    def _identify_high_risk_lines(self, pedigree_tree, risk_analysis):
        """Identify family lines with high genetic risk"""
        high_risk_lines = []
        
        # Analyze each generation
        for generation, members in pedigree_tree['generations'].items():
            affected_count = sum(
                1 for m_id in members
                if pedigree_tree['members'][m_id]['affected']
            )
            
            high_risk_count = sum(
                1 for m_id in members
                if risk_analysis.get(m_id, {}).get('risk_level') in ['high_risk', 'affected']
            )
            
            if affected_count >= 2 or high_risk_count >= 3:
                high_risk_lines.append({
                    'generation': generation,
                    'affected_count': affected_count,
                    'high_risk_count': high_risk_count,
                    'members': members,
                    'severity': 'high' if affected_count >= 2 else 'moderate'
                })
        
        return high_risk_lines
    
    def _calculate_carrier_probabilities(self, pedigree_tree, inheritance_analysis):
        """Calculate carrier probabilities for family members"""
        carrier_analysis = {}
        
        primary_pattern = inheritance_analysis.get('primary_pattern')
        if not primary_pattern or primary_pattern['pattern'] != 'autosomal_recessive':
            return carrier_analysis
        
        # For autosomal recessive, calculate carrier probabilities
        for member_id, member in pedigree_tree['members'].items():
            if member['affected']:
                carrier_analysis[member_id] = {
                    'carrier_probability': 100,
                    'status': 'affected_carrier'
                }
            else:
                # Calculate based on family history
                relationships = tree['relationships'].get(member_id, {})
                parents = relationships.get('parents', [])
                siblings = relationships.get('siblings', [])
                
                parents_affected = sum(
                    1 for p in parents
                    if p in pedigree_tree['members'] and pedigree_tree['members'][p]['affected']
                )
                
                siblings_affected = sum(
                    1 for s in siblings
                    if s in pedigree_tree['members'] and pedigree_tree['members'][s]['affected']
                )
                
                if parents_affected >= 1:
                    carrier_prob = 100
                elif siblings_affected >= 1:
                    carrier_prob = 66  # 2/3 probability
                else:
                    carrier_prob = 2  # Population frequency
                
                carrier_analysis[member_id] = {
                    'carrier_probability': carrier_prob,
                    'status': 'likely_carrier' if carrier_prob >= 50 else 'possible_carrier'
                }
        
        return carrier_analysis
    
    def _generate_visualization_data(self, pedigree_tree, risk_analysis):
        """Generate data structure for pedigree visualization"""
        nodes = []
        edges = []
        
        # Create nodes for each family member
        for member_id, member in pedigree_tree['members'].items():
            risk_info = risk_analysis.get(member_id, {})
            
            nodes.append({
                'id': member_id,
                'name': member['name'],
                'gender': member['gender'],
                'age': member['age'],
                'generation': member['generation'],
                'affected': member['affected'],
                'deceased': member['deceased'],
                'risk_level': risk_info.get('risk_level', 'unknown'),
                'risk_score': risk_info.get('risk_score', 0),
                'color': risk_info.get('color', self.risk_colors['unknown']),
                'symbol': 'square' if member['gender'] == 'male' else 'circle'
            })
        
        # Create edges for relationships
        for member_id, relationships in pedigree_tree['relationships'].items():
            parents = relationships.get('parents', [])
            for parent in parents:
                edges.append({
                    'from': parent,
                    'to': member_id,
                    'type': 'parent_child'
                })
        
        return {
            'nodes': nodes,
            'edges': edges,
            'legend': self.risk_colors
        }
    
    def _generate_pedigree_recommendations(self, inheritance_analysis, high_risk_lines):
        """Generate recommendations based on pedigree analysis"""
        recommendations = []
        
        primary_pattern = inheritance_analysis.get('primary_pattern')
        
        if primary_pattern:
            pattern_type = primary_pattern['pattern']
            recommendations.append({
                'category': 'Inheritance Pattern',
                'recommendation': f"Pedigree suggests {pattern_type.replace('_', ' ').title()} inheritance",
                'priority': 'High',
                'action': 'Confirm with genetic testing'
            })
        
        if high_risk_lines:
            recommendations.append({
                'category': 'High-Risk Lines',
                'recommendation': f"{len(high_risk_lines)} generation(s) show high genetic risk",
                'priority': 'Critical',
                'action': 'All at-risk family members should undergo genetic counseling'
            })
        
        recommendations.extend([
            {
                'category': 'Genetic Testing',
                'recommendation': 'Cascade screening for all first-degree relatives',
                'priority': 'High',
                'action': 'Schedule genetic testing appointments'
            },
            {
                'category': 'Family Planning',
                'recommendation': 'Preconception genetic counseling for at-risk couples',
                'priority': 'High',
                'action': 'Discuss reproductive options with genetic counselor'
            },
            {
                'category': 'Documentation',
                'recommendation': 'Maintain updated family medical history',
                'priority': 'Moderate',
                'action': 'Update pedigree annually or when new diagnoses occur'
            }
        ])
        
        return recommendations
    
    def create_simple_pedigree_from_assessment(self, patient_data, family_history):
        """
        Create a simplified pedigree from assessment data
        Useful when detailed family data is not available
        """
        family_members = []
        member_id = 1
        
        # Add patient (proband)
        family_members.append({
            'id': member_id,
            'name': patient_data.get('name', 'Patient'),
            'gender': patient_data.get('gender', 'unknown'),
            'age': patient_data.get('age', 0),
            'generation': 0,
            'affected': True,
            'disorders': patient_data.get('disorders', []),
            'relationship': 'proband'
        })
        proband_id = member_id
        member_id += 1
        
        # Add parents if family history exists
        if family_history.get('has_history', False):
            affected_relatives = family_history.get('affected_relatives', [])
            disorders = family_history.get('disorders', [])
            
            # Add parents
            if 'parent' in affected_relatives or 'mother' in affected_relatives:
                family_members.append({
                    'id': member_id,
                    'name': 'Mother',
                    'gender': 'female',
                    'age': patient_data.get('age', 30) + 30,
                    'generation': 1,
                    'affected': True,
                    'disorders': disorders,
                    'relationship': 'mother'
                })
                member_id += 1
            
            if 'parent' in affected_relatives or 'father' in affected_relatives:
                family_members.append({
                    'id': member_id,
                    'name': 'Father',
                    'gender': 'male',
                    'age': patient_data.get('age', 30) + 30,
                    'generation': 1,
                    'affected': True,
                    'disorders': disorders,
                    'relationship': 'father'
                })
                member_id += 1
            
            # Add siblings
            if 'sibling' in affected_relatives:
                family_members.append({
                    'id': member_id,
                    'name': 'Sibling',
                    'gender': 'unknown',
                    'age': patient_data.get('age', 30),
                    'generation': 0,
                    'affected': True,
                    'disorders': disorders,
                    'relationship': 'sibling'
                })
                member_id += 1
            
            # Add grandparents
            if 'grandparent' in affected_relatives:
                family_members.append({
                    'id': member_id,
                    'name': 'Grandparent',
                    'gender': 'unknown',
                    'age': patient_data.get('age', 30) + 60,
                    'generation': 2,
                    'affected': True,
                    'disorders': disorders,
                    'relationship': 'grandparent'
                })
        
        return self.build_pedigree(family_members, proband_id)
