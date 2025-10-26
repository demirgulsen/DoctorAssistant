"""
Hangi modellere ihtiyacımız var:

1. SymptomExtraction - Kullanıcı mesajından semptomları çıkar
    Amaç: Kullanıcının mesajından semptomları çıkarmak
    Ne zaman kullanılır: Her kullanıcı mesajında
    Alanlar:
    - symptoms: List[str] - Tespit edilen semptomlar listesi
    - duration: Optional[str] - Şikayetin süresi (örn: "2 gündür", "3 hafta")
    - severity: str - "mild", "moderate", "severe"
    - additional_info: Optional[str] - Diğer önemli bilgiler

2. TriageAssessment - Aciliyet değerlendirmesi
    Amaç: Aciliyet değerlendirmesi yapmak
    Ne zaman kullanılır: Yeterli semptom toplandıktan sonra

    Alanlar:
    - urgency_score: int - 1-10 arası skor (10 en acil)
    - urgency_level: str - "low", "medium", "high", "emergency"
    - requires_immediate_care: bool - Hemen hastaneye gitmeli mi?
    - reasoning: str - Neden bu skoru verdiğini açıklama

3. MedicalAdvice - Yapılandırılmış tavsiye
    Amaç: Yapılandırılmış tıbbi tavsiye vermek
    Ne zaman kullanılır: Değerlendirme sonrası

    Alanlar:
    - recommendations: List[str] - Yapılması gerekenler listesi
    - warning_signs: List[str] - Dikkat edilmesi gereken semptomlar
    - follow_up_timeframe: str - "24 saat içinde", "1 hafta içinde" vb.
    - self_care_tips: List[str] - Evde yapılabilecek şeyler

4. ConversationState - Hangi aşamada olduğumuzu takip etme
    Amaç: Konuşmanın hangi aşamada olduğunu takip etmek
    Ne zaman kullanılır: Her mesaj işlenirken durum kontrolü için

    Alanlar:
    - current_phase: str - "symptom_gathering", "assessment", "advice", "follow_up"
    - symptoms_collected: int - Kaç semptom toplandı
    - ready_for_assessment: bool - Değerlendirme yapılabilir mi?
    - last_updated: str - Son güncelleme zamanı
"""
from pydantic import BaseModel, Field
from enum import Enum
from typing import List, Optional

class ChatRequest(BaseModel):
    """Chat message input model"""
    name: str
    age: int
    message: str
    language: str = "en"
    provider: str = "groq"    # To use Ollama locally and Groq in Chainlit

class ChatResponse(BaseModel):
    """Chat response output model"""
    response: str
    symptoms: List[str] = Field(default_factory=list)
    symptom_count: int = 0


# Enums (for constant values)
class Severity(str, Enum):
    MILD = "mild"
    MODERATE = "moderate"
    SEVERE = "severe"


class UrgencyLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    EMERGENCY = "emergency"


class ConversationPhase(str, Enum):
    SYMPTOM_GATHERING = "symptom_gathering"
    ASSESSMENT = "assessment"
    ADVICE = "advice"


# Model 1: Eliminate Symptoms
class SymptomExtraction(BaseModel):
    symptoms: List[str] = Field(default_factory=list)
    duration: Optional[str] = None
    severity: Severity = Severity.MILD
    additional_info: Optional[str] = None


# Model 2: Urgency Assessment
class TriageAssessment(BaseModel):
    urgency_score: int = Field(ge=1, le=10)
    urgency_level: UrgencyLevel
    requires_immediate_care: bool = False
    reasoning: str


# Model 3: Medical Advice
class MedicalAdvice(BaseModel):
    recommendations: List[str] = Field(default_factory=list)
    warning_signs: List[str] = Field(default_factory=list)
    follow_up_timeframe: str
    self_care_tips: List[str] = Field(default_factory=list)


# Model 4: Talking Status (Opsiyonel)
class ConversationState(BaseModel):
    current_phase: ConversationPhase = ConversationPhase.SYMPTOM_GATHERING
    symptoms_collected: int = 0
    ready_for_assessment: bool = False
