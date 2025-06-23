import time
import yfinance as yf
import requests
from json.decoder import JSONDecodeError


def set_user_agent():
    # Create a session with custom headers
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36'
    })
    return session


def fetch_ticker_info(ticker_symbol, retries=5):
    session = set_user_agent()  # Get the session with the custom user agent
    ticker = yf.Ticker(ticker_symbol, session=session)  # Use the custom session

    wait_time = 2  # Initial wait time in seconds

    for attempt in range(retries):
        try:
            info = ticker.info
            return info  # Return the info if successful
        except JSONDecodeError:
            print("JSON Decode Error encountered. Retrying...")
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                print(f"Received 429 Too Many Requests. Waiting {wait_time} seconds before retrying...")
                time.sleep(wait_time)
                wait_time *= 2  # Exponential backoff
            else:
                print(f"HTTP error encountered: {e}. Retrying...")
        except Exception as e:
            print(f"An unexpected error has occurred: {e}. Retrying...")

        time.sleep(wait_time)  # General wait time before retrying

    raise Exception("Failed to fetch data after multiple attempts.")


# Example usage
if __name__ == "__main__":
    try:
        ticker_info = fetch_ticker_info('JEPI')
        print(ticker_info)
    except Exception as e:
        print(e)
