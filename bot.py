import requests
import time

# === CONFIGURATION ===
TOKEN = "7962621975:AAGS5KN9RTtjkJ3ePKSgID6VWlMBmS5SMNE"
chat_id = "7609115046"

# === Fonction d’envoi d’un message Telegram ===
def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print("Erreur lors de l'envoi Telegram :", e)

# === Message de test au démarrage ===
send_telegram_message("✅ Le bot a bien démarré et fonctionne correctement.")

# === Exemple de boucle (à remplacer par la vraie logique de détection de tokens) ===
while True:
    # TODO : remplacer ce bloc par la détection réelle de nouveaux tokens
    print("Bot en veille... (simulation)")
    time.sleep(60)
