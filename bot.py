
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
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": text, "parse_mode": "Markdown"}
    try:
        requests.post(url, data=data)
    except Exception as e:
        print(f"[Telegram] Erreur : {e}")

# === Birdeye ===
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
                lp = token.get("liquidity", 0) / 1e6
                if lp >= LP_THRESHOLD:
                    name = token.get("name", "Inconnu")
                    symbol = token.get("symbol", "")
                    link = f"https://birdeye.so/token/{token_address}?chain=solana"
                    message = (
                        f"🚀 *Nouveau token détecté sur Birdeye*

"
                        f"📛 *Nom* : {name} ({symbol})
"
                        f"💧 *LP* : ${int(lp):,}
"
                        f"🔗 {link}"
                    )
                    new_tokens.append((token_address, message))
        return new_tokens
    except Exception as e:
        print(f"[Birdeye] Erreur : {e}")
        return []

# === GeckoTerminal ===
def fetch_gecko_tokens():
    try:
        url = "https://api.geckoterminal.com/api/v2/networks/solana/pools/new"
        r = requests.get(url, timeout=10)
        data = r.json().get("data", [])
        new_tokens = []
        for item in data:
            attributes = item.get("attributes", {})
            token_address = attributes.get("base_token_address")
            if token_address and token_address not in SEEN_TOKENS:
                name = attributes.get("base_token_name", "Inconnu")
                symbol = attributes.get("base_token_symbol", "")
                lp = float(attributes.get("reserve_in_usd", 0))
                if lp >= LP_THRESHOLD:
                    link = f"https://www.geckoterminal.com/solana/pools/{item.get('id')}"
                    message = (
                        f"🦎 *Nouveau token sur GeckoTerminal*

"
                        f"📛 *Nom* : {name} ({symbol})
"
                        f"💧 *LP* : ${int(lp):,}
"
                        f"🔗 {link}"
                    )
                    new_tokens.append((token_address, message))
        return new_tokens
    except Exception as e:
        print(f"[GeckoTerminal] Erreur : {e}")
        return []

# === DexScanner ===
def fetch_dexscanner_tokens():
    try:
        url = "https://api.dexscreener.com/latest/dex/pairs/solana"
        r = requests.get(url, timeout=10)
        data = r.json().get("pairs", [])
        new_tokens = []
        for item in data[:15]:
            token_address = item.get("pairAddress")
            if token_address and token_address not in SEEN_TOKENS:
                name = item.get("baseToken", {}).get("name", "Inconnu")
                symbol = item.get("baseToken", {}).get("symbol", "")
                lp = float(item.get("liquidity", {}).get("usd", 0))
                if lp >= LP_THRESHOLD:
                    link = f"https://dexscreener.com/solana/{token_address}"
                    message = (
                        f"🧪 *Nouveau token sur DexScanner*

"
                        f"📛 *Nom* : {name} ({symbol})
"
                        f"💧 *LP* : ${int(lp):,}
"
                        f"🔗 {link}"
                    )
                    new_tokens.append((token_address, message))
        return new_tokens
    except Exception as e:
        print(f"[DexScanner] Erreur : {e}")
        return []

# === Main loop ===
if __name__ == "__main__":
    send_telegram_message("✅ Le bot est en ligne et surveille les nouveaux tokens (3 sources)...")
    while True:
        for fetcher in [fetch_birdeye_tokens, fetch_gecko_tokens, fetch_dexscanner_tokens]:
            for t, msg in fetcher():
                if t not in SEEN_TOKENS:
                    send_telegram_message(msg)
                    SEEN_TOKENS.add(t)
        time.sleep(60)
