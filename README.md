# 🧬 GeneAccessAI - AI-Powered Genetic Health Assessment Platform

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-success.svg)]()

> An advanced AI-powered platform for genetic health risk assessment, combining machine learning, NLP, and comprehensive genetic counseling to provide personalized health insights.
<img width="1340" height="619" alt="image" src="https://github.com/user-attachments/assets/80f7b179-8a1d-4509-9acc-4f2c320387ff" />
<img width="1330" height="635" alt="image" src="https://github.com/user-attachments/assets/f1f4f37b-88c2-47b3-905d-719a5c6d1676" />
<img width="1347" height="636" alt="image" src="https://github.com/user-attachments/assets/d6ac195b-de1b-42e0-b73f-01f732f08538" />

## 🌟 Overview

GeneAccessAI is a cutting-edge web application that leverages ensemble machine learning models, natural language processing, and a comprehensive disease encyclopedia to assess genetic disorder risks. The platform provides professional-grade genetic analysis tools without requiring DNA testing, making genetic health insights accessible to everyone.

## ✨ Key Features

### 🤖 Core AI Capabilities
- **Ensemble ML Models**: XGBoost, LightGBM, and Random Forest for accurate risk prediction
- **NLP Symptom Suggester**: Intelligent symptom recognition and categorization
- **Disease Encyclopedia**: Comprehensive database with 50+ genetic disorders
- **AI Genetic Counseling**: Personalized recommendations and preventive care guidance
- **Multi-language Support**: Accessible in multiple languages

### 🔬 Advanced Analysis Tools

#### 📈 Risk Timeline
- Visualize genetic risk progression over time
- Age-based risk projections
- Interactive timeline charts

#### 🌳 Family Pedigree Builder
- Create detailed family medical history charts
- Inheritance pattern analysis
- Multi-generational tracking

#### 🌍 Ethnicity Risk Adjuster
- Population-specific risk calculations
- 7 major ethnic groups supported
- Real CDC/WHO data integration
- 50+ genetic disorders database

#### 🧬 Genomic Profile Generator
- AI-powered gene analysis (12+ genes)
- Pathway mapping and interactions
- Pharmacogenomics insights
- No DNA testing required

#### 🧪 Clinical Test Recommender
- 30+ clinical test recommendations
- Cost estimates and insurance predictions
- Turnaround time estimates
- Lab-specific guidance

#### 💊 Adverse Drug Reaction Predictor
- Pharmacogenetic risk assessment
- Drug interaction warnings
- Personalized medication guidance

#### 🧠 Psychosocial Risk Modulator
- Environmental factor analysis
- Lifestyle impact assessment
- Stress and mental health considerations

#### 🔄 Inheritance Simulator
- Genetic inheritance probability calculator
- Autosomal and X-linked pattern simulation
- Family planning insights

### 📊 Assessment Methods

1. **Interactive Chat Assessment**: Conversational AI-guided evaluation
2. **Comprehensive Form Assessment**: Detailed questionnaire with advanced fields
3. **Real-time Symptom Suggestions**: NLP-powered symptom autocomplete

### 📄 Professional Reporting
- PDF report generation with detailed analysis
- Risk scores and confidence levels
- Personalized recommendations
- Genetic counseling summaries
- Downloadable and shareable reports

## 🚀 Technology Stack

### Backend
- **Framework**: Flask 3.0.0
- **Database**: SQLAlchemy with SQLite
- **ML Libraries**: 
  - XGBoost 2.0.3
  - LightGBM 4.1.0
  - scikit-learn 1.3.2
  - NumPy 1.24.3

### Frontend
- **HTML5/CSS3**: Modern responsive design
- **JavaScript**: Interactive UI components
- **Chart.js**: Data visualization
- **Tailwind CSS**: Utility-first styling

### AI/ML Components
- Ensemble learning models
- Natural Language Processing
- Feature engineering pipeline
- Risk prediction algorithms

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Virtual environment (recommended)

### Setup Instructions

1. **Clone the repository**
```bash
git clone https://github.com/Ankit2006Rajand/geneaccessai.git
cd geneaccessai
```

2. **Create virtual environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Initialize the database**
```bash
python
>>> from app import app, db
>>> with app.app_context():
...     db.create_all()
>>> exit()
```

5. **Run the application**
```bash
python app.py
```

6. **Access the application**
```
Open your browser and navigate to: http://localhost:5000
```

## 📁 Project Structure

```
geneaccessai/
├── app.py                          # Main Flask application
├── requirements.txt                # Python dependencies
├── instance/
│   └── geneaccess.db              # SQLite database
├── models/
│   └── ensemble_models.pkl        # Trained ML models
├── reports/                        # Generated PDF reports
├── src/
│   ├── api/                       # API routes
│   ├── models/                    # ML model implementations
│   ├── services/                  # Business logic services
│   └── utils/                     # Utility functions
├── static/
│   ├── css/                       # Stylesheets
│   ├── js/                        # JavaScript files
│   └── images/                    # Image assets
└── templates/                      # HTML templates
```

## 🎯 Usage

### Quick Start

1. **Home Page**: Navigate to the landing page
2. **Start Assessment**: Choose between Chat or Form mode
3. **Provide Information**: 
   - Personal details (name, age, gender)
   - Symptoms and medical history
   - Family genetic history
   - Lifestyle factors
4. **Get Results**: Receive AI-powered risk assessment
5. **Download Report**: Generate and download PDF report
6. **Explore Advanced Features**: Access professional analysis tools

### Advanced Features Access

Access advanced features through:
- Homepage feature cards
- Dashboard widget
- Navigation menu dropdown
- Floating Action Button (FAB) - available on all pages
- Assessment page banner
- Advanced Features overview page

## 🔬 ML Model Details

### Ensemble Architecture
- **Random Forest**: Robust baseline predictions
- **XGBoost**: Gradient boosting for complex patterns
- **LightGBM**: Fast and efficient tree-based learning

### Feature Engineering
- Symptom encoding and categorization
- Family history pattern recognition
- Age and demographic factors
- Lifestyle and environmental variables
- Ethnicity-based risk adjustments

### Model Performance
- Confidence scoring for predictions
- Risk level classification (Low/Moderate/High)
- Disorder-specific predictions
- Continuous model improvement

## 📊 API Endpoints

### Assessment APIs
- `POST /api/predict` - Chat-based assessment prediction
- `POST /api/predict-form` - Form-based assessment prediction
- `POST /api/chat` - Conversational AI interaction

### Feature APIs
- `POST /api/suggest-symptoms` - NLP symptom suggestions
- `POST /api/disease-info` - Disease encyclopedia lookup
- `POST /api/counseling/<disorder>` - Genetic counseling info
- `POST /api/change-language` - Multi-language support

### Advanced Feature APIs
- `POST /api/ethnicity-risk` - Ethnicity-based risk calculation
- `POST /api/genomic-profile` - Generate genomic profile
- `POST /api/clinical-tests` - Clinical test recommendations
- `POST /api/drug-reactions` - Drug reaction predictions

## 🛡️ Security & Privacy

- Secure session management
- Data encryption in transit
- No external data sharing
- Local database storage
- HIPAA-compliant design principles
- User data anonymization options

## 🌐 Browser Support

- Chrome (recommended)
- Firefox
- Safari
- Edge
- Mobile browsers (iOS/Android)

## 📈 Future Enhancements

- [ ] Integration with real genetic testing APIs
- [ ] Blockchain for secure health records
- [ ] Mobile app (iOS/Android)
- [ ] Telemedicine integration
- [ ] Real-time genetic research updates
- [ ] Community support forums
- [ ] Healthcare provider portal

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

**IMPORTANT**: This application is for educational and informational purposes only. It is NOT a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of qualified health providers with any questions regarding genetic conditions or medical concerns.

## 📞 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Contact the development team
- Check the documentation

## 🙏 Acknowledgments

- Medical genetics research community
- Open-source ML libraries
- Flask and Python communities
- Healthcare data providers (CDC, WHO)

## 👨‍💻 Author

**Ankit Raj**

- 🌐 GitHub: [@Ankit2006Rajand](https://github.com/Ankit2006Rajand)
- 💼 LinkedIn: [Ankit Raj](https://www.linkedin.com/in/ankit-raj-226a36309)
- 📧 Email: ankit9905163014@gmail.com

---

<div align="center">

### ⭐ Star this repository if you find it helpful!

**Made with ❤️ and 🧬 by Ankit Raj**

</div>
