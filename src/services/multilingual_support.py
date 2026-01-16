"""
Multi-Language Support System
Supports English, Hindi, Bengali, Telugu, and more
"""

class MultilingualTranslator:
    def __init__(self):
        self.translations = {
            'en': {
                'app_name': 'GeneAccessAI',
                'welcome': 'Welcome to GeneAccessAI',
                'tagline': 'AI-Powered Genetic Disorder Risk Prediction',
                'start_assessment': 'Start Assessment',
                'login': 'Login',
                'register': 'Register',
                'logout': 'Logout',
                'dashboard': 'Dashboard',
                'about': 'About',
                'username': 'Username',
                'email': 'Email',
                'password': 'Password',
                'submit': 'Submit',
                'cancel': 'Cancel',
                'symptoms': 'Symptoms',
                'family_history': 'Family History',
                'risk_score': 'Risk Score',
                'prediction': 'Prediction',
                'recommendations': 'Recommendations',
                'download_report': 'Download Report',
                'view_details': 'View Details',
                'assessment_history': 'Assessment History',
                'no_assessments': 'No assessments yet',
                'loading': 'Loading...',
                'error': 'Error',
                'success': 'Success',
                'chatbot_greeting': 'Hello! I\'m your AI genetic health assistant.',
                'enter_symptoms': 'Please describe your symptoms',
                'consult_doctor': 'Please consult a doctor for proper diagnosis',
                'low_risk': 'Low Risk',
                'moderate_risk': 'Moderate Risk',
                'high_risk': 'High Risk',
            },
            'hi': {  # Hindi
                'app_name': 'जीनएक्सेसएआई',
                'welcome': 'जीनएक्सेसएआई में आपका स्वागत है',
                'tagline': 'एआई-संचालित आनुवंशिक विकार जोखिम भविष्यवाणी',
                'start_assessment': 'मूल्यांकन शुरू करें',
                'login': 'लॉगिन',
                'register': 'पंजीकरण करें',
                'logout': 'लॉगआउट',
                'dashboard': 'डैशबोर्ड',
                'about': 'के बारे में',
                'username': 'उपयोगकर्ता नाम',
                'email': 'ईमेल',
                'password': 'पासवर्ड',
                'submit': 'जमा करें',
                'cancel': 'रद्द करें',
                'symptoms': 'लक्षण',
                'family_history': 'पारिवारिक इतिहास',
                'risk_score': 'जोखिम स्कोर',
                'prediction': 'भविष्यवाणी',
                'recommendations': 'सिफारिशें',
                'download_report': 'रिपोर्ट डाउनलोड करें',
                'view_details': 'विवरण देखें',
                'assessment_history': 'मूल्यांकन इतिहास',
                'no_assessments': 'अभी तक कोई मूल्यांकन नहीं',
                'loading': 'लोड हो रहा है...',
                'error': 'त्रुटि',
                'success': 'सफलता',
                'chatbot_greeting': 'नमस्ते! मैं आपका एआई आनुवंशिक स्वास्थ्य सहायक हूं।',
                'enter_symptoms': 'कृपया अपने लक्षणों का वर्णन करें',
                'consult_doctor': 'कृपया उचित निदान के लिए डॉक्टर से परामर्श करें',
                'low_risk': 'कम जोखिम',
                'moderate_risk': 'मध्यम जोखिम',
                'high_risk': 'उच्च जोखिम',
            },
            'bn': {  # Bengali
                'app_name': 'জিনঅ্যাক্সেসএআই',
                'welcome': 'জিনঅ্যাক্সেসএআই-তে স্বাগতম',
                'tagline': 'এআই-চালিত জেনেটিক ডিসঅর্ডার ঝুঁকি পূর্বাভাস',
                'start_assessment': 'মূল্যায়ন শুরু করুন',
                'login': 'লগইন',
                'register': 'নিবন্ধন করুন',
                'logout': 'লগআউট',
                'dashboard': 'ড্যাশবোর্ড',
                'about': 'সম্পর্কে',
                'username': 'ব্যবহারকারীর নাম',
                'email': 'ইমেইল',
                'password': 'পাসওয়ার্ড',
                'submit': 'জমা দিন',
                'cancel': 'বাতিল করুন',
                'symptoms': 'লক্ষণ',
                'family_history': 'পারিবারিক ইতিহাস',
                'risk_score': 'ঝুঁকি স্কোর',
                'prediction': 'পূর্বাভাস',
                'recommendations': 'সুপারিশ',
                'download_report': 'রিপোর্ট ডাউনলোড করুন',
                'view_details': 'বিস্তারিত দেখুন',
                'assessment_history': 'মূল্যায়ন ইতিহাস',
                'no_assessments': 'এখনও কোনো মূল্যায়ন নেই',
                'loading': 'লোড হচ্ছে...',
                'error': 'ত্রুটি',
                'success': 'সফলতা',
                'chatbot_greeting': 'হ্যালো! আমি আপনার এআই জেনেটিক স্বাস্থ্য সহায়ক।',
                'enter_symptoms': 'অনুগ্রহ করে আপনার লক্ষণগুলি বর্ণনা করুন',
                'consult_doctor': 'সঠিক নির্ণয়ের জন্য অনুগ্রহ করে একজন ডাক্তারের সাথে পরামর্শ করুন',
                'low_risk': 'কম ঝুঁকি',
                'moderate_risk': 'মাঝারি ঝুঁকি',
                'high_risk': 'উচ্চ ঝুঁকি',
            },
            'te': {  # Telugu
                'app_name': 'జీన్‌యాక్సెస్ఏఐ',
                'welcome': 'జీన్‌యాక్సెస్ఏఐకి స్వాగతం',
                'tagline': 'ఏఐ-శక్తితో కూడిన జన్యు రుగ్మత ప్రమాద అంచనా',
                'start_assessment': 'అంచనా ప్రారంభించండి',
                'login': 'లాగిన్',
                'register': 'నమోదు చేసుకోండి',
                'logout': 'లాగౌట్',
                'dashboard': 'డాష్‌బోర్డ్',
                'about': 'గురించి',
                'username': 'వినియోగదారు పేరు',
                'email': 'ఇమెయిల్',
                'password': 'పాస్‌వర్డ్',
                'submit': 'సమర్పించండి',
                'cancel': 'రద్దు చేయండి',
                'symptoms': 'లక్షణాలు',
                'family_history': 'కుటుంబ చరిత్ర',
                'risk_score': 'ప్రమాద స్కోర్',
                'prediction': 'అంచనా',
                'recommendations': 'సిఫార్సులు',
                'download_report': 'నివేదికను డౌన్‌లోడ్ చేయండి',
                'view_details': 'వివరాలను చూడండి',
                'assessment_history': 'అంచనా చరిత్ర',
                'no_assessments': 'ఇంకా అంచనాలు లేవు',
                'loading': 'లోడ్ అవుతోంది...',
                'error': 'లోపం',
                'success': 'విజయం',
                'chatbot_greeting': 'హలో! నేను మీ ఏఐ జన్యు ఆరోగ్య సహాయకుడిని.',
                'enter_symptoms': 'దయచేసి మీ లక్షణాలను వివరించండి',
                'consult_doctor': 'సరైన నిర్ధారణ కోసం దయచేసి వైద్యుడిని సంప్రదించండి',
                'low_risk': 'తక్కువ ప్రమాదం',
                'moderate_risk': 'మధ్యస్థ ప్రమాదం',
                'high_risk': 'అధిక ప్రమాదం',
            },
            'ta': {  # Tamil
                'app_name': 'ஜீன்அக்சஸ்ஏஐ',
                'welcome': 'ஜீன்அக்சஸ்ஏஐக்கு வரவேற்கிறோம்',
                'tagline': 'ஏஐ-இயக்கப்படும் மரபணு கோளாறு ஆபத்து கணிப்பு',
                'start_assessment': 'மதிப்பீட்டைத் தொடங்கவும்',
                'login': 'உள்நுழைவு',
                'register': 'பதிவு செய்யவும்',
                'logout': 'வெளியேறு',
                'dashboard': 'டாஷ்போர்டு',
                'about': 'பற்றி',
                'username': 'பயனர் பெயர்',
                'email': 'மின்னஞ்சல்',
                'password': 'கடவுச்சொல்',
                'submit': 'சமர்ப்பிக்கவும்',
                'cancel': 'ரத்து செய்',
                'symptoms': 'அறிகுறிகள்',
                'family_history': 'குடும்ப வரலாறு',
                'risk_score': 'ஆபத்து மதிப்பெண்',
                'prediction': 'கணிப்பு',
                'recommendations': 'பரிந்துரைகள்',
                'download_report': 'அறிக்கையைப் பதிவிறக்கவும்',
                'view_details': 'விவரங்களைக் காண்க',
                'assessment_history': 'மதிப்பீட்டு வரலாறு',
                'no_assessments': 'இன்னும் மதிப்பீடுகள் இல்லை',
                'loading': 'ஏற்றுகிறது...',
                'error': 'பிழை',
                'success': 'வெற்றி',
                'chatbot_greeting': 'வணக்கம்! நான் உங்கள் ஏஐ மரபணு சுகாதார உதவியாளர்.',
                'enter_symptoms': 'தயவுசெய்து உங்கள் அறிகுறிகளை விவரிக்கவும்',
                'consult_doctor': 'சரியான நோயறிதலுக்கு மருத்துவரை அணுகவும்',
                'low_risk': 'குறைந்த ஆபத்து',
                'moderate_risk': 'மிதமான ஆபத்து',
                'high_risk': 'அதிக ஆபத்து',
            }
        }
        
        self.supported_languages = {
            'en': 'English',
            'hi': 'हिन्दी (Hindi)',
            'bn': 'বাংলা (Bengali)',
            'te': 'తెలుగు (Telugu)',
            'ta': 'தமிழ் (Tamil)'
        }
        
        self.default_language = 'en'
    
    def get_text(self, key, language='en'):
        """Get translated text for a given key"""
        if language not in self.translations:
            language = self.default_language
        
        return self.translations[language].get(key, self.translations['en'].get(key, key))
    
    def get_all_translations(self, language='en'):
        """Get all translations for a language"""
        if language not in self.translations:
            language = self.default_language
        
        return self.translations[language]
    
    def get_supported_languages(self):
        """Get list of supported languages"""
        return self.supported_languages
    
    def detect_language(self, text):
        """Simple language detection based on character sets"""
        # Devanagari script (Hindi)
        if any('\u0900' <= char <= '\u097F' for char in text):
            return 'hi'
        # Bengali script
        elif any('\u0980' <= char <= '\u09FF' for char in text):
            return 'bn'
        # Telugu script
        elif any('\u0C00' <= char <= '\u0C7F' for char in text):
            return 'te'
        # Tamil script
        elif any('\u0B80' <= char <= '\u0BFF' for char in text):
            return 'ta'
        # Default to English
        else:
            return 'en'
    
    def translate_medical_terms(self, term, target_language='en'):
        """Translate common medical terms"""
        medical_translations = {
            'en': {
                'genetic disorder': 'Genetic Disorder',
                'symptoms': 'Symptoms',
                'diagnosis': 'Diagnosis',
                'treatment': 'Treatment',
                'risk': 'Risk',
                'hereditary': 'Hereditary',
                'mutation': 'Mutation',
                'chromosome': 'Chromosome',
                'gene': 'Gene',
                'inheritance': 'Inheritance'
            },
            'hi': {
                'genetic disorder': 'आनुवंशिक विकार',
                'symptoms': 'लक्षण',
                'diagnosis': 'निदान',
                'treatment': 'उपचार',
                'risk': 'जोखिम',
                'hereditary': 'वंशानुगत',
                'mutation': 'उत्परिवर्तन',
                'chromosome': 'गुणसूत्र',
                'gene': 'जीन',
                'inheritance': 'विरासत'
            },
            'bn': {
                'genetic disorder': 'জেনেটিক ডিসঅর্ডার',
                'symptoms': 'লক্ষণ',
                'diagnosis': 'নির্ণয়',
                'treatment': 'চিকিৎসা',
                'risk': 'ঝুঁকি',
                'hereditary': 'বংশগত',
                'mutation': 'মিউটেশন',
                'chromosome': 'ক্রোমোজোম',
                'gene': 'জিন',
                'inheritance': 'উত্তরাধিকার'
            },
            'te': {
                'genetic disorder': 'జన్యు రుగ్మత',
                'symptoms': 'లక్షణాలు',
                'diagnosis': 'నిర్ధారణ',
                'treatment': 'చికిత్స',
                'risk': 'ప్రమాదం',
                'hereditary': 'వంశపారంపర్య',
                'mutation': 'మ్యుటేషన్',
                'chromosome': 'క్రోమోజోమ్',
                'gene': 'జన్యువు',
                'inheritance': 'వారసత్వం'
            },
            'ta': {
                'genetic disorder': 'மரபணு கோளாறு',
                'symptoms': 'அறிகுறிகள்',
                'diagnosis': 'நோயறிதல்',
                'treatment': 'சிகிச்சை',
                'risk': 'ஆபத்து',
                'hereditary': 'பரம்பரை',
                'mutation': 'மரபணு மாற்றம்',
                'chromosome': 'குரோமோசோம்',
                'gene': 'மரபணு',
                'inheritance': 'மரபு'
            }
        }
        
        term_lower = term.lower()
        if target_language in medical_translations:
            return medical_translations[target_language].get(term_lower, term)
        return term

# Initialize global instance
translator = MultilingualTranslator()

if __name__ == '__main__':
    # Test translations
    trans = MultilingualTranslator()
    
    print("Supported Languages:")
    for code, name in trans.get_supported_languages().items():
        print(f"{code}: {name}")
    
    print("\nSample Translations:")
    for lang in ['en', 'hi', 'bn', 'te']:
        print(f"\n{lang}:")
        print(f"  Welcome: {trans.get_text('welcome', lang)}")
        print(f"  Start Assessment: {trans.get_text('start_assessment', lang)}")
