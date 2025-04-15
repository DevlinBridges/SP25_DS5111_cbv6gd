"""
This module contains implementations of Yahoo gainers downloader and processor.
"""

import csv
import os
import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from .base import GainerDownload, GainerProcess


class GainerDownloadYahoo(GainerDownload):
    """Handles downloading Yahoo gainers data from Yahoo Finance."""

    def __init__(self):
        super().__init__("https://finance.yahoo.com/gainers")

    def download(self, output_file):
        """Downloads Yahoo gainers data using requests and saves it to a CSV file."""
        print("📡 Downloading Yahoo gainers data from:", self.url)

        headers = {
            "User-Agent": (
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36"
            )
        }

        response = requests.get(self.url, headers=headers)
        if response.status_code != 200:
            print("❌ Failed to fetch data from Yahoo Finance.")
            return

        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find("table")
        if not table:
            print("❌ Could not find the gainers table on Yahoo page.")
            return

        rows = table.find_all("tr")
        if not rows:
            print("⚠️ Table found, but no rows.")
            return

        with open(output_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Symbol", "Name", "Last Price", "Change", "Change %"])

            for row in rows[1:]:
                cols = row.find_all("td")
                if len(cols) >= 5:
                    symbol = cols[0].get_text(strip=True)
                    name = cols[1].get_text(strip=True)
                    last_price = cols[2].get_text(strip=True)
                    change = cols[3].get_text(strip=True)
                    change_percent = cols[4].get_text(strip=True)
                    writer.writerow([symbol, name, last_price, change, change_percent])

        print(f"✅ Saved Yahoo data to {output_file}")


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
