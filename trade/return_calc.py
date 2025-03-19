from datetime import date, datetime
import pandas as pd
import matplotlib.pyplot as plt
from longport.openapi import QuoteContext, Config, Period, AdjustType


def get_price_on_date(ticker, target_date):
    """
    Retrieves the closing price of a stock on a specific date using QuoteContext.
    """
    ctx = QuoteContext(Config.from_env())  # Initialize QuoteContext

    # Convert the target_date string to a datetime.date object
    target_date = datetime.strptime(target_date, '%Y-%m-%d').date()

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


def calculate_dca_returns(ticker, start_date, end_date, weekly_investment, transaction_fee):
    """
    Calculates and plots the returns of a Dollar-Cost Averaging (DCA) investment strategy,
    including yearly and total returns.

    Args:
        ticker (str): The stock ticker symbol (e.g., "VOO").
        start_date (str): The start date for the investment period (e.g., "2018-01-01").
        end_date (str): The end date for the investment period (e.g., "2024-09-23").
        weekly_investment (float): The amount to invest each week.
        transaction_fee (float): The transaction fee per purchase.

    Returns:
        pandas.DataFrame or None: DataFrame containing yearly returns, or None if an error occurs.
    """
    investment_dates = pd.date_range(start=start_date, end=end_date, freq='W-TUE')

    portfolio_value = []
    net_investment = []
    shares = 0

    for i, date in enumerate(investment_dates):
        price = get_price_on_date(ticker, date.strftime('%Y-%m-%d'))
        if price is None:
            print(f"Skipping investment on {date} due to missing data.")
            continue

        available_investment = weekly_investment - transaction_fee
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
ticker = 'BRK.B.US'  # Use the appropriate ticker format for your API
start_date = '2025-01-01'
end_date = '2025-01-23'
weekly_investment = 50
transaction_fee = 0.35

yearly_returns_df = calculate_dca_returns(ticker, start_date, end_date, weekly_investment, transaction_fee)

if yearly_returns_df is not None:  # Check if the function returned a DataFrame
    print("\nYearly Returns DataFrame:")
    print(yearly_returns_df)
