from datetime import date
from longport.openapi import QuoteContext, Config, Period, AdjustType

def find_ticket_price(ticket_idx, ticket_date):
    # Initialize Config and QuoteContext
    config = Config.from_env()
    ctx = QuoteContext(config)

    # Define the symbol and date
    symbol = ticket_idx
    # target_date = ticket_date
    target_date = date(2025, 3, 12)
    target_date = date(ticket_date[0], ticket_date[1], ticket_date[2])

    # Retrieve historical candlesticks for the specific date
    candlesticks = ctx.history_candlesticks_by_date(
        symbol=symbol,
        period=Period.Day,  # Daily candlesticks
        adjust_type=AdjustType.NoAdjust,  # No adjustment
        start=target_date,
        end=target_date,
    )

    if candlesticks:
        # Extract the candlestick for the specific date
        candlestick = candlesticks[0]
        print(f"TSLA on {target_date}:")
        print(f"Open: {candlestick.open}")
        print(f"Close: {candlestick.close}")
        print(f"High: {candlestick.high}")
        print(f"Low: {candlestick.low}")
        return candlestick.close
    else:
        print(f"No data found for TSLA on {target_date}.")
        raise Exception


