"""
Early-Stage Genetic Counseling System
Provides preventive care tips, lifestyle suggestions, and recommendations
"""

class GeneticCounselor:
    def __init__(self):
        self.counseling_database = {
            'Down Syndrome': {
                'preventive_care': [
                    'Regular health checkups every 6 months',
                    'Annual thyroid function tests',
                    'Regular hearing and vision screenings',
                    'Cardiac evaluations (echocardiogram)',
                    'Monitor for sleep apnea',
                    'Dental checkups every 6 months'
                ],
                'lifestyle_suggestions': [
                    'Engage in regular physical activity adapted to abilities',
                    'Maintain a balanced, nutritious diet',
                    'Participate in social activities and community programs',
                    'Continue educational and vocational training',
                    'Establish consistent daily routines',
                    'Encourage independence in daily activities'
                ],
                'specialist_recommendations': [
                    'Pediatric cardiologist (for heart conditions)',
                    'Endocrinologist (for thyroid issues)',
                    'Developmental pediatrician',
                    'Speech therapist',
                    'Physical therapist',
                    'Occupational therapist'
                ],
                'red_flags': [
                    'Sudden changes in behavior or personality',
                    'Difficulty breathing or chest pain',
                    'Unexplained weight loss or gain',
                    'Persistent fatigue beyond normal',
                    'New onset seizures',
                    'Regression in developmental milestones'
                ],
                'family_planning': [
                    'Genetic counseling before pregnancy',
                    'Prenatal screening options available',
                    'Discuss recurrence risk with geneticist',
                    'Consider advanced maternal age factors'
                ]
            },
            'Cystic Fibrosis': {
                'preventive_care': [
                    'Daily airway clearance therapy',
                    'Regular pulmonary function tests',
                    'Quarterly clinic visits',
                    'Annual comprehensive evaluations',
                    'Preventive antibiotics as prescribed',
                    'Vaccinations (flu, pneumonia) up to date'
                ],
                'lifestyle_suggestions': [
                    'High-calorie, high-protein diet',
                    'Take pancreatic enzyme supplements with meals',
                    'Stay well-hydrated',
                    'Regular exercise to improve lung function',
                    'Avoid smoke and air pollutants',
                    'Practice good hand hygiene to prevent infections'
                ],
                'specialist_recommendations': [
                    'Pulmonologist (lung specialist)',
                    'Gastroenterologist (digestive system)',
                    'Nutritionist/Dietitian',
                    'Respiratory therapist',
                    'CF care team at accredited center',
                    'Endocrinologist (if diabetes develops)'
                ],
                'red_flags': [
                    'Increased coughing or change in mucus color',
                    'Fever above 100.4°F (38°C)',
                    'Difficulty breathing or chest pain',
                    'Significant weight loss',
                    'Coughing up blood',
                    'Decreased exercise tolerance'
                ],
                'family_planning': [
                    'Carrier screening for partners',
                    'Genetic counseling recommended',
                    'Preimplantation genetic diagnosis available',
                    'Fertility considerations (males often infertile)'
                ]
            },
            'Sickle Cell Anemia': {
                'preventive_care': [
                    'Take daily penicillin (children) or as prescribed',
                    'Stay up to date with vaccinations',
                    'Regular blood tests and checkups',
                    'Annual eye exams',
                    'Annual kidney function tests',
                    'Transcranial Doppler ultrasound (children)'
                ],
                'lifestyle_suggestions': [
                    'Drink 8-10 glasses of water daily',
                    'Avoid extreme temperatures',
                    'Avoid high altitudes and unpressurized flights',
                    'Get adequate rest and sleep',
                    'Manage stress effectively',
                    'Avoid strenuous physical activity without preparation'
                ],
                'specialist_recommendations': [
                    'Hematologist (blood specialist)',
                    'Pain management specialist',
                    'Ophthalmologist (eye doctor)',
                    'Nephrologist (kidney specialist)',
                    'Cardiologist (heart specialist)',
                    'Genetic counselor'
                ],
                'red_flags': [
                    'Severe pain crisis lasting >2 hours',
                    'Fever above 101°F (38.3°C)',
                    'Difficulty breathing or chest pain',
                    'Severe headache or dizziness',
                    'Sudden vision changes',
                    'Abdominal swelling or severe pain',
                    'Priapism (prolonged painful erection)',
                    'Stroke symptoms (weakness, slurred speech)'
                ],
                'family_planning': [
                    'Carrier testing for partners',
                    'Genetic counseling before pregnancy',
                    'Prenatal diagnosis available',
                    'Newborn screening in most countries'
                ]
            },
            'Huntington Disease': {
                'preventive_care': [
                    'Regular neurological examinations',
                    'Psychiatric evaluations',
                    'Cognitive assessments',
                    'Speech and swallowing evaluations',
                    'Physical therapy assessments',
                    'Nutritional monitoring'
                ],
                'lifestyle_suggestions': [
                    'Maintain physical activity as long as possible',
                    'Engage in cognitive stimulation activities',
                    'Establish support network early',
                    'Plan for future care needs',
                    'Maintain social connections',
                    'Consider occupational therapy for daily tasks'
                ],
                'specialist_recommendations': [
                    'Neurologist specializing in movement disorders',
                    'Psychiatrist',
                    'Genetic counselor',
                    'Speech therapist',
                    'Physical therapist',
                    'Occupational therapist',
                    'Social worker'
                ],
                'red_flags': [
                    'Rapid progression of symptoms',
                    'Severe depression or suicidal thoughts',
                    'Difficulty swallowing (choking risk)',
                    'Significant weight loss',
                    'Falls or injuries from movement problems',
                    'Severe behavioral changes'
                ],
                'family_planning': [
                    'Genetic testing and counseling crucial',
                    'Predictive testing available for at-risk individuals',
                    'Preimplantation genetic diagnosis available',
                    '50% chance of inheritance from affected parent',
                    'Psychological support recommended before testing'
                ]
            },
            'Hemophilia': {
                'preventive_care': [
                    'Prophylactic factor replacement therapy',
                    'Regular joint examinations',
                    'Dental care with hemophilia precautions',
                    'Annual comprehensive care visits',
                    'Hepatitis A and B vaccinations',
                    'Monitor for inhibitor development'
                ],
                'lifestyle_suggestions': [
                    'Engage in low-impact exercises (swimming, walking)',
                    'Avoid contact sports and high-risk activities',
                    'Wear protective gear during activities',
                    'Maintain healthy weight to reduce joint stress',
                    'Avoid medications that affect clotting (aspirin, NSAIDs)',
                    'Carry medical alert identification'
                ],
                'specialist_recommendations': [
                    'Hematologist at hemophilia treatment center',
                    'Orthopedic surgeon (for joint issues)',
                    'Physical therapist',
                    'Dentist experienced with bleeding disorders',
                    'Genetic counselor',
                    'Pain management specialist'
                ],
                'red_flags': [
                    'Bleeding that doesn\'t stop with treatment',
                    'Severe headache or head injury',
                    'Joint swelling, warmth, or severe pain',
                    'Blood in urine or stool',
                    'Prolonged nosebleeds',
                    'Abdominal pain or vomiting',
                    'Any significant trauma or injury'
                ],
                'family_planning': [
                    'Carrier testing for female relatives',
                    'Genetic counseling recommended',
                    'Prenatal diagnosis available',
                    'X-linked inheritance pattern',
                    'Female carriers may have mild symptoms'
                ]
            },
            'Thalassemia': {
                'preventive_care': [
                    'Regular blood transfusions (if major)',
                    'Iron chelation therapy',
                    'Monitor iron levels regularly',
                    'Cardiac monitoring (MRI, echocardiogram)',
                    'Liver function tests',
                    'Endocrine evaluations',
                    'Bone density scans'
                ],
                'lifestyle_suggestions': [
                    'Avoid iron supplements unless prescribed',
                    'Maintain balanced diet rich in calcium and vitamin D',
                    'Regular exercise to maintain bone health',
                    'Avoid alcohol to protect liver',
                    'Take folic acid supplements',
                    'Protect against infections'
                ],
                'specialist_recommendations': [
                    'Hematologist',
                    'Cardiologist',
                    'Endocrinologist',
                    'Hepatologist (liver specialist)',
                    'Genetic counselor',
                    'Bone marrow transplant specialist (if applicable)'
                ],
                'red_flags': [
                    'Severe fatigue or weakness',
                    'Chest pain or irregular heartbeat',
                    'Abdominal pain or swelling',
                    'Jaundice (yellowing of skin/eyes)',
                    'Frequent infections',
                    'Bone pain or fractures',
                    'Growth delays in children'
                ],
                'family_planning': [
                    'Carrier screening for partners',
                    'Genetic counseling essential',
                    'Prenatal diagnosis available',
                    'Preimplantation genetic diagnosis option',
                    'Both parents must be carriers for affected child'
                ]
            },
            'BRCA Mutation': {
                'preventive_care': [
                    'Enhanced breast cancer screening (mammogram + MRI)',
                    'Clinical breast exams every 6-12 months',
                    'Consider risk-reducing medications',
                    'Ovarian cancer screening (CA-125, transvaginal ultrasound)',
                    'Regular skin checks',
                    'Prostate screening for men'
                ],
                'lifestyle_suggestions': [
                    'Maintain healthy weight',
                    'Regular exercise (150 minutes/week)',
                    'Limit alcohol consumption',
                    'Avoid smoking',
                    'Eat a balanced diet rich in fruits and vegetables',
                    'Manage stress effectively',
                    'Breastfeed if possible (reduces risk)'
                ],
                'specialist_recommendations': [
                    'Genetic counselor',
                    'Oncologist',
                    'Breast surgeon',
                    'Gynecologic oncologist',
                    'Plastic surgeon (if considering preventive surgery)',
                    'Mental health professional'
                ],
                'red_flags': [
                    'New breast lump or thickening',
                    'Changes in breast size or shape',
                    'Nipple discharge or inversion',
                    'Skin changes on breast',
                    'Persistent abdominal bloating',
                    'Pelvic pain',
                    'Difficulty eating or feeling full quickly',
                    'Urinary urgency or frequency'
                ],
                'family_planning': [
                    'Genetic testing for family members',
                    'Preimplantation genetic diagnosis available',
                    '50% chance of passing mutation to children',
                    'Consider timing of risk-reducing surgeries',
                    'Discuss with genetic counselor before pregnancy'
                ]
            },
            'Muscular Dystrophy': {
                'preventive_care': [
                    'Regular cardiac monitoring',
                    'Pulmonary function tests',
                    'Orthopedic evaluations',
                    'Physical therapy sessions',
                    'Occupational therapy',
                    'Nutritional assessments'
                ],
                'lifestyle_suggestions': [
                    'Maintain mobility with appropriate exercises',
                    'Use assistive devices as needed',
                    'Prevent contractures with stretching',
                    'Maintain healthy weight',
                    'Ensure adequate calcium and vitamin D',
                    'Adapt home for accessibility'
                ],
                'specialist_recommendations': [
                    'Neurologist',
                    'Cardiologist',
                    'Pulmonologist',
                    'Physical therapist',
                    'Occupational therapist',
                    'Orthopedic surgeon',
                    'Genetic counselor'
                ],
                'red_flags': [
                    'Rapid progression of weakness',
                    'Difficulty breathing or shortness of breath',
                    'Chest pain or irregular heartbeat',
                    'Difficulty swallowing',
                    'Severe scoliosis',
                    'Frequent falls or injuries',
                    'Respiratory infections'
                ],
                'family_planning': [
                    'Genetic counseling essential',
                    'Carrier testing for female relatives',
                    'Prenatal diagnosis available',
                    'Inheritance pattern varies by type',
                    'Duchenne: X-linked recessive'
                ]
            },
            'Low Risk': {
                'preventive_care': [
                    'Annual health checkups',
                    'Age-appropriate cancer screenings',
                    'Maintain vaccination schedule',
                    'Regular dental and vision exams',
                    'Monitor blood pressure and cholesterol',
                    'Keep family medical history updated'
                ],
                'lifestyle_suggestions': [
                    'Eat a balanced, nutritious diet',
                    'Exercise regularly (150 minutes/week)',
                    'Maintain healthy weight',
                    'Get adequate sleep (7-9 hours)',
                    'Manage stress effectively',
                    'Avoid smoking and limit alcohol',
                    'Stay socially connected'
                ],
                'specialist_recommendations': [
                    'Primary care physician for regular checkups',
                    'Genetic counselor if planning family',
                    'Specialists as needed for specific concerns'
                ],
                'red_flags': [
                    'Unexplained weight loss or gain',
                    'Persistent fatigue',
                    'New or changing symptoms',
                    'Family history of genetic conditions',
                    'Unusual bleeding or bruising'
                ],
                'family_planning': [
                    'Update family medical history',
                    'Consider genetic counseling if family history present',
                    'Preconception health optimization',
                    'Prenatal care when pregnant'
                ]
            }
        }
    
    def get_counseling(self, disorder, risk_level='moderate'):
        """Get comprehensive genetic counseling information"""
        if disorder not in self.counseling_database:
            disorder = 'Low Risk'
        
        counseling = self.counseling_database[disorder]
        
        # Customize based on risk level
        urgency = self.get_urgency_level(risk_level)
        
        return {
            'disorder': disorder,
            'risk_level': risk_level,
            'urgency': urgency,
            'preventive_care': counseling['preventive_care'],
            'lifestyle_suggestions': counseling['lifestyle_suggestions'],
            'specialist_recommendations': counseling['specialist_recommendations'],
            'red_flags': counseling['red_flags'],
            'family_planning': counseling.get('family_planning', []),
            'next_steps': self.get_next_steps(disorder, risk_level)
        }
    
    def get_urgency_level(self, risk_level):
        """Determine urgency of consultation"""
        risk_level = risk_level.lower()
        if risk_level == 'high':
            return 'Urgent - Schedule consultation within 1-2 weeks'
        elif risk_level == 'moderate':
            return 'Important - Schedule consultation within 1 month'
        else:
            return 'Routine - Schedule consultation at your convenience'
    
    def get_next_steps(self, disorder, risk_level):
        """Get personalized next steps"""
        steps = []
        
        if risk_level.lower() == 'high':
            steps.append('Schedule an appointment with a genetic counselor immediately')
            steps.append('Discuss genetic testing options with your healthcare provider')
            steps.append('Inform immediate family members about potential hereditary risk')
        elif risk_level.lower() == 'moderate':
            steps.append('Consult with a genetic counselor within the next month')
            steps.append('Consider genetic testing for confirmation')
            steps.append('Keep detailed records of symptoms and family history')
        else:
            steps.append('Maintain regular health checkups')
            steps.append('Update family medical history periodically')
            steps.append('Consult genetic counselor if planning a family')
        
        if disorder != 'Low Risk':
            steps.append(f'Research support groups for {disorder}')
            steps.append('Educate yourself about the condition using reliable sources')
            steps.append('Discuss findings with your primary care physician')
        
        return steps
    
    def generate_counseling_summary(self, disorder, risk_level, patient_age=None):
        """Generate a comprehensive counseling summary"""
        counseling = self.get_counseling(disorder, risk_level)
        
        summary = f"""
GENETIC COUNSELING SUMMARY
{'='*50}

Condition: {disorder}
Risk Level: {risk_level}
Urgency: {counseling['urgency']}

PREVENTIVE CARE RECOMMENDATIONS:
{self._format_list(counseling['preventive_care'])}

LIFESTYLE SUGGESTIONS:
{self._format_list(counseling['lifestyle_suggestions'])}

RECOMMENDED SPECIALISTS:
{self._format_list(counseling['specialist_recommendations'])}

WARNING SIGNS (Seek Immediate Medical Attention):
{self._format_list(counseling['red_flags'])}

FAMILY PLANNING CONSIDERATIONS:
{self._format_list(counseling['family_planning'])}

NEXT STEPS:
{self._format_list(counseling['next_steps'])}

IMPORTANT DISCLAIMER:
This information is for educational purposes only and does not replace
professional medical advice. Always consult with qualified healthcare
providers for diagnosis and treatment decisions.
"""
        return summary
    
    def _format_list(self, items):
        """Format list items for display"""
        if not items:
            return "  • None specified"
        return '\n'.join([f"  • {item}" for item in items])
    
    def get_emergency_guidelines(self, disorder):
        """Get emergency guidelines for specific disorder"""
        emergency_info = {
            'Sickle Cell Anemia': {
                'when_to_call_911': [
                    'Severe chest pain',
                    'Difficulty breathing',
                    'Severe headache or confusion',
                    'Sudden weakness or numbness',
                    'Seizures',
                    'Loss of consciousness'
                ],
                'when_to_call_doctor': [
                    'Fever above 101°F',
                    'Pain crisis lasting >2 hours',
                    'Severe abdominal pain',
                    'Priapism lasting >2 hours'
                ]
            },
            'Hemophilia': {
                'when_to_call_911': [
                    'Head injury of any kind',
                    'Severe bleeding that won\'t stop',
                    'Severe abdominal or chest pain',
                    'Difficulty breathing',
                    'Loss of consciousness'
                ],
                'when_to_call_doctor': [
                    'Joint swelling or pain',
                    'Prolonged nosebleed',
                    'Blood in urine or stool',
                    'Any significant injury'
                ]
            }
        }
        
        return emergency_info.get(disorder, {
            'when_to_call_911': ['Severe symptoms', 'Life-threatening situations'],
            'when_to_call_doctor': ['Concerning symptoms', 'New or worsening conditions']
        })

# Initialize global instance
genetic_counselor = GeneticCounselor()

if __name__ == '__main__':
    # Test the counselor
    counselor = GeneticCounselor()
    
    # Test counseling for different disorders
    test_cases = [
        ('Thalassemia', 'high'),
        ('BRCA Mutation', 'moderate'),
        ('Low Risk', 'low')
    ]
    
    for disorder, risk in test_cases:
        print(counselor.generate_counseling_summary(disorder, risk))
        print("\n" + "="*70 + "\n")
