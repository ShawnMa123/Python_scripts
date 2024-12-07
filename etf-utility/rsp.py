import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt


def rsp_calculator(start_date, end_date, investment_amount, investment_day):
    # Fetch historical data
    qqqm_data = yf.download('QQQM', start=start_date, end=end_date)
    voo_data = yf.download('VOO', start=start_date, end=end_date)

    # Check if data was fetched correctly
    if qqqm_data.empty or voo_data.empty:
        print("Error: No historical data available for one or both ETFs.")
        return

    # Combine the dataframes and align by date
    df = pd.concat([qqqm_data['Adj Close'], voo_data['Adj Close']], axis=1, join='inner').dropna().sort_index()
    df.columns = ['QQQM', 'VOO']

    # Calculate weekly returns
    df['QQQM_Return'] = df['QQQM'].pct_change()
    df['VOO_Return'] = df['VOO'].pct_change()

    # Filter for investment days (Tuesdays)
    df = df[df.index.weekday == investment_day]

    # Initial values
    qqqm_shares = 0
    voo_shares = 0
    total_investment = 0

    # Simulation
    for date, row in df.iterrows():
        if qqqm_shares == 0:
            qqqm_shares = investment_amount / row['QQQM']
        else:
            qqqm_shares *= (1 + row['QQQM_Return'])
            qqqm_shares += (investment_amount / row['QQQM'])

        if voo_shares == 0:
            voo_shares = investment_amount / row['VOO']
        else:
            voo_shares *= (1 + row['VOO_Return'])
            voo_shares += (investment_amount / row['VOO'])

        total_investment += 2 * investment_amount  # Investing in both ETFs

    # Final value calculation
    final_qqqm_value = qqqm_shares * df['QQQM'].iloc[-1]
    final_voo_value = voo_shares * df['VOO'].iloc[-1]
    total_value = final_qqqm_value + final_voo_value

    # Print results
    print(f"Total Investment: ${total_investment:.2f}")
    print(f"Final Value of QQQM: ${final_qqqm_value:.2f}")
    print(f"Final Value of VOO: ${final_voo_value:.2f}")
    print(f"Total Final Value: ${total_value:.2f}")
    print(f"Total Return: {((total_value - total_investment) / total_investment) * 100:.2f}%")

    # Plotting
    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df['QQQM'], label='QQQM')
    plt.plot(df.index, df['VOO'], label='VOO')
    plt.title('Historical Prices of QQQM and VOO ETFs')
    plt.xlabel('Date')
    plt.ylabel('Price ($)')
    plt.legend()
    plt.show()


# Run the calculator
rsp_calculator(start_date='2010-01-01', end_date='2024-12-07', investment_amount=50, investment_day=1)
