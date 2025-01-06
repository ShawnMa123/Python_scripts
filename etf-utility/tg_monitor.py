import os
import yfinance as yf
import telegram
import asyncio
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler('etf_tracker.log'),
        logging.StreamHandler()
    ]
)

# Retrieve environment variables
TELEGRAM_BOT_TOKEN = os.getenv('BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')


# Validate environment variables
def validate_env_vars():
    errors = []

    if not TELEGRAM_BOT_TOKEN:
        errors.append("TELEGRAM_BOT_TOKEN is missing")

    if not TELEGRAM_CHAT_ID:
        errors.append("TELEGRAM_CHAT_ID is missing")

    if errors:
        error_message = "Environment Configuration Errors:\n" + "\n".join(errors)
        logging.error(error_message)
        raise ValueError(error_message)


# List of ETFs to track
ETFS = ['VOO', 'QQQM', 'SGOV']


def create_robust_session():
    """Create a robust requests session with retry mechanism"""
    session = requests.Session()
    retries = Retry(
        total=3,
        backoff_factor=0.1,
        status_forcelist=[500, 502, 503, 504]
    )
    session.mount('https://', HTTPAdapter(max_retries=retries))
    return session


async def get_etf_info(ticker):
    try:
        # Fetch ETF data
        stock = yf.Ticker(ticker)

        # Get current price
        current_price = stock.history(period='1d')['Close'].iloc[-1]

        # Calculate weekly performance
        weekly_data = stock.history(period='5d')
        week_ago_price = weekly_data['Close'].iloc[0]
        weekly_change_percent = ((current_price - week_ago_price) / week_ago_price) * 100

        # Prepare message
        message = f"📊 {ticker} ETF Update:\n"
        message += f"Current Price: ${current_price:.2f}\n"
        message += f"Weekly Change: {weekly_change_percent:.2f}%"

        logging.info(f"Successfully retrieved data for {ticker}")
        return message

    except Exception as e:
        logging.error(f"Error fetching data for {ticker}: {str(e)}")
        return f"Error fetching data for {ticker}: {str(e)}"


async def send_telegram_message(bot, chat_id, message):
    try:
        # Use a robust session for sending messages
        session = create_robust_session()

        # Send message with custom session
        await bot.send_message(
            chat_id=chat_id,
            text=message,
            request_timeout=10
        )

        logging.info("Telegram message sent successfully")

    except Exception as e:
        logging.error(f"Error sending Telegram message: {str(e)}")

        # Fallback method: use requests directly
        try:
            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
            payload = {
                'chat_id': chat_id,
                'text': message
            }
            response = requests.post(url, data=payload, timeout=10)
            response.raise_for_status()
            logging.info("Message sent via fallback method")

        except Exception as fallback_error:
            logging.error(f"Fallback method failed: {str(fallback_error)}")


async def main():
    try:
        # Validate environment variables before proceeding
        validate_env_vars()

        # Initialize Telegram Bot
        bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)

        # Collect ETF information
        etf_messages = []
        for etf in ETFS:
            etf_info = await get_etf_info(etf)
            etf_messages.append(etf_info)

        # Combine messages
        final_message = "\n\n".join(etf_messages)

        # Send message to Telegram
        await send_telegram_message(bot, TELEGRAM_CHAT_ID, final_message)

    except Exception as e:
        logging.error(f"Main process error: {str(e)}")


# Advanced Scheduling Option
def run_scheduler():
    import schedule
    import time

    def job():
        asyncio.run(main())

    # Schedule multiple times for redundancy
    schedule.every().day.at("09:00").do(job)
    schedule.every().day.at("12:00").do(job)
    schedule.every().day.at("16:30").do(job)

    logging.info("Scheduler started")
    while True:
        schedule.run_pending()
        time.sleep(1)


# Run the script
if __name__ == '__main__':
    try:
        # Option 1: Run once
        asyncio.run(main())

        # Option 2: Run with scheduler
        # run_scheduler()

    except Exception as e:
        logging.error(f"Script execution error: {str(e)}")