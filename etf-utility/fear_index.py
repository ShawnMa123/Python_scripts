import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup


def get_fear_greed_index():
    """Scrapes the CNN Fear & Greed Index from their website."""
    url = "https://www.cnn.com/markets/fear-and-greed"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise an exception for bad status codes
        soup = BeautifulSoup(response.content, "html.parser")
        index_value_element = soup.find("div", class_="market-fng-gauge__meter-value")
        if index_value_element:
            index_value = int(index_value_element.text)
            return index_value
        else:
            print("Could not find Fear and Greed index on the CNN website. The website structure may have changed.")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Fear & Greed Index: {e}")
        return None
    except (ValueError, TypeError) as e:
        print(f"Error parsing Fear & Greed Index: {e}")
        return None


def get_historical_fear_greed(start_date, end_date):
    """Placeholder for fetching historical Fear & Greed data.
       Since CNN doesn't readily provide historical data, this returns None."""
    print("Historical Fear & Greed data is not readily available from CNN. This will show a straight line.")
    dates = pd.date_range(start=start_date, end=end_date)
    return pd.Series(50, index=dates)  # Returns a neutral value for all dates.


def plot_data(start_date, end_date):
    """Fetches stock, USD, and China A50 data and plots it."""
    tickers = ["^GSPC", "^IXIC", "DX-Y.NYB", "000001.SS"]  # S&P 500, NASDAQ, USD Index, China A50 (SSE Composite)
    data = yf.download(tickers, start=start_date, end=end_date)['Adj Close']

    if data.empty:
        print("No stock, USD, or China A50 data was downloaded. Please check the tickers and date range.")
        return

    fear_greed = get_historical_fear_greed(start_date, end_date)
    if fear_greed is None:
        return

    fig, ax1 = plt.subplots(figsize=(16, 8))

    # Plot stock data
    ax1.plot(data.index, data["^GSPC"], label="S&P 500", color="blue")
    ax1.plot(data.index, data["^IXIC"], label="NASDAQ", color="orange")
    ax1.plot(data.index, data["000001.SS"], label="China A50", color="purple")  # Plot China A50
    ax1.set_xlabel("Date")
    ax1.set_ylabel("Adjusted Close Price", color="black")
    ax1.tick_params(axis='y', labelcolor='black')
    ax1.legend(loc='upper left')

    # Plot USD Index on a secondary y-axis
    ax2 = ax1.twinx()
    ax2.plot(data.index, data["DX-Y.NYB"], label="USD Index (DXY)", color="green", linestyle="--")
    ax2.set_ylabel("USD Index", color="green")
    ax2.tick_params(axis='y', labelcolor='green')
    ax2.legend(loc='upper center')

    # # Plot Fear & Greed on a tertiary y-axis
    # ax3 = ax1.twinx()
    # ax3.spines.right.set_position(("outward", 60))
    # ax3.plot(fear_greed.index, fear_greed, label="Fear & Greed (Constant 50)", color="red", linestyle=":")
    # ax3.set_ylabel("Fear & Greed Index", color="red")
    # ax3.tick_params(axis='y', labelcolor='red')
    # ax3.set_ylim(0, 100)
    # ax3.legend(loc="upper right")

    plt.title("S&P 500, NASDAQ, USD Index, China A50")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    end_date = datetime.now()
    start_date = end_date - timedelta(days=10 * 365)  # 10 years ago

    plot_data(start_date, end_date)
