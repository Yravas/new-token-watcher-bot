import requests
import time
import telegram

# Ton token Telegram
BOT_TOKEN = "7962621975:AAGS5KN9RTtjkJ3ePKSgID6VWlMBmS5SMNE"
# Ton chat ID personnel
CHAT_ID = "7609115046"
# Envoyer un message test au démarrage
def send_startup_message():
    message = "✅ Le bot a bien démarré et fonctionne correctement."
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": chat_id, "text": message}
    try:
        requests.post(url, data=data)
    except Exception as e:
        print("Erreur lors de l'envoi du message test :", e)

# Appeler la fonction au lancement du script
send_startup_message()

# Intervalle entre chaque vérification (en secondes)
CHECK_INTERVAL = 30
SEEN = set()

bot = telegram.Bot(token=BOT_TOKEN)

def check_new_tokens():
    url = "https://public-api.birdeye.so/public/token/last_created"
    try:
        response = requests.get(url)
        tokens = response.json().get("data", [])
    except Exception as e:
        print(f"Erreur API : {e}")
        return

    for token in tokens:
        address = token.get("address")
        if address and address not in SEEN:
            SEEN.add(address)
            name = token.get("name", "N/A")
            symbol = token.get("symbol", "N/A")
            mcap = token.get("market_cap", "N/A")
            liquidity = token.get("liquidity", "N/A")
            link = f"https://dexscreener.com/solana/{address}"
            message = (
                f"🚨 *Nouveau Token détecté !*\n\n"
                f"🪙 *{name}* ({symbol})\n"
                f"💰 MCAP : {mcap}\n"
                f"💦 Liquidité : {liquidity}\n"
                f"📊 [Voir graphique]({link})"
            )
            try:
                bot.send_message(chat_id=CHAT_ID, text=message, parse_mode="Markdown", disable_web_page_preview=True)
                print(f"Notification envoyée pour {name} ({symbol})")
            except Exception as e:
                print(f"Erreur Telegram : {e}")

if __name__ == "__main__":
    print("🚀 Bot lancé...")
    while True:
        check_new_tokens()
        time.sleep(CHECK_INTERVAL)
