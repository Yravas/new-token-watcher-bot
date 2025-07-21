import requests
import time

# === CONFIGURATION ===
TELEGRAM_TOKEN = "7962621975:AAGS5KN9RTtjkJ3ePKSgID6VWlMBmS5SMNE"
TELEGRAM_CHAT_ID = "7609115046"
LP_THRESHOLD = 1000  # Minimum de LP en dollars
SEEN_TOKENS = set()

# === Envoi Telegram ===
def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": text}
    try:
        requests.post(url, data=data)
    except Exception as e:
        print(f"[Telegram] Erreur : {e}")

# === Fetch Birdeye (just listed tokens) ===
def fetch_birdeye_tokens():
    try:
        url = "https://public-api.birdeye.so/public/token/justListed"
        headers = {"x-chain": "solana"}
        r = requests.get(url, headers=headers, timeout=10)
        data = r.json().get("data", [])
        new_tokens = []
        for token in data:
            token_address = token.get("address")
            if token_address not in SEEN_TOKENS:
                lp = token.get("liquidity", 0) / 1e6  # Convert μSOL to SOL
                if lp >= LP_THRESHOLD:
                    name = token.get("name", "Inconnu")
                    symbol = token.get("symbol", "")
                    link = f"https://birdeye.so/token/{token_address}?chain=solana"
                    message = (
                        f"🚀 *Nouveau token détecté sur Birdeye*\n\n"
                        f"📛 *Nom* : {name} ({symbol})\n"
                        f"💧 *LP* : ${int(lp):,}\n"
                        f"🔗 {link}"
                    )
                    new_tokens.append((token_address, message))
        return new_tokens
    except Exception as e:
        print(f"[Birdeye] Erreur : {e}")
        return []

# === Main loop ===
if __name__ == "__main__":
    send_telegram_message("✅ Le bot est en ligne et surveille les nouveaux tokens...")

    while True:
        print("[Bot] Vérification des nouveaux tokens...")
        birdeye_tokens = fetch_birdeye_tokens()

        for token_address, msg in birdeye_tokens:
            if token_address not in SEEN_TOKENS:
                send_telegram_message(msg)
                SEEN_TOKENS.add(token_address)

        # TODO : Ajouter GeckoTerminal + DexScanner ici plus tard
        time.sleep(60)
