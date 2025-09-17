# get_stock_ticker_tool.py

import requests
from langchain.tools import tool

@tool("get_stock_ticker", return_direct=True)
def get_stock_ticker(company_name: str) -> str:
    """
    Get the stock ticker symbol for a given company name using Yahoo Finance search API.

    Args:
        company_name (str): The full name of the company (e.g., "Apple Inc").

    Returns:
        str: The stock ticker symbol (e.g., "AAPL").
    """
    try:
        url = "https://query2.finance.yahoo.com/v1/finance/search"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
        }
        params = {
            "q": company_name,
            "quotes_count": 1,
            "country": "United States"
        }

        response = requests.get(url=url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()

        # Extract ticker symbol
        ticker = data["quotes"][0]["symbol"]
        return ticker

    except Exception as e:
        return f"ERROR: Could not fetch ticker for '{company_name}'. Details: {str(e)}"
