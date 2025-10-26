===== Proje Özeti =====

Bu proje, LangChain, FastAPI, Chainlit' de Groq/ localde Ollama ve Chainlit kullanılarak geliştirilmiş bir LLM tabanlı doktor asistanıdır.
Kullanıcının doğal dilde (Türkçe veya İngilizce) yazdığı mesajlardan semptom çıkarımı, hafıza yönetimi ve değerlendirme yapar.


Mimarinin Kısa Özeti
    >>> Kullanıcı → Chainlit → FastAPI → LangChain → LLM (Groq veya Ollama)

===== Ana Özellikler =====

Çok Dilli Destek (Türkçe / İngilizce)
    > Kullanıcının konuşma dili otomatik tespit edilir.
    > Dil konuşma ortasında değişse bile hafıza korunur.
Dinamik Hafıza Yönetimi
    > InMemoryChatMessageHistory kullanılarak önceki mesajlar saklanır.
    > LLM cevapları bağlama göre üretir.

Semptom Çıkarımı ve Değerlendirme
    > Mesajlardan semptomlar çıkarılır ve otomatik değerlendirme akışı başlatılır.

Asenkron Yapı (async/await)
    > Backend tüm akışlarda asenkron çalışır.

Frontend + Backend Ayrımı
    > Frontend: Chainlit arayüzü
    > Backend: FastAPI tabanlı REST servisi


===== Neden iki Farklı Model Kullandım? =====

Bu projenin konusuna en uygun yöntem Ollama modeli kullanmaktır ama bu bir demo projesi olduğu için herkesin deneyebilmesi adına Chainlit ile Groq modelini kullandım.
Ayrıca, böyle bir projenin gerçek hayatta nasıl kullanılabileceğini göstermek için de yerel makinede ollama kullandım.
Not: llm.py de groq kısmını kaldırırsanız ollama + chainlit yapısıyla lokalde kullanmaya devam edebilirsiniz. Sadece Groq modelini kaldırmanız yeterli.


========= Kurulum (Yerel Geliştirme) =========
Öncelikle bağımlılıkları yükleyin.
    pip install -r requirements.txt

Projede Chainlit + Groq kullanmak isterseniz;
    Projeyi çalıştırmak için iki terminal açmalısınız
        1. sine api başlatma komutunu yazmalısınız
        --> uvicorn app.api.assistant_api:app --reload
        2. sine chainlit başlatma komutunu yazmalısınız (boş olan bir port girebilirsiniz, ben 8002 portunu kullandım)
        --> chainlit run main.py --port 8002 -wh

    Not: fast api 8000 portunu kullandığı için chainlit için farklı bir port girmeliyiz

=========

Eğer Chainlit + Ollama kullanmak isterseniz;
    Projeyi çalıştırmak ve llm ile sohbet etmek için üç terminal açmalısınız
        1. sine aşağıdaki ollama servisini başlatan kodu yazmalısınız
        --> ollama serve
        2. sine api başlatma komutunu yazmalısınız
        --> uvicorn app.api.assistant_api:app --reload
        3. sine client_test yolunu yazmalısınız ve artık çalıştırabilirsiniz
        --> python C:\...\DoctorAssistant\tests\client_test.py  (kendi client_test yolunuzu girin. Bunu yapmak için;
        client_test dosyayınzın üzerine sağ tıklayın "Copy Path/Reference" ye tıklayın ve ardından "Absolute Path' e tıklamanız yeterli. Yolu kopyalacaktır.")

    Not: Ollama modelinin çalışması için bilgisayarınızda ollama'nın kurulu olması ve ollama içinde de config.py' de belirlediğimiz "qwen2.5:3b" modelinin yüklü olması gerekmektedir!
         İstediğiniz herhangi bir model kullanabilirsiniz alternatif modelleri cofig.py' de belirttim. Sadece kullanmadan önce Ollama'da yüklü olduğundan emin olun!
