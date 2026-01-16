"""
Disease Encyclopedia - AI-based Knowledge Assistant
Provides detailed information about genetic disorders
"""

class DiseaseEncyclopedia:
    def __init__(self):
        self.disease_database = {
            'thalassemia': {
                'name': 'Thalassemia',
                'category': 'Blood Disorder',
                'description': 'Thalassemia is an inherited blood disorder that causes your body to have less hemoglobin than normal. Hemoglobin enables red blood cells to carry oxygen.',
                'causes': [
                    'Inherited mutations in genes that make hemoglobin',
                    'Autosomal recessive inheritance pattern',
                    'Mutations in HBB gene (beta-thalassemia) or HBA genes (alpha-thalassemia)'
                ],
                'symptoms': [
                    'Fatigue and weakness',
                    'Pale or yellowish skin',
                    'Facial bone deformities',
                    'Slow growth',
                    'Abdominal swelling',
                    'Dark urine'
                ],
                'types': [
                    'Alpha-thalassemia (mild to severe)',
                    'Beta-thalassemia (minor, intermedia, major)',
                    'Thalassemia minor (carrier)',
                    'Thalassemia major (Cooley\'s anemia)'
                ],
                'diagnosis': [
                    'Complete blood count (CBC)',
                    'Hemoglobin electrophoresis',
                    'Genetic testing',
                    'Prenatal testing available'
                ],
                'treatment': [
                    'Regular blood transfusions',
                    'Iron chelation therapy',
                    'Folic acid supplements',
                    'Bone marrow transplant (curative)',
                    'Gene therapy (emerging)'
                ],
                'prevalence': 'Common in Mediterranean, Middle Eastern, Asian, and African populations',
                'inheritance': 'Autosomal recessive'
            },
            'brca mutation': {
                'name': 'BRCA Gene Mutation',
                'category': 'Cancer Predisposition',
                'description': 'BRCA1 and BRCA2 are genes that produce proteins to help repair damaged DNA. Mutations in these genes significantly increase the risk of breast and ovarian cancers.',
                'causes': [
                    'Inherited mutations in BRCA1 or BRCA2 genes',
                    'Autosomal dominant inheritance',
                    'Can be inherited from either parent'
                ],
                'symptoms': [
                    'No symptoms until cancer develops',
                    'Family history of breast cancer',
                    'Family history of ovarian cancer',
                    'Early-onset breast cancer in family',
                    'Male breast cancer in family'
                ],
                'risks': [
                    'Breast cancer risk: 45-70% by age 70',
                    'Ovarian cancer risk: 11-40% by age 70',
                    'Increased risk of pancreatic cancer',
                    'Increased risk of prostate cancer (men)',
                    'Earlier age of cancer onset'
                ],
                'diagnosis': [
                    'Genetic testing (blood or saliva)',
                    'Family history assessment',
                    'Genetic counseling recommended',
                    'Multi-gene panel testing available'
                ],
                'management': [
                    'Enhanced screening (mammograms, MRI)',
                    'Prophylactic mastectomy (preventive surgery)',
                    'Prophylactic oophorectomy (ovary removal)',
                    'Chemoprevention medications',
                    'Regular monitoring and checkups'
                ],
                'prevalence': '1 in 400-800 people in general population; higher in Ashkenazi Jewish population',
                'inheritance': 'Autosomal dominant (50% chance of passing to children)',
                'special_considerations': 'Affects both men and women; genetic counseling strongly recommended'
            },
            'cystic fibrosis': {
                'name': 'Cystic Fibrosis',
                'category': 'Respiratory/Digestive Disorder',
                'description': 'Cystic fibrosis is a genetic disorder that affects the lungs and digestive system. It causes thick, sticky mucus to build up in organs.',
                'causes': [
                    'Mutations in CFTR gene',
                    'Autosomal recessive inheritance',
                    'Over 2,000 known mutations'
                ],
                'symptoms': [
                    'Persistent cough with thick mucus',
                    'Wheezing and shortness of breath',
                    'Frequent lung infections',
                    'Poor growth and weight gain',
                    'Salty-tasting skin',
                    'Digestive problems'
                ],
                'diagnosis': [
                    'Newborn screening',
                    'Sweat chloride test',
                    'Genetic testing',
                    'Pulmonary function tests'
                ],
                'treatment': [
                    'Airway clearance techniques',
                    'Inhaled medications',
                    'CFTR modulator drugs',
                    'Antibiotics for infections',
                    'Pancreatic enzyme supplements',
                    'Nutritional support'
                ],
                'prevalence': '1 in 3,000 births in Caucasian populations',
                'inheritance': 'Autosomal recessive'
            },
            'down syndrome': {
                'name': 'Down Syndrome',
                'category': 'Chromosomal Disorder',
                'description': 'Down syndrome is a genetic condition caused by an extra copy of chromosome 21, leading to developmental and intellectual delays.',
                'causes': [
                    'Trisomy 21 (extra chromosome 21)',
                    'Usually not inherited',
                    'Risk increases with maternal age'
                ],
                'symptoms': [
                    'Intellectual disability',
                    'Distinctive facial features',
                    'Low muscle tone',
                    'Short stature',
                    'Heart defects (50% of cases)',
                    'Developmental delays'
                ],
                'diagnosis': [
                    'Prenatal screening tests',
                    'Diagnostic tests (amniocentesis, CVS)',
                    'Postnatal physical examination',
                    'Chromosomal analysis (karyotype)'
                ],
                'treatment': [
                    'Early intervention programs',
                    'Physical therapy',
                    'Speech therapy',
                    'Occupational therapy',
                    'Treatment of associated conditions',
                    'Educational support'
                ],
                'prevalence': '1 in 700 births',
                'inheritance': 'Usually sporadic (not inherited)'
            },
            'sickle cell anemia': {
                'name': 'Sickle Cell Anemia',
                'category': 'Blood Disorder',
                'description': 'Sickle cell anemia is an inherited blood disorder where red blood cells become rigid and sickle-shaped, blocking blood flow.',
                'causes': [
                    'Mutation in HBB gene',
                    'Autosomal recessive inheritance',
                    'Requires two copies of mutated gene'
                ],
                'symptoms': [
                    'Anemia and fatigue',
                    'Pain crises',
                    'Swelling of hands and feet',
                    'Frequent infections',
                    'Delayed growth',
                    'Vision problems'
                ],
                'diagnosis': [
                    'Newborn screening',
                    'Hemoglobin electrophoresis',
                    'Blood tests',
                    'Genetic testing'
                ],
                'treatment': [
                    'Hydroxyurea medication',
                    'Pain management',
                    'Blood transfusions',
                    'Bone marrow transplant',
                    'Gene therapy (emerging)',
                    'Preventive antibiotics'
                ],
                'prevalence': 'Common in African, Mediterranean, Middle Eastern, and Indian populations',
                'inheritance': 'Autosomal recessive'
            },
            'huntington disease': {
                'name': 'Huntington Disease',
                'category': 'Neurodegenerative Disorder',
                'description': 'Huntington disease is a progressive brain disorder causing uncontrolled movements, emotional problems, and cognitive decline.',
                'causes': [
                    'Mutation in HTT gene',
                    'CAG repeat expansion',
                    'Autosomal dominant inheritance'
                ],
                'symptoms': [
                    'Involuntary movements (chorea)',
                    'Difficulty walking',
                    'Cognitive decline',
                    'Psychiatric problems',
                    'Difficulty swallowing',
                    'Speech problems'
                ],
                'diagnosis': [
                    'Genetic testing',
                    'Neurological examination',
                    'Brain imaging (MRI, CT)',
                    'Psychiatric evaluation'
                ],
                'treatment': [
                    'Medications for movement disorders',
                    'Psychiatric medications',
                    'Physical therapy',
                    'Speech therapy',
                    'Occupational therapy',
                    'Supportive care'
                ],
                'prevalence': '3-7 per 100,000 people',
                'inheritance': 'Autosomal dominant (50% chance if parent affected)'
            },
            'hemophilia': {
                'name': 'Hemophilia',
                'category': 'Bleeding Disorder',
                'description': 'Hemophilia is a genetic disorder where blood doesn\'t clot properly due to lack of clotting factors.',
                'causes': [
                    'Mutations in F8 gene (Hemophilia A) or F9 gene (Hemophilia B)',
                    'X-linked recessive inheritance',
                    'Primarily affects males'
                ],
                'symptoms': [
                    'Excessive bleeding from injuries',
                    'Easy bruising',
                    'Spontaneous bleeding',
                    'Joint bleeding and pain',
                    'Blood in urine or stool',
                    'Prolonged bleeding after surgery'
                ],
                'diagnosis': [
                    'Blood clotting tests',
                    'Factor level tests',
                    'Genetic testing',
                    'Family history assessment'
                ],
                'treatment': [
                    'Clotting factor replacement therapy',
                    'Preventive (prophylactic) treatment',
                    'Gene therapy (emerging)',
                    'Desmopressin for mild cases',
                    'Avoid blood-thinning medications'
                ],
                'prevalence': 'Hemophilia A: 1 in 5,000 male births; Hemophilia B: 1 in 30,000 male births',
                'inheritance': 'X-linked recessive'
            },
            'muscular dystrophy': {
                'name': 'Muscular Dystrophy',
                'category': 'Neuromuscular Disorder',
                'description': 'Muscular dystrophy is a group of genetic diseases causing progressive muscle weakness and degeneration.',
                'causes': [
                    'Various genetic mutations',
                    'Most common: DMD gene mutation (Duchenne)',
                    'Different inheritance patterns depending on type'
                ],
                'symptoms': [
                    'Progressive muscle weakness',
                    'Difficulty walking',
                    'Frequent falls',
                    'Muscle pain and stiffness',
                    'Enlarged calf muscles',
                    'Learning disabilities (some types)'
                ],
                'types': [
                    'Duchenne muscular dystrophy (most common)',
                    'Becker muscular dystrophy',
                    'Myotonic dystrophy',
                    'Facioscapulohumeral dystrophy',
                    'Limb-girdle muscular dystrophy'
                ],
                'diagnosis': [
                    'Genetic testing',
                    'Muscle biopsy',
                    'Electromyography (EMG)',
                    'Blood tests (CK levels)',
                    'MRI'
                ],
                'treatment': [
                    'Physical therapy',
                    'Corticosteroids',
                    'Assistive devices',
                    'Respiratory support',
                    'Cardiac care',
                    'Gene therapy (research stage)'
                ],
                'prevalence': 'Duchenne: 1 in 3,500-5,000 male births',
                'inheritance': 'Varies by type; Duchenne is X-linked recessive'
            }
        }
        
        # Keywords for matching queries
        self.keywords = {
            'thalassemia': ['thalassemia', 'thalassaemia', 'cooley', 'hemoglobin disorder'],
            'brca mutation': ['brca', 'breast cancer gene', 'ovarian cancer gene', 'brca1', 'brca2'],
            'cystic fibrosis': ['cystic fibrosis', 'cf', 'cftr'],
            'down syndrome': ['down syndrome', 'down\'s syndrome', 'trisomy 21', 'chromosome 21'],
            'sickle cell anemia': ['sickle cell', 'sickle cell anemia', 'sickle cell disease'],
            'huntington disease': ['huntington', 'huntington\'s', 'chorea'],
            'hemophilia': ['hemophilia', 'haemophilia', 'bleeding disorder'],
            'muscular dystrophy': ['muscular dystrophy', 'duchenne', 'becker', 'dmd']
        }
    
    def search_disease(self, query):
        """Search for disease information based on query"""
        query = query.lower().strip()
        
        # Direct match
        if query in self.disease_database:
            return self.disease_database[query]
        
        # Keyword matching
        for disease_key, keywords in self.keywords.items():
            for keyword in keywords:
                if keyword in query or query in keyword:
                    return self.disease_database.get(disease_key)
        
        return None
    
    def get_disease_info(self, disease_name):
        """Get comprehensive information about a disease"""
        disease = self.search_disease(disease_name)
        if disease:
            return disease
        return {'error': 'Disease not found in database'}
    
    def answer_question(self, question):
        """Answer natural language questions about diseases"""
        question = question.lower().strip()
        
        # Extract disease name from question
        disease = None
        for disease_key in self.disease_database.keys():
            if disease_key in question:
                disease = self.disease_database[disease_key]
                break
        
        if not disease:
            # Try keyword matching
            for disease_key, keywords in self.keywords.items():
                for keyword in keywords:
                    if keyword in question:
                        disease = self.disease_database[disease_key]
                        break
                if disease:
                    break
        
        if not disease:
            return "I couldn't find information about that disease. Please try asking about: Thalassemia, BRCA Mutation, Cystic Fibrosis, Down Syndrome, Sickle Cell Anemia, Huntington Disease, Hemophilia, or Muscular Dystrophy."
        
        # Answer based on question type
        if any(word in question for word in ['what is', 'what\'s', 'define', 'explain']):
            return f"{disease['name']}: {disease['description']}"
        
        elif any(word in question for word in ['cause', 'why', 'how does']):
            causes = '\n• '.join(disease['causes'])
            return f"Causes of {disease['name']}:\n• {causes}"
        
        elif any(word in question for word in ['symptom', 'sign', 'affect']):
            symptoms = '\n• '.join(disease['symptoms'])
            return f"Symptoms of {disease['name']}:\n• {symptoms}"
        
        elif any(word in question for word in ['treat', 'cure', 'therapy', 'medication']):
            treatment = '\n• '.join(disease['treatment'])
            return f"Treatment for {disease['name']}:\n• {treatment}"
        
        elif any(word in question for word in ['diagnose', 'test', 'detect']):
            diagnosis = '\n• '.join(disease['diagnosis'])
            return f"Diagnosis of {disease['name']}:\n• {diagnosis}"
        
        elif any(word in question for word in ['inherit', 'genetic', 'pass', 'family']):
            return f"{disease['name']} inheritance: {disease.get('inheritance', 'Information not available')}"
        
        elif any(word in question for word in ['common', 'rare', 'prevalence', 'frequent']):
            return f"{disease['name']} prevalence: {disease.get('prevalence', 'Information not available')}"
        
        else:
            # Return general information
            return f"{disease['name']}: {disease['description']}\n\nFor more specific information, ask about causes, symptoms, treatment, or diagnosis."
    
    def list_all_diseases(self):
        """List all diseases in the database"""
        return [
            {
                'key': key,
                'name': info['name'],
                'category': info['category']
            }
            for key, info in self.disease_database.items()
        ]
    
    def get_diseases_by_category(self, category):
        """Get diseases filtered by category"""
        return [
            {
                'key': key,
                'name': info['name'],
                'description': info['description']
            }
            for key, info in self.disease_database.items()
            if info['category'].lower() == category.lower()
        ]

# Initialize global instance
disease_encyclopedia = DiseaseEncyclopedia()

if __name__ == '__main__':
    # Test the encyclopedia
    encyclopedia = DiseaseEncyclopedia()
    
    test_questions = [
        "What is Thalassemia?",
        "How does BRCA mutation affect women?",
        "What are the symptoms of cystic fibrosis?",
        "How is Down syndrome diagnosed?"
    ]
    
    for question in test_questions:
        print(f"\nQ: {question}")
        print(f"A: {encyclopedia.answer_question(question)}")
