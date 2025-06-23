import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf

def calculate_dca_returns(ticker, start_date, end_date, weekly_investment, transaction_fee):
    """
    Calculates and plots the returns of a Dollar-Cost Averaging (DCA) investment strategy,
    including yearly and total returns, and plots the ticker's closing price.

    Args:
        ticker (str): The stock ticker symbol (e.g., "VOO").
        start_date (str): The start date for the investment period (e.g., "2018-01-01").
        end_date (str): The end date for the investment period (e.g., "2024-09-23").
        weekly_investment (float): The amount to invest each week.
        transaction_fee (float): The transaction fee per purchase.

    Returns:
        pandas.DataFrame or None: DataFrame containing yearly returns, or None if an error occurs.
    """
    try:
        data = yf.download(ticker, start=start_date, end=end_date)
        if data.empty:
            raise ValueError(f"No data found for ticker {ticker}")
    except Exception as e:
        print(f"Error downloading data: {e}")
        return None

    investment_dates = pd.date_range(start=start_date, end=end_date, freq='W-TUE')
    investment_dates = [date for date in investment_dates if date in data.index]

    portfolio_value = []
    net_investment = []
    shares = 0

    for i, date in enumerate(investment_dates):
        available_investment = weekly_investment - transaction_fee
        price = data.loc[date]['Close'].item()
        if price == 0:
            print(f"Warning: Price is zero on {date}. Skipping investment.")
            continue
        shares_bought = available_investment / price
        shares += shares_bought
        current_value = shares * price
        portfolio_value.append(current_value)
        net_investment.append((i + 1) * weekly_investment)

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

    # Plot ticker close price
    plt.plot(data['Close'], label=f'{ticker} Close Price', alpha=0.5, linestyle=':')

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
ticker = 'VOO'
start_date = '2018-01-01'
end_date = '2024-09-23'
weekly_investment = 50
transaction_fee = 0.35

yearly_returns_df = calculate_dca_returns(ticker, start_date, end_date, weekly_investment, transaction_fee)

if yearly_returns_df is not None:
    print("\nYearly Returns DataFrame:")
    print(yearly_returns_df)