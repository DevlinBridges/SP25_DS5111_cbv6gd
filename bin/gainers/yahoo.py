"""
This module contains implementations of Yahoo gainers downloader and processor.
"""

import csv
import os
import requests
from datetime import datetime
from .base import GainerDownload, GainerProcess


class GainerDownloadYahoo(GainerDownload):
    """Handles downloading Yahoo gainers data using the Screener API."""

    def __init__(self):
        super().__init__("https://query1.finance.yahoo.com/v1/finance/screener/predefined/saved")

    def download(self, output_file):
        """Fetches top gainers via Yahoo's screener API and writes to a CSV."""
        print("📡 Fetching Yahoo gainers from API...")

        params = {"scrIds": "day_gainers", "count": "100"}
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(self.url, headers=headers, params=params)
        if response.status_code != 200:
            print("❌ Failed to fetch data from Yahoo Finance API.")
            return

        data = response.json()
        quotes = data.get("finance", {}).get("result", [])[0].get("quotes", [])

        if not quotes:
            print("⚠️ No gainers found in API response.")
            return

        with open(output_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Symbol", "Name", "Last Price", "Change", "Change %"])
            for q in quotes:
                writer.writerow([
                    q.get("symbol", ""),
                    q.get("shortName", ""),
                    q.get("regularMarketPrice", ""),
                    q.get("regularMarketChange", ""),
                    q.get("regularMarketChangePercent", ""),
                ])

        print(f"✅ Yahoo gainer data saved to {output_file}")


class GainerProcessYahoo(GainerProcess):
    """Processes and normalizes Yahoo gainers data."""

    def normalize(self, input_file):
        assert os.path.isfile(input_file), f"File not found: {input_file}"
        normalized_data = []

        with open(input_file, newline="", encoding="utf-8") as infile:
            reader = csv.reader(infile)
            next(reader)  # Skip header

            for row in reader:
                if len(row) < 5:
                    continue

                symbol = row[0].strip()
                price = row[2].strip().replace(",", "")
                price_change = row[3].strip().replace(",", "").replace("+", "")
                price_percent_change = row[4].strip().replace("%", "").replace("+", "")

                if price and price != "0":
                    normalized_data.append([
                        symbol,
                        price,
                        price_change if price_change else "0",
                        price_percent_change if price_percent_change else "0",
                    ])

        return normalized_data

    def save_with_timestamp(self, normalized_data, output_file):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"{output_file}_yahoo_{timestamp}.csv"
        with open(output_file, "w", newline="", encoding="utf-8") as outfile:
            writer = csv.writer(outfile)
            writer.writerow(["symbol", "price", "price_change", "price_percent_change"])
            writer.writerows(normalized_data)
        print(f"📁 Saved Yahoo normalized data to {output_file}")
