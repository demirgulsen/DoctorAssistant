"""
Terminal üzerinden fast api kullanarak ollama modeli ile sohbet (post atarak)
api endpoint: /chat
"""

import requests
import os
os.environ["LLM_PROVIDER"] = "ollama"

def send_message(name: str, age: int, user_msg: str) -> str:
    """Kullanıcı mesajını FastAPI sunucusuna gönderir ve yanıt döndürür."""

    API_URL: str = "http://127.0.0.1:8000/chat"
    # API ye gönderilecek veri paketi
    payload = {
        "name": name,
        "age": age,
        "message": user_msg,
        "provider": "ollama"
    }
    try:
        # fastapi sunusuna post isteği atalım
        res = requests.post(API_URL, json=payload, timeout=80)

        # eğer istek başarılıysa, yanıt içinde response kodu yazdırılır
        if res.status_code == 200:
            return res.json().get("response", "The assistant couldn’t generate to repond")
        else:
            return f"Error: {res.status_code} - {res.text}"
    except requests.exceptions.RequestException as e:
        return f"Connection error: {e}"

def start_chat():
    """Terminal üzerinden sohbeti başlatır."""
    print("=== Doctor Assistant Terminal Chat ===")
    name = input("Your name: ")
    age_input = input("Your age: ")
    age = int(age_input) if age_input.isdigit() else 0

    print("\nThe chat has started. Type quit, to exit.\n")
    # Kullanıcıdan mesaj alalım ve sunucuya gönderelim
    while True:
        user_msg = input(f"{name}: ").strip()
        if user_msg.lower() == "quit":
            print("The program has ended. Take care of yourself!")
            break

        reply = send_message(name, age, user_msg)
        print(f"Doctor Assistant: {reply}\n")


if __name__ == "__main__":
    start_chat()



# client_test dosyasını çalıştırmak ve llm ile sohbet etmek için üç terminal açmalısınız
# 1. sine aşağıdaki ollama servisini başlatan kodu yazmalısınız
# --> ollama serve
# 2. sine api başlatma komutunu yazmalısınız
# --> uvicorn app.api.assistant_api:app --reload
# 3. sine client_test yolunu yazmalısınız ve artık çalıştırabilirsiniz
# --> python C:\...\DoctorAssistant\tests\client_test.py  (kendi client_test yolunuzu girin. Bunu yapmak için;
# client_test dosyayınzın üzerine sağ tıklayın "Copy Path/Reference" ye tıklayın ve ardından "Absolute Path' e tıklamanız yeterli. Yolu kopyalacaktır")

# ÖNEMLİ NOT
# client_test' de ollama modeli kullanıldı. Bunların çalışması için bilgisayarınızda ollama' nın kurulu olması ve
# ollama içinde de config.py' de belirlediğimiz "qwen2.5:3b" modelinin yüklü olması gerekmektedir!
