# bot.py
import requests
from bs4 import BeautifulSoup
import time
import os

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
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
    try:
        r = requests.get(URL, headers=headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        links = soup.find_all('a', href=True)
        for link in links:
            if '/en/support/announcement/' in link['href']:
                return "https://www.binance.com" + link['href']
    except Exception as e:
        print("Error fetching listing:", e)
    return None

def monitor():
    last_seen = get_latest_announcement()
    print("👀 Monitoring started. Last post:", last_seen)
    while True:
        time.sleep(60)
        latest = get_latest_announcement()
        if latest and latest != last_seen:
            send_telegram_message(f"🚨 New Binance Listing!\n{latest}")
            last_seen = latest

if __name__ == "__main__":
    monitor()
