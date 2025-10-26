"""
problem tanımı: Kullanıcının sağlıkla ilgili sorularını anlayan ve yanıtlayan bir groq tabanlı doctor asistanı chatbot
    - Kullanıcının adını ve yaşını dikkate alan cevaplar üretmeli
    - Mesaj geçmişini hatırlayarak diyaloğu ona göre sürdürmeli (memory)
    - Langchain and ücretsiz LLM (Groq)
    - İlk olarak terminalde çalışan bir versiyon, ardından FastAPI tabanlı bir web servisi oluşturalım
    - client tarafını yazıp test edelim

model tanıtımı : Ücretsiz LLM ile oluşturulan modeli kullanalım, Groq -> llama-3.3-70b-versatile
    - API üzerinden iletişim kurarak gerçek zamanlı sağlık önerilerini alalım

Langcahin: LLM kütüphanesi - Memory için
    - prompt yonetimi
    - memory
    - tool entegrasyonu: ai agents için tool kullanımı
    - chain yapısı

install libraries
     - fastapi : web api geliştirmek için bir freamwork (asenkron)
               - pip install fastapi
     - uvicorn: fastapi çalıştırmak için gerekli sunucu
     - langchain
     - ChatGroq
     - python-dotenv: .env dosyasından api anahtarını almak için kullanacağız
"""

# import libraries
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.chat_history import InMemoryChatMessageHistory

def main():
    ###### ortam değişkenlerini tanımlama
    load_dotenv()
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError("GROQ_API_KEY bulunamadı. Lütfen .env dosyasını kontrol edin.")

    ###### LLM
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",   # llama-3.1-8b-instant
        api_key=api_key,
        temperature=0.2,
        timeout=30,
        max_retries=3,
    )

    ###### Memory
    memory = InMemoryChatMessageHistory()

    ###### kullanıcı bilgilerini al - isim ve yas
    name = input("Adınız: ")
    age = int(input("Yaşınız: "))

    intro = (
        f"Sen bir doktor asistanısını, Hasta {name}, {age} yaşında."
        "Sağlık sorunları hakkında konuşmak istiyor."
        "Yaşına uygun dikkatli ve nazik tavsiyeler ver; ismiyle hitap et."
        "Hastanın soru sorduğu dil ile cevap ver"
    )

    memory.add_message(HumanMessage(content=intro))
    print("Merhaba ben bir doktor asistanıyım. Size nasıl yardımcı olabilirim?")

    ###### chatbot döngüsü tanımlama
    while True:
        user_msg = input(f"{name}: ")
        if user_msg.lower() == "quit":  # konuşmayı sonlandır
            print("Sana yardımcı olmak harikaydı. Görüşmek üzere" )
            break

        # Doktor asistanı cevap verdi ve hafızaya atıldı  -- conversation de kayıtlar tutuluyor
        memory.add_message(HumanMessage(content=user_msg))
        reply = llm.invoke(memory.messages)   # llm cevabı
        reply_text = reply.content if hasattr(reply, 'content') else str(reply)

        # AI cevabını memory'ye ekle
        memory.add_message(AIMessage(content=reply_text))

        print(f"Doktor Asistanı: {reply}")

        # Veirlen cevapları ekranda göster
        print("Hafıza: ")
        for idx, m in enumerate(memory.messages, start=1):
            print(f"{idx:02d}. {m.type.upper()}: {m.content}")

        print("______________________________________________")



if __name__ == "__main__":
    main()