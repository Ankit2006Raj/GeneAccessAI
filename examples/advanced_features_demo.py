"""
Demo Script for Advanced Features
Demonstrates Risk Timeline and Family Pedigree AI capabilities
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.services.risk_timeline import RiskTimelineEngine
from src.services.family_pedigree import FamilyPedigreeAI
import json

def demo_risk_timeline():
    """Demonstrate Risk Timeline Engine"""
    print("=" * 80)
    print("DEMO 1: AI-Generated Personal Genetic Risk Timeline")
    print("=" * 80)
    
    # Initialize engine
    timeline_engine = RiskTimelineEngine()
    
    # Sample patient data
    patient_data = {
        'current_age': 35,
        'disorder': 'Huntington Disease',
        'current_risk_score': 65,
        'family_history': {
            'has_history': True,
            'affected_relatives': ['parent', 'grandparent'],
            'disorders': ['Huntington Disease']
        },
        'lifestyle_data': {
            'smoking': 'current',
            'exercise': 'none',
            'bmi': 28
        }
    }
    
    print("\n📊 Patient Profile:")
    print(f"  Age: {patient_data['current_age']}")
    print(f"  Disorder: {patient_data['disorder']}")
    print(f"  Current Risk Score: {patient_data['current_risk_score']}")
    print(f"  Family History: {patient_data['family_history']['affected_relatives']}")
    
    # Generate timeline
    print("\n🔄 Generating risk timeline...")
    timeline = timeline_engine.generate_risk_timeline(
        current_age=patient_data['current_age'],
        disorder=patient_data['disorder'],
        current_risk_score=patient_data['current_risk_score'],
        family_history=patient_data['family_history'],
        lifestyle_data=patient_data['lifestyle_data']
    )
    
    # Display projections
    print("\n📈 RISK PROJECTIONS:")
    print("-" * 80)
    
    for period in ['5_year', '10_year', '20_year']:
        proj = timeline['projections'][period]
        print(f"\n{period.replace('_', '-').upper()}:")
        print(f"  Age: {proj['projected_age']}")
        print(f"  Risk Score: {proj['projected_risk_score']}")
        print(f"  Risk Level: {proj['risk_level']}")
        print(f"  Manifestation Probability: {proj['manifestation_probability']}%")
        print(f"  Confidence Interval: {proj['confidence_interval']['lower']} - {proj['confidence_interval']['upper']}")
    
    # Display what-if scenarios
    print("\n💡 WHAT-IF SCENARIOS:")
    print("-" * 80)
    
    for scenario in timeline['what_if_scenarios']:
        print(f"\n{scenario['scenario']}:")
        print(f"  Impact: {scenario['impact_percentage']}%")
        print(f"  10-Year Risk: {scenario['projected_10yr_risk']}")
        print(f"  Risk Reduction: {scenario['risk_reduction']} points")
        if scenario['years_of_life_quality_gained'] > 0:
            print(f"  Quality Years Gained: {scenario['years_of_life_quality_gained']}")
    
    # Display lifestyle recommendations
    print("\n🏃 LIFESTYLE RECOMMENDATIONS:")
    print("-" * 80)
    
    for rec in timeline['lifestyle_recommendations'][:3]:  # Show top 3
        print(f"\n{rec['category']} ({rec['priority']} Priority):")
        print(f"  Action: {rec['action']}")
        print(f"  Impact: {rec['impact']}")
        print(f"  Expected Benefit: {rec['expected_benefit']} points")
    
    # Display milestones
    if timeline['milestones']:
        print("\n🚩 CRITICAL MILESTONES:")
        print("-" * 80)
        for milestone in timeline['milestones']:
            print(f"\n  Age {milestone['age']} ({milestone['years_from_now']} years from now):")
            print(f"    {milestone['description']}")
    
    print("\n✅ Risk Timeline Demo Complete!\n")
    return timeline


def demo_family_pedigree():
    """Demonstrate Family Pedigree AI"""
    print("=" * 80)
    print("DEMO 2: Family Pedigree AI - Automatic Pedigree Chart Builder")
    print("=" * 80)
    
    # Initialize AI
    pedigree_ai = FamilyPedigreeAI()
    
    # Sample family data (3 generations)
    family_data = [
        # Generation 0 (Proband and siblings)
        {
            'id': 1,
            'name': 'John Doe (Proband)',
            'gender': 'male',
            'age': 35,
            'generation': 0,
            'affected': True,
            'disorders': ['Huntington Disease'],
            'carrier_status': 'affected',
            'parents': [2, 3],
            'siblings': [4],
            'children': [],
            'relationship': 'proband'
        },
        {
            'id': 4,
            'name': 'Jane Doe (Sister)',
            'gender': 'female',
            'age': 32,
            'generation': 0,
            'affected': False,
            'disorders': [],
            'carrier_status': 'unknown',
            'parents': [2, 3],
            'siblings': [1],
            'children': [],
            'relationship': 'sibling'
        },
        # Generation 1 (Parents)
        {
            'id': 2,
            'name': 'Mary Doe (Mother)',
            'gender': 'female',
            'age': 60,
            'generation': 1,
            'affected': True,
            'disorders': ['Huntington Disease'],
            'carrier_status': 'affected',
            'parents': [5, 6],
            'siblings': [],
            'children': [1, 4],
            'relationship': 'mother'
        },
        {
            'id': 3,
            'name': 'Robert Doe (Father)',
            'gender': 'male',
            'age': 62,
            'generation': 1,
            'affected': False,
            'disorders': [],
            'carrier_status': 'unaffected',
            'parents': [],
            'siblings': [],
            'children': [1, 4],
            'relationship': 'father'
        },
        # Generation 2 (Grandparents)
        {
            'id': 5,
            'name': 'Grandmother (Maternal)',
            'gender': 'female',
            'age': 85,
            'generation': 2,
            'affected': True,
            'disorders': ['Huntington Disease'],
            'carrier_status': 'affected',
            'deceased': False,
            'parents': [],
            'siblings': [],
            'children': [2],
            'relationship': 'grandparent'
        },
        {
            'id': 6,
            'name': 'Grandfather (Maternal)',
            'gender': 'male',
            'age': 87,
            'generation': 2,
            'affected': False,
            'disorders': [],
            'carrier_status': 'unaffected',
            'deceased': False,
            'parents': [],
            'siblings': [],
            'children': [2],
            'relationship': 'grandparent'
        }
    ]
    
    print("\n👨‍👩‍👧‍👦 Family Structure:")
    print(f"  Total Members: {len(family_data)}")
    print(f"  Generations: 3")
    print(f"  Affected Members: {sum(1 for m in family_data if m['affected'])}")
    
    # Build pedigree
    print("\n🔄 Building pedigree and analyzing inheritance patterns...")
    pedigree = pedigree_ai.build_pedigree(family_data, proband_id=1)
    
    # Display inheritance analysis
    print("\n🧬 INHERITANCE PATTERN ANALYSIS:")
    print("-" * 80)
    
    inheritance = pedigree['inheritance_analysis']
    if inheritance['primary_pattern']:
        pattern = inheritance['primary_pattern']
        print(f"\nPrimary Pattern: {pattern['pattern'].replace('_', ' ').title()}")
        print(f"Confidence: {pattern['confidence'] * 100:.0f}%")
        print(f"Evidence: {pattern['evidence']}")
    
    if len(inheritance['detected_patterns']) > 1:
        print("\nOther Possible Patterns:")
        for pattern in inheritance['detected_patterns']:
            if pattern != inheritance['primary_pattern']:
                print(f"  - {pattern['pattern'].replace('_', ' ').title()} ({pattern['confidence'] * 100:.0f}%)")
    
    # Display risk analysis
    print("\n⚠️ FAMILY RISK ANALYSIS:")
    print("-" * 80)
    
    risk_analysis = pedigree['risk_analysis']
    for member_id, risk in risk_analysis.items():
        member = next(m for m in family_data if m['id'] == member_id)
        print(f"\n{member['name']}:")
        print(f"  Risk Level: {risk['risk_level'].replace('_', ' ').title()}")
        print(f"  Risk Score: {risk['risk_score']}")
        if risk['carrier_probability'] > 0:
            print(f"  Carrier Probability: {risk['carrier_probability']}%")
    
    # Display high-risk lines
    if pedigree['high_risk_lines']:
        print("\n🚨 HIGH-RISK HEREDITARY LINES:")
        print("-" * 80)
        for line in pedigree['high_risk_lines']:
            print(f"\nGeneration {line['generation']}:")
            print(f"  Affected Members: {line['affected_count']}")
            print(f"  High-Risk Members: {line['high_risk_count']}")
            print(f"  Severity: {line['severity'].upper()}")
    
    # Display carrier analysis
    if pedigree['carrier_analysis']:
        print("\n🧪 CARRIER PROBABILITY ANALYSIS:")
        print("-" * 80)
        for member_id, analysis in pedigree['carrier_analysis'].items():
            member = next(m for m in family_data if m['id'] == member_id)
            print(f"\n{member['name']}:")
            print(f"  Carrier Probability: {analysis['carrier_probability']}%")
            print(f"  Status: {analysis['status'].replace('_', ' ').title()}")
    
    # Display recommendations
    print("\n📋 GENETIC COUNSELING RECOMMENDATIONS:")
    print("-" * 80)
    
    for rec in pedigree['recommendations']:
        print(f"\n{rec['category']} ({rec['priority']} Priority):")
        print(f"  Recommendation: {rec['recommendation']}")
        print(f"  Action: {rec['action']}")
    
    # Display visualization data summary
    viz_data = pedigree['visualization_data']
    print("\n📊 PEDIGREE VISUALIZATION DATA:")
    print("-" * 80)
    print(f"  Nodes (Family Members): {len(viz_data['nodes'])}")
    print(f"  Edges (Relationships): {len(viz_data['edges'])}")
    print(f"  Risk Color Legend: {len(viz_data['legend'])} levels")
    
    print("\n✅ Family Pedigree Demo Complete!\n")
    return pedigree


def demo_simple_pedigree():
    """Demonstrate simple pedigree creation from assessment data"""
    print("=" * 80)
    print("DEMO 3: Simple Pedigree from Assessment Data")
    print("=" * 80)
    
    pedigree_ai = FamilyPedigreeAI()
    
    # Sample assessment data
    patient_data = {
        'name': 'Sarah Johnson',
        'age': 28,
        'gender': 'female',
        'disorders': ['Cystic Fibrosis']
    }
    
    family_history = {
        'has_history': True,
        'affected_relatives': ['sibling', 'parent'],
        'disorders': ['Cystic Fibrosis']
    }
    
    print("\n👤 Patient Data:")
    print(f"  Name: {patient_data['name']}")
    print(f"  Age: {patient_data['age']}")
    print(f"  Gender: {patient_data['gender']}")
    print(f"  Disorder: {patient_data['disorders'][0]}")
    
    print("\n👨‍👩‍👧 Family History:")
    print(f"  Has History: {family_history['has_history']}")
    print(f"  Affected Relatives: {', '.join(family_history['affected_relatives'])}")
    
    # Create simple pedigree
    print("\n🔄 Creating simplified pedigree...")
    pedigree = pedigree_ai.create_simple_pedigree_from_assessment(
        patient_data, family_history
    )
    
    # Display results
    print("\n✅ Pedigree Created!")
    print(f"  Family Members: {len(pedigree['pedigree_tree']['members'])}")
    print(f"  Generations: {len(pedigree['pedigree_tree']['generations'])}")
    
    if pedigree['inheritance_analysis']['primary_pattern']:
        pattern = pedigree['inheritance_analysis']['primary_pattern']
        print(f"\n  Detected Pattern: {pattern['pattern'].replace('_', ' ').title()}")
        print(f"  Confidence: {pattern['confidence'] * 100:.0f}%")
    
    print("\n✅ Simple Pedigree Demo Complete!\n")
    return pedigree


def demo_combined_analysis():
    """Demonstrate combined risk timeline and pedigree analysis"""
    print("=" * 80)
    print("DEMO 4: Combined Risk Timeline + Pedigree Analysis")
    print("=" * 80)
    
    # Run both analyses
    print("\n🔄 Running combined analysis...\n")
    
    timeline = demo_risk_timeline()
    pedigree = demo_family_pedigree()
    
    # Generate combined insights
    print("\n" + "=" * 80)
    print("COMBINED INSIGHTS")
    print("=" * 80)
    
    print("\n📊 Summary:")
    print(f"  Current Risk: {timeline['current_risk_score']}")
    print(f"  5-Year Projection: {timeline['projections']['5_year']['projected_risk_score']}")
    print(f"  10-Year Projection: {timeline['projections']['10_year']['projected_risk_score']}")
    print(f"  20-Year Projection: {timeline['projections']['20_year']['projected_risk_score']}")
    
    if pedigree['inheritance_analysis']['primary_pattern']:
        pattern = pedigree['inheritance_analysis']['primary_pattern']
        print(f"\n  Inheritance Pattern: {pattern['pattern'].replace('_', ' ').title()}")
        print(f"  Pattern Confidence: {pattern['confidence'] * 100:.0f}%")
    
    print(f"\n  High-Risk Family Lines: {len(pedigree['high_risk_lines'])}")
    print(f"  Critical Milestones: {len(timeline['milestones'])}")
    
    # Best what-if scenario
    best_scenario = min(timeline['what_if_scenarios'], 
                       key=lambda x: x['projected_10yr_risk'])
    print(f"\n💡 Best Intervention Strategy:")
    print(f"  Scenario: {best_scenario['scenario']}")
    print(f"  Risk Reduction: {best_scenario['risk_reduction']} points")
    print(f"  Quality Years Gained: {best_scenario['years_of_life_quality_gained']}")
    
    print("\n✅ Combined Analysis Complete!\n")


def main():
    """Run all demos"""
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 15 + "ADVANCED FEATURES DEMONSTRATION" + " " * 32 + "║")
    print("║" + " " * 20 + "GeneAccessAI Platform" + " " * 37 + "║")
    print("╚" + "=" * 78 + "╝")
    print("\n")
    
    try:
        # Demo 1: Risk Timeline
        demo_risk_timeline()
        input("\nPress Enter to continue to next demo...")
        
        # Demo 2: Family Pedigree
        demo_family_pedigree()
        input("\nPress Enter to continue to next demo...")
        
        # Demo 3: Simple Pedigree
        demo_simple_pedigree()
        input("\nPress Enter to continue to final demo...")
        
        # Demo 4: Combined Analysis
        demo_combined_analysis()
        
        print("\n" + "=" * 80)
        print("ALL DEMOS COMPLETED SUCCESSFULLY! 🎉")
        print("=" * 80)
        print("\nNext Steps:")
        print("  1. Start the Flask app: python app.py")
        print("  2. Navigate to: http://localhost:5000/risk-timeline")
        print("  3. Navigate to: http://localhost:5000/family-pedigree")
        print("  4. Or use the API endpoints directly")
        print("\nDocumentation:")
        print("  - ADVANCED_FEATURES.md - Complete feature documentation")
        print("  - INTEGRATION_GUIDE.md - Integration instructions")
        print("\n")
        
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user.")
    except Exception as e:
        print(f"\n\nError during demo: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
