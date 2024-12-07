import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
from datetime import datetime, timedelta

# 下载特斯拉股票数据
start = '2018-01-01'
end = '2024-09-23'
ticker = 'QQQM'
data = yf.download(ticker, start=start, end=end)

# # 每月15号定投
# investment_dates = pd.date_range(start=start, end=end, freq='MS') + pd.DateOffset(days=14)
# investment_dates = [date for date in investment_dates if date in data.index]

# Weekly
investment_dates = pd.date_range(start=start, end=end, freq='W-TUE')  # Adjust 'W-FRI' to your desired day
investment_dates = [date for date in investment_dates if date in data.index]

# 定投金额
monthly_investment = 50

# 初始化投资组合
portfolio_value = []
net_investment = []
shares = 0

# 回测定投策略
for i, date in enumerate(investment_dates):
    # 计算购买的股票数量
    price = data.loc[date]['Close']
    shares_bought = monthly_investment / price
    shares += shares_bought

    # 计算当前投资组合的价值
    current_value = shares * price
    portfolio_value.append(current_value)

    # 计算净投入
    net_investment.append((i+1) * monthly_investment)



# 创建净值曲线 DataFrame
portfolio_df = pd.DataFrame({
    'Date': investment_dates,
    'Portfolio Value': portfolio_value,
    'Net Investment': net_investment
})
portfolio_df.set_index('Date', inplace=True)

# 绘制净值曲线和净投入曲线
plt.figure(figsize=(10, 6))
plt.plot(portfolio_df.index, portfolio_df['Portfolio Value'], label='Portfolio Value')
plt.plot(portfolio_df.index, portfolio_df['Net Investment'], label='Net Investment', linestyle='--')
plt.title(f'DCA Portfolio Value for {ticker}')
plt.xlabel('Date')
plt.ylabel('Value in USD')
plt.grid(True)
plt.legend()
plt.show()

