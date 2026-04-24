import requests
import json
from datetime import datetime

def fetch_stock_quote(ticker: str) -> dict:
    """
    Fetch a real-time stock quote using the Yahoo Finance unofficial API.
    No API key required.
    """
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
    params = {
        "interval": "1d",
        "range": "5d"
    }
    headers = {
        # Yahoo requires a User-Agent header or it returns 429
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()  # Raises an error for bad status codes

    data = response.json()
    meta = data["chart"]["result"][0]["meta"]

    return {
        "ticker": ticker.upper(),
        "currency": meta.get("currency"),
        "current_price": meta.get("regularMarketPrice"),
        "previous_close": meta.get("previousClose"),
        "exchange": meta.get("exchangeName"),
        "fetched_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }


def fetch_multiple(tickers: list[str]) -> list[dict]:
    results = []
    for ticker in tickers:
        try:
            quote = fetch_stock_quote(ticker)
            results.append(quote)
            print(f"✅ {quote['ticker']}: ${quote['current_price']} {quote['currency']}")
        except Exception as e:
            print(f"❌ Failed to fetch {ticker}: {e}")
    return results


if __name__ == "__main__":
    watchlist = ["AAPL", "MSFT", "TSLA", "NVDA"]

    print(f"\n📈 Fetching quotes for: {', '.join(watchlist)}\n")
    quotes = fetch_multiple(watchlist)

    # Save results to a JSON file
    output_file = "quotes.json"
    with open(output_file, "w") as f:
        json.dump(quotes, f, indent=2)

    print(f"\n💾 Results saved to {output_file}")
