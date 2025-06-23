from datetime import date, datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt
from longport.openapi import QuoteContext, Config, Period, AdjustType, Market
from concurrent.futures import ThreadPoolExecutor, as_completed
import time


def get_trading_days(start_date, end_date, chunk_size=365):
    """
    Retrieves all trading days within the specified date range.
    Splits the date range into smaller chunks to avoid exceeding API limits.
    """
    ctx = QuoteContext(Config.from_env())  # Initialize QuoteContext
    trading_days = []

    current_start = start_date
    while current_start < end_date:
        # Define the end of the current chunk
        current_end = current_start + timedelta(days=chunk_size)
        if current_end > end_date:
            current_end = end_date

        # Fetch trading days for the current chunk
        try:
            chunk = ctx.trading_days(Market.US, current_start, current_end)
            trading_days.extend([date.fromisoformat(day) for day in chunk])
        except Exception as e:
            print(f"Error fetching trading days for {current_start} to {current_end}: {e}")

        # Move to the next chunk
        current_start = current_end + timedelta(days=1)

    return trading_days


def get_price_on_date(ticker, target_date):
    """
    Retrieves the closing price of a stock on a specific date using QuoteContext.
    """
    ctx = QuoteContext(Config.from_env())  # Initialize QuoteContext
    candlesticks = ctx.history_candlesticks_by_date(
        symbol=ticker,
        period=Period.Day,  # Daily candlesticks
        adjust_type=AdjustType.NoAdjust,  # No adjustment
        start=target_date,
        end=target_date,
    )
    if candlesticks:
        return float(candlesticks[0].close)  # Convert Decimal to float
    else:
        print(f"No data found for {ticker} on {target_date}.")
        return None


def fetch_prices_concurrently(ticker, dates):
    """
    Fetches prices for multiple dates concurrently using ThreadPoolExecutor.
    Respects the API rate limits: no more than 5 concurrent requests and no more than 10 requests per second.
    """
    prices = {}
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = []
        for i, date in enumerate(dates):
            # Throttle to ensure no more than 10 requests per second
            if i % 10 == 0 and i != 0:
                time.sleep(1)  # Wait 1 second after every 10 requests
            future = executor.submit(get_price_on_date, ticker, date)
            futures.append((date, future))

        for date, future in futures:
            try:
                prices[date] = future.result()
            except Exception as e:
                print(f"Error fetching price for {date}: {e}")
                prices[date] = None

    return prices


def calculate_dca_returns(ticker, start_date, end_date, weekly_investment, transaction_fee):
    """
    Calculates and plots the returns of a Dollar-Cost Averaging (DCA) investment strategy,
    including yearly and total returns.
    """
    # Convert start_date and end_date strings to datetime.date objects
    start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

    # Get all trading days within the date range
    trading_days = get_trading_days(start_date, end_date)

    # Filter for weekly investment dates (every Tuesday)
    investment_dates = [day for day in trading_days if day.weekday() == 1]  # Tuesday = 1
    investment_dates_str = [day.strftime('%Y-%m-%d') for day in investment_dates]

    # Fetch prices for all trading dates concurrently
    prices = fetch_prices_concurrently(ticker, investment_dates_str)

    portfolio_value = []
    net_investment = []
    shares = 0

    for date in investment_dates_str:
        price = prices.get(date)
        if price is None:
            print(f"Skipping investment on {date} due to missing data.")
            continue

        available_investment = weekly_investment - transaction_fee
        shares_bought = available_investment / price
        shares += shares_bought
        current_value = shares * price
        portfolio_value.append(current_value)
        net_investment.append((len(portfolio_value)) * weekly_investment)

    if not portfolio_value:
        print("No investment dates found within the given range.")
        return None

    portfolio_df = pd.DataFrame({
        'Date': investment_dates,
        'Portfolio Value': portfolio_value,
        'Net Investment': net_investment
    })
    portfolio_df.set_index('Date', inplace=True)

    portfolio_df['Year'] = portfolio_df.index.year
    yearly_returns = portfolio_df.groupby('Year').agg(
        StartingValue=('Portfolio Value', 'first'),
        EndingValue=('Portfolio Value', 'last'),
        TotalInvested=('Net Investment', 'last')
    )

    yearly_returns['PreviousTotalInvested'] = yearly_returns['TotalInvested'].shift(1).fillna(0)
    yearly_returns['YearlyInvested'] = yearly_returns['TotalInvested'] - yearly_returns['PreviousTotalInvested']
    yearly_returns['YearlyReturn'] = (yearly_returns['EndingValue'] - yearly_returns['StartingValue'] - yearly_returns['YearlyInvested'])
    yearly_returns['YearlyReturnRate'] = (yearly_returns['YearlyReturn'] / (yearly_returns['StartingValue'] + yearly_returns['YearlyInvested'])) * 100

    total_investment = portfolio_df['Net Investment'].iloc[-1]
    final_portfolio_value = portfolio_df['Portfolio Value'].iloc[-1]
    total_return = final_portfolio_value - total_investment
    total_return_rate = (total_return / total_investment) * 100 if total_investment != 0 else 0

    print("\nYearly Returns:")
    print(yearly_returns[['YearlyReturn', 'YearlyReturnRate']])
    print(f"\nTotal Return: ${total_return:.2f}")
    print(f"Total Return Rate: {total_return_rate:.2f}%")

    plt.figure(figsize=(12, 8))
    plt.plot(portfolio_df.index, portfolio_df['Portfolio Value'], label='Portfolio Value')
    plt.plot(portfolio_df.index, portfolio_df['Net Investment'], label='Net Investment', linestyle='--')
    plt.title(f'DCA Portfolio Value for {ticker} (Incl. Fee, Total Return: {total_return_rate:.2f}%)')
    plt.xlabel('Date')
    plt.ylabel('Value in USD')
    plt.grid(True)
    plt.legend()

    for year, row in yearly_returns.iterrows():
        plt.annotate(f"{row['YearlyReturnRate']:.1f}%",
                     xy=(pd.Timestamp(f'{year}-12-31'), row['EndingValue']),
                     xytext=(5, 5), textcoords='offset points')

    plt.show()
    return yearly_returns


# Example usage:
ticker = 'TSLA.US'  # Use the appropriate ticker format for your API
start_date = '2020-01-01'
end_date = '2020-09-23'
weekly_investment = 50
transaction_fee = 0.35

yearly_returns_df = calculate_dca_returns(ticker, start_date, end_date, weekly_investment, transaction_fee)

if yearly_returns_df is not None:  # Check if the function returned a DataFrame
    print("\nYearly Returns DataFrame:")
    print(yearly_returns_df)
