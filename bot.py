import requests
from bs4 import BeautifulSoup
import os

# Telegram credentials
TELEGRAM_TOKEN = "8413500001:AAG5Zwxv6shWkEVoXsNg1bAVQdbw1D4pSCc"
CHAT_ID = "1648177856"

# Binance announcement URL
URL = "https://www.binance.com/en/support/announcement/list/48"
headers = {"User-Agent": "Mozilla/5.0"}
LAST_TITLE_FILE = "last_sent_title.txt"

def send_telegram_message(msg):
    api_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": msg}
    try:
        requests.post(api_url, data=data)
    except Exception as e:
        print("Telegram send failed:", e)

def get_latest_listing_announcement():
    r = requests.get(URL, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")
    links = soup.find_all("a", href=True)
    for link in links:
        if "/en/support/announcement/" in link['href']:
            title = link.text.strip()
            title_lower = title.lower()
            if "will launch" in title_lower or "futures" in title_lower:
                full_url = "https://www.binance.com" + link['href']
                return title, full_url
    return None, None

def has_been_sent(title):
    if not os.path.exists(LAST_TITLE_FILE):
        return False
    with open(LAST_TITLE_FILE, "r") as f:
        last_title = f.read().strip()
    return title == last_title

def save_sent_title(title):
    with open(LAST_TITLE_FILE, "w") as f:
        f.write(title)

def main():
    title, link = get_latest_listing_announcement()
    if title and not has_been_sent(title):
        send_telegram_message(f"📢 Binance Listing Alert:\n\n{title}\n{link}")
        save_sent_title(title)

if __name__ == "__main__":
    main()
