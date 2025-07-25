import requests
from bs4 import BeautifulSoup

# Hardcoded Telegram credentials
TELEGRAM_TOKEN = "8413500001:AAG5Zwxv6shWKeVoxSNg1bAvQdbw1D4pSCc"
CHAT_ID = "1648177856"

# Binance listing announcement URL
URL = "https://www.binance.com/en/support/announcement/list/48"

headers = {
    "User-Agent": "Mozilla/5.0"
}

def send_telegram_message(msg):
    api_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": msg}
    try:
        requests.post(api_url, data=data)
    except Exception as e:
        print("Telegram send failed:", e)

def get_latest_announcement():
    r = requests.get(URL, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")
    links = soup.find_all("a", href=True)
    for link in links:
        if "/en/support/announcement/" in link['href']:
            full_url = "https://www.binance.com" + link['href']
            title = link.text.strip()
            return title, full_url
    return None, None

def main():
    title, link = get_latest_announcement()
    if title:
        send_telegram_message(f"Binance listing check:\n\n{title}\n{link}")

if __name__ == "__main__":
    main()
