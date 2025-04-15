"""
This module contains implementations of Wall Street Journal gainers downloader and processor.
"""

# pylint: disable=too-few-public-methods

import csv
import os
import re
import time
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from .base import GainerDownload, GainerProcess


class GainerDownloadWSJ(GainerDownload):
    """Handles downloading WSJ gainers data from the Wall Street Journal."""

    def __init__(self):
        super().__init__("https://www.wsj.com/market-data/stocks/us/movers")

    def download(self, output_file):
        """Downloads WSJ gainers data using Selenium and saves it to a CSV file."""
        print("Downloading WSJ gainers data using Selenium...")

        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.binary_location = "/snap/chromium/current/usr/lib/chromium-browser/chrome"

        driver = webdriver.Chrome(service=Service(), options=options)
        driver.get(self.url)
        time.sleep(5)  # Let JavaScript render the content
        soup = BeautifulSoup(driver.page_source, "html.parser")
        driver.quit()

        tables = soup.find_all("table")
        if not tables:
            print("⚠️ No tables found on WSJ page.")
            return

        with open(output_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Symbol", "Name", "Last Price", "Change", "Change %"])

            for table in tables:
                rows = table.find_all("tr")
                for row in rows[1:]:
                    cols = row.find_all("td")
                    if len(cols) >= 5:
                        name_with_symbol = cols[0].get_text(strip=True)
                        volume = cols[1].get_text(strip=True)
                        last_price = cols[2].get_text(strip=True)
                        change = cols[3].get_text(strip=True)
                        change_percent = cols[4].get_text(strip=True)

                        match = re.search(r'\(([^)]+)\)', name_with_symbol)
                        symbol = match.group(1) if match else name_with_symbol

                        writer.writerow([symbol, name_with_symbol, last_price, change, change_percent])

        print(f"✅ Saved WSJ data to {output_file}")


class GainerProcessWSJ(GainerProcess):
    """Processes and normalizes WSJ gainers CSV data."""

    def normalize(self, input_file):
        """Reads and normalizes WSJ gainers CSV data.

        Args:
            input_file (str): Path to the CSV file.

        Returns:
            list: A list of lists containing symbol, price, price change, and price percent change.
        """
        assert os.path.isfile(input_file), f"File not found: {input_file}"
        normalized_data = []

        with open(input_file, newline="", encoding="utf-8") as infile:
            reader = csv.reader(infile)
            next(reader)

            for row in reader:
                if len(row) < 5:
                    continue
                symbol = row[0].strip()
                price = row[2].strip().replace(",", "")
                price_change = row[3].strip().replace(",", "")
                price_percent_change = row[4].strip().replace("%", "").strip()

                if price and price != "0":
                    normalized_data.append(
                        [symbol, price, price_change, price_percent_change]
                    )
        return normalized_data

    def save_with_timestamp(self, normalized_data, output_file):
        """Saves normalized data with a timestamped filename.

        Args:
            normalized_data (list): Processed stock gainers data.
            output_file (str): Base name of the output CSV file.
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"{output_file}_wsj_{timestamp}.csv"
        with open(output_file, "w", newline="", encoding="utf-8") as outfile:
            writer = csv.writer(outfile)
            writer.writerow(["symbol", "price", "price_change", "price_percent_change"])
            writer.writerows(normalized_data)
        print(f"📄 Saved WSJ normalized data to {output_file}")
