"""
ENG: Application-wide constant values
TR: Uygulama genelinde kullanılan sabit değerler
"""

###### utils  ######
SIDEBAR_TEXTS = {
    "tr": {
        "assess": "🔍 Değerlendir",
        "summary": "📋 Özet Gör",
        "clear": "🔄 Temizle",
        "status": "{count} semptom kaydedildi"
    },
    "en": {
        "assess": "🔍 Assess",
        "summary": "📋 Show Summary",
        "clear": "🔄 Clear",
        "status": "{count} symptom(s) recorded"
    }
}


###### actions  ######
ACTION_TYPES = {
    "ASSESS": "assess",
    "SUMMARY": "summary",
    "CLEAR": "clear",
    "CONTINUE": "continue"
}


####### language_detector ######
TURKISH_CHARS = ['ı', 'ğ', 'ü', 'ş', 'ö', 'ç', 'İ', 'Ğ', 'Ü', 'Ş', 'Ö', 'Ç']

TURKISH_KEYWORDS = [
    'ben', 'merhaba', 'nasıl', 'neden', 'için', 'var', 'yok',
    'bu', 'şu', 'ağrı', 'hasta', 've', 'veya', 'ile', 'bir',
    'ne', 'mi', 'mı', 'mu', 'mü'
]

SUPPORTED_LANGUAGES = {
    "TURKISH": "tr",
    "ENGLISH": "en"
}


###### main - Authentication constants  ######
USER_ROLES = {
    "ADMIN": "admin",
    "USER": "user"
}

AUTH_PROVIDERS = {
    "CREDENTIALS": "credentials"
}


###### main - Chat initialization constants  ######
MESSAGES = {
    "greeting": "👋 Hello! I am **Doctor Assistant**.\nI need a few details from you so I can assist you better.",
    "age_prompt": "Thank you {name}! Could you please tell me your age? 🎂",
    "success": "Awesome {name}! 🎉 We can begin our chat.\nWhat's your complaint?",
    "login_required": "Please log in to start a chat.",
    "invalid_age": "⚠️ Invalid or missing age information. The chat has been ended."
}

DEFAULT_SESSION_VALUES = {
    "symptoms": [],
    "language": "en",
    "language_detected": False
}


###### main - Action callback constants  ######
ASSESSMENT_MESSAGES = {
    "en": {
        "no_symptoms": "❌ No symptoms to assess!",
        "loading": "⏳ Assessing...",
        "no_response": "❌ No assessment response",
        "command": "assess"
    },
    "tr": {
        "no_symptoms": "❌ Değerlendirecek semptom yok!",
        "loading": "⏳ Değerlendiriliyor...",
        "no_response": "❌ Değerlendirme yanıtı alınamadı",
        "command": "degerlendir"
    }
}


###### main - Summary action constants  ######
SUMMARY_MESSAGES = {
    "en": {
        "title": "📋 Symptom Summary",
        "none": "No symptoms recorded yet",
        "total": "Total"
    },
    "tr": {
        "title": "📋 Semptom Özeti",
        "none": "Henüz semptom kaydedilmedi",
        "total": "Toplam"
    }
}


###### main - Clear action constants  ######
CLEAR_MESSAGES = {
    "en": "🗑️ Symptoms cleared! You can continue chatting.",
    "tr": "🗑️ Semptomlar temizlendi! Sohbete devam edebilirsiniz."
}


###### main - Assessment card constants  ######
URGENCY_EMOJI = {
    "low": "🟢",
    "medium": "🟡",
    "high": "🟠",
    "emergency": "🔴"
}

URGENCY_LEVELS = {
    "low": "Low",
    "medium": "Medium",
    "high": "High",
    "emergency": "EMERGENCY"
}

ASSESSMENT_CARD_TEXTS = {
    "en": {
        "title": "Health Assessment",
        "urgency": "Urgency Level",
        "symptoms": "Your Symptoms",
        "reasoning": "Assessment",
        "recommendations": "Recommendations",
        "warnings": "Warning Signs",
        "followup": "Doctor Consultation",
        "selfcare": "Self-Care Tips",
        "emergency": "🚨 **URGENT: Seek immediate medical attention!**"
    },
    "tr": {
        "title": "Sağlık Değerlendirmesi",
        "urgency": "Aciliyet Seviyesi",
        "symptoms": "Semptomlarınız",
        "reasoning": "Değerlendirme",
        "recommendations": "Öneriler",
        "warnings": "Dikkat Edilmesi Gerekenler",
        "followup": "Doktor Görüşmesi",
        "selfcare": "Evde Yapabilecekleriniz",
        "emergency": "🚨 **ACİL: Hemen sağlık kuruluşuna başvurun!**"
    }
}


###### main - Main message handler constants  ######
MAIN_MESSAGES = {
    "incomplete_info": "⚠️ Incomplete user's information. Please restart the chat.",
    "loading": "⏳ Processing...",
    "no_response": "❌ No response received",
    "no_reply": "Doctor Assistant: No reply"
}


###### chat_service - Assessment response formatting constants  ######
ASSESSMENT_RESPONSE_TEXTS = {
    "en": {
        "report_title": "Assessment Report",
        "urgency_level": "Urgency Level",
        "score": "Score",
        "assessment": "Assessment",
        "recommendations": "Recommendations",
        "doctor_consultation": "Doctor Consultation",
        "warning_signs": "Warning Signs",
        "self_care": "Self-Care Tips",
        "emergency": "🚨 **EMERGENCY: Seek immediate medical attention!**"
    },
    "tr": {
        "report_title": "Değerlendirme Raporu",
        "urgency_level": "Aciliyet Seviyesi",
        "score": "Skor",
        "assessment": "Değerlendirme",
        "recommendations": "Öneriler",
        "doctor_consultation": "Doktor Görüşmesi",
        "warning_signs": "Dikkat Edilmesi Gerekenler",
        "self_care": "Evde Yapabilecekleriniz",
        "emergency": "🚨 **ACİL DURUM: En yakın sağlık kuruluşuna başvurun!**"
    }
}


###### chat_service - Chat processing constants ######
TRIGGER_WORDS = {
    "assessment": [
        "değerlendir", "analiz", "acil mi", "durumum ne", "rapor", "sonuç", "teşhis",
        "evaluate", "analyze", "is it urgent", "what is my situation","assessment", "diagnose","report", "result"
    ]
}

DEFAULT_EXTRACTED_DATA = {
    "symptoms": [],
    "last_assessment": None,
    "last_advice": None
}