import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf


def calculate_dca_returns(ticker, start_date, end_date, weekly_investment, transaction_fee):
    """
    Calculates and plots the returns of a Dollar-Cost Averaging (DCA) investment strategy.

    Args:
        ticker (str): The stock ticker symbol (e.g., "VOO").
        start_date (str): The start date for the investment period (e.g., "2018-01-01").
        end_date (str): The end date for the investment period (e.g., "2024-09-23").
        weekly_investment (float): The amount to invest each week.
        transaction_fee (float): The transaction fee per purchase.

    Returns:
        None. Displays the plot and prints the total return and return rate.
    """
    try:
        data = yf.download(ticker, start=start_date, end=end_date)
        if data.empty:
            raise ValueError(f"No data found for ticker {ticker}")
    except Exception as e:
        print(f"Error downloading data: {e}")
        return

    investment_dates = pd.date_range(start=start_date, end=end_date, freq='W-TUE')
    investment_dates = [date for date in investment_dates if date in data.index]

    portfolio_value = []
    net_investment = []
    shares = 0

    for i, date in enumerate(investment_dates):
        available_investment = weekly_investment - transaction_fee

        # Handle zero price using .item()
        price = data.loc[date]['Close'].item()  # Get the actual value from the Series
        if price == 0:
            print(f"Warning: Price is zero on {date}. Skipping investment.")
            continue

        shares_bought = available_investment / price
        shares += shares_bought

        current_value = shares * price
        portfolio_value.append(current_value)

        net_investment.append((i + 1) * weekly_investment)

    if not portfolio_value:  # check if portfolio value is empty
        print("No investment dates found within the given range.")
        return

    # Calculate total return
    total_investment = net_investment[-1] if isinstance(net_investment, list) else net_investment.iloc[-1]
    final_portfolio_value = portfolio_value[-1] if isinstance(portfolio_value, list) else portfolio_value.iloc[-1]

    total_return = final_portfolio_value - total_investment
    total_return_rate = (total_return / total_investment) * 100 if total_investment != 0 else 0

    if isinstance(total_return, pd.Series):
        total_return = total_return.item()
    if isinstance(total_return_rate, pd.Series):
        total_return_rate = total_return_rate.item()

    print(f"Total Return: ${total_return:.2f}")
    print(f"Total Return Rate: {total_return_rate:.2f}%")

    # Create DataFrame for plotting
    portfolio_df = pd.DataFrame({
        'Date': investment_dates,
        'Portfolio Value': portfolio_value,
        'Net Investment': net_investment
    })
    portfolio_df.set_index('Date', inplace=True)

    plt.figure(figsize=(10, 6))
    plt.plot(portfolio_df.index, portfolio_df['Portfolio Value'], label='Portfolio Value')
    plt.plot(portfolio_df.index, portfolio_df['Net Investment'], label='Net Investment', linestyle='--')
    plt.title(f'DCA Portfolio Value for {ticker} (Incl. Fee, Return: {total_return_rate:.2f}%)')
    plt.xlabel('Date')
    plt.ylabel('Value in USD')
    plt.grid(True)
    plt.legend()
    plt.show()


# Example usage:
ticker = 'QQQM'
start_date = '2018-01-01'
end_date = '2024-11-23'
weekly_investment = 50

calculate_dca_returns(ticker,start_date,end_date,weekly_investment,0.35)