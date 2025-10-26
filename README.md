### ENG :
# AI Doctor Assistant

### ===== 🩺 About the Project

This project is an LLM-based doctor assistant developed using LangChain, FastAPI, and Chainlit, leveraging Groq via Chainlit or Ollama locally.
It extracts symptoms, manages memory, and performs evaluations from user messages written in natural language (Turkish or English).

Short Architecture Overview
    > User → Chainlit → FastAPI → LangChain → LLM (Groq or Ollama)

### ===== ⚙️ Main Features

##### 🌐 Multilingual Support (Turkish / English)
    > Automatically detects the user’s language.  
    > Memory is preserved even if the language changes mid-conversation.  
    > Custom functions are implemented for language detection and control.

##### 🧠 Dynamic Memory Management
    > Previous messages are stored using InMemoryChatMessageHistory.  
    > LLM responses are generated contextually.

##### 🧩 Symptom Extraction and Evaluation
    > Symptoms are extracted from messages, triggering the evaluation workflow.

##### ⚕️ Evaluation Workflow
    > Analyzes recorded symptoms to provide urgency, recommendations, and risk assessment.

##### 🧬 Asynchronous Architecture (async/await)
    > The backend operates asynchronously across all flows. Fast, modular, and scalable.


### ===== 🧩 Technologies Used

##### 🖥️ Frontend 
    > Chainlit interface: Interactive chat UI  
    > Action Callbacks: Button-based interactions like "Assess", "Show Summary", "Clear"  
    > Real-time Session Management: User-specific session handling

##### 🧩 Backend

| Technology                | Description                                |
| ------------------------- | ------------------------------------------ |
| **FastAPI**               | Asynchronous REST API service              |
| **LangChain**             | LLM flow management and memory             |
| **ChatGroq / ChatOllama** | LLM models (local or cloud-based)          |
| **Pydantic**              | Data validation and schema management      |
| **Custom Memory Manager** | User-specific memory control               |
| **Language Detector**     | Automatic message-based language detection |


### ===== Why Two Different Models? =====

While Ollama is the most suitable model for this project, for demo purposes and to allow everyone to try it, we used Groq via Chainlit.
Additionally, to demonstrate real-world usage, Ollama can be run locally.

**Note:** If you remove the Groq part from llm.py, you can continue to use Ollama + Chainlit locally. You only need to remove the Groq model.

### ===== 🚀 Setup and Running

**First, create a virtual environment and install dependencies:**

> python -m venv venv
> venv\Scripts\activate
> pip install -r requirements.txt


**If you want to use Chainlit + Groq:**

Open two terminals to run the project:    
1. Start the API in one terminal:
   > uvicorn app.api.assistant_api:app --reload
2. Start Chainlit in another terminal (choose any free port, e.g., 8002):
   > chainlit run main.py --port 8002 -wh

**Note:** Since FastAPI uses port 8000, Chainlit should run on a different port.

**If you want to use Chainlit + Ollama:**

Open three terminals to run the project and chat with the LLM:
1. Start the Ollama service:
   > ollama serve
2. Start the API:
   > uvicorn app.api.assistant_api:app --reload
3. Run the client test script:
   > python C:\...\DoctorAssistant\tests\client_test.py
(Replace with your own client_test.py absolute path. Right-click the file → Copy Path/Reference → Absolute Path.)
    
**Note**: To use the Ollama model, Ollama must be installed on your machine, and the model defined in config.py (e.g., "qwen2.5:3b") must be downloaded.
    
    You can use any model; alternatives are listed in config.py. Just ensure it’s installed in Ollama before use.


#### ===========  ******** =========  ******** ========= ******** =========

### TR :
# AI Doktor Asistanı

### ===== 🩺 Proje Hakkında

Bu proje, LangChain, FastAPI, Chainlit' de Groq/ localde Ollama ve Chainlit kullanılarak geliştirilmiş bir LLM tabanlı doktor asistanıdır.
Kullanıcının doğal dilde (Türkçe veya İngilizce) yazdığı mesajlardan semptom çıkarımı, hafıza yönetimi ve değerlendirme yapar.

Mimarinin Kısa Özeti
    > Kullanıcı → Chainlit → FastAPI → LangChain → LLM (Groq veya Ollama)

### ===== ⚙️ Ana Özellikler

##### 🌐 Çok Dilli Destek (Türkçe / İngilizce)
    > Kullanıcının konuşma dili otomatik tespit edilir.
    > Dil konuşma ortasında değişse bile hafıza korunur.
    > Dil tespiti ve kontrolleri için fonksiyonlar yazılmıştır

##### 🧠 Dinamik Hafıza Yönetimi
    > InMemoryChatMessageHistory kullanılarak önceki mesajlar saklanır.
    > LLM cevapları bağlama göre üretir.

##### 🧩 Semptom Çıkarımı ve Değerlendirme
    > Mesajlardan semptomlar çıkarılır ve değerlendirme akışı başlatılır.

##### ⚕️ Değerlendirme Akışı
    > Kayıtlı semptomları analiz ederek aciliyet, öneri ve risk değerlendirmesi sunar.

##### 🧬 Asenkron Yapı (async/await)
    > Backend tüm akışlarda asenkron çalışır. Hızlı, modüler ve ölçeklenebilirdir

### ===== 🧩 Kullanılan Teknolojiler

##### 🖥️ Frontend 
    > Chainlit arayüzü : Etkileşimli sohbet arayüzü
    > Action Callback’ler : “Değerlendir”, “Özet Gör”, “Temizle” gibi buton tabanlı etkileşimler
    > Gerçek Zamanlı Oturum Yönetimi : Kullanıcıya özel session yönetimi

##### 🧩 Backend:

| Teknoloji                 | Açıklama                                 |
| ------------------------- | ---------------------------------------- |
| **FastAPI**               | Asenkron REST API servisi                |
| **LangChain**             | LLM akış yönetimi ve hafıza              |
| **ChatGroq / ChatOllama** | LLM modelleri (local veya bulut tabanlı) |
| **Pydantic**              | Veri doğrulama ve şema yönetimi          |
| **Custom Memory Manager** | Kullanıcı bazlı bellek kontrolü          |
| **Language Detector**     | Mesaj bazlı otomatik dil algılama        |


### ===== Neden iki Farklı Model Kullandım? =====

Bu projenin konusuna en uygun yöntem Ollama modeli kullanmaktır ama bu bir demo projesi olduğu için herkesin deneyebilmesi adına Chainlit ile Groq modelini kullandım.
Ayrıca, böyle bir projenin gerçek hayatta nasıl kullanılabileceğini göstermek için de yerel makinede ollama kullandım.
Not: llm.py de groq kısmını kaldırırsanız ollama + chainlit yapısıyla lokalde kullanmaya devam edebilirsiniz. Sadece Groq modelini kaldırmanız yeterli.


### ===== 🚀 Kurulum ve Çalıştırma

**Öncelikle sanal ortamı ayarlayın ve bağımlılıkları yükleyin.**

> python -m venv venv
> venv\Scripts\activate
> pip install -r requirements.txt

**Projede Chainlit + Groq kullanmak isterseniz;**

Projeyi çalıştırmak için iki terminal açmalısınız
        
1. terminale api başlatma komutunu yazmalısınız
   > uvicorn app.api.assistant_api:app --reload
2. terminale chainlit başlatma komutunu yazmalısınız (boş olan bir port girebilirsiniz, ben 8002 portunu kullandım)
   > chainlit run main.py --port 8002 -wh

   **Not**: fast api 8000 portunu kullandığı için chainlit için farklı bir port girmeliyiz

=========

**Eğer Chainlit + Ollama kullanmak isterseniz;**

Projeyi çalıştırmak ve llm ile sohbet etmek için üç terminal açmalısınız
1. terminale aşağıdaki ollama servisini başlatan kodu yazmalısınız
   > ollama serve
2. terminale api başlatma komutunu yazmalısınız
   > uvicorn app.api.assistant_api:app --reload
3. terminale client_test yolunu yazmalısınız ve artık çalıştırabilirsiniz
   > python C:\...\DoctorAssistant\tests\client_test.py  (kendi client_test yolunuzu girin. Bunu yapmak için;
client_test dosyayınzın üzerine sağ tıklayın "Copy Path/Reference" ye tıklayın ve ardından "Absolute Path' e tıklamanız yeterli. Yolu kopyalacaktır.")

**Not**: Ollama modelinin çalışması için bilgisayarınızda ollama'nın kurulu olması ve ollama içinde de config.py' de belirlediğimiz "qwen2.5:3b" modelinin yüklü olması gerekmektedir!
İstediğiniz herhangi bir model kullanabilirsiniz alternatif modelleri cofig.py' de belirttim. Sadece kullanmadan önce Ollama'da yüklü olduğundan emin olun!


### 🧑‍💻 Developer ( Geliştirici )
👋 **Gülşen Demir** — Data Scientist & AI Developer

### ===== 📫 Contact ( İletişim )
    Email: alyula.coder@gmail.com | gulsendemirbm@gmail.com
    LinkedIn: linkedin.com/in/gulsendemir

### ===== ▶️ Project Demo and Video Presentation ( Projenin Demo ve Video Sunumu )

Chainlit-App : []
Youtube: [https://youtu.be/P3jrZfgo25w]

