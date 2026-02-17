import requests
from producer.config import logger, headers, url

def connect_to_api(symbol="IBM"):
    params = {
        "function": "TIME_SERIES_INTRADAY",
        "symbol": symbol,
        "interval": "5min",
        "outputsize": "compact",
        "datatype": "json"
    }

    r = requests.get(url, headers=headers, params=params, timeout=15)
    r.raise_for_status()
    return r.json()

def parse_time_series(ts_dict, sym, records):
    for date_str, metrics in ts_dict.items():
        if not isinstance(metrics, dict):
            continue
        records.append({
            "date": date_str,
            "symbol": sym,
            "open":  metrics.get("1. open"),
            "high":  metrics.get("2. high"),
            "low":   metrics.get("3. low"),
            "close": metrics.get("4. close"),
        })

def extract_json(response, symbol="IBM"):
    records = []

    # API limit / error detection
    if isinstance(response, dict) and ("Note" in response or "Information" in response or "Error Message" in response):
        print("API limit or error:", response)
        return []

    # Normal AlphaVantage-style dict
    if isinstance(response, dict) and "Time Series (5min)" in response:
        sym = response.get("Meta Data", {}).get("2. Symbol", symbol)
        ts = response.get("Time Series (5min)", {})
        if isinstance(ts, dict):
            parse_time_series(ts, sym, records)
        return records

    # If response is already the time-series dict
    if isinstance(response, dict):
        parse_time_series(response, symbol, records)
        return records

    return []