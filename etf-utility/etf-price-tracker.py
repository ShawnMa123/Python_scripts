import requests
import yfinance as yf
import time
import os
from dotenv import load_dotenv

load_dotenv()

# Replace with your actual tokens/keys (or use environment variables)
BOT_TOKEN = os.environ.get("BOT_TOKEN")
YOUR_TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

def get_qqqm_data_yfinance():
    try:
        qqqm = yf.Ticker("QQQM")
        data = qqqm.info
        if data:
            price = data.get("regularMarketPrice") or data.get("currentPrice")
            change = data.get("regularMarketChange")
            change_percent = data.get("regularMarketChangePercent")
            volume = data.get("regularMarketVolume")

            if all(v is not None for v in [price, change, change_percent, volume]):
                return {
                    "price": price,
                    "change": change,
                    "change_percent": f"{change_percent * 100:.2f}%",
                    "volume": volume
                }
            else:
                print("Could not retrieve all required QQQM data from yfinance")
                return None
        else:
            print("Could not retrieve QQQM data from yfinance")
            return None
    except Exception as e:
        print(f"Error fetching data using yfinance: {e}")
        return None

def send_qqqm_update():
    qqqm_data = get_qqqm_data_yfinance()
    if qqqm_data:
        message = (
            f"<b>QQQM Update:</b>\n"
            f"Price: ${qqqm_data['price']:.2f}\n"
            f"Change: ${qqqm_data['change']:.2f} ({qqqm_data['change_percent']})\n"
            f"Volume: {qqqm_data['volume']}"
        )
    else:
        message = "Could not retrieve QQQM data."

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': YOUR_TELEGRAM_CHAT_ID,
        'text': message,
        'parse_mode': 'HTML'
    }
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        print("Message sent successfully")
    else:
        print(f"Failed to send message: {response.status_code}")

def main():
    while True:
        send_qqqm_update()
        # Sleep for one hour
        time.sleep(3600)

if __name__ == '__main__':
    main()