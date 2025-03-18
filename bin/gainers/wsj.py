"""
This module contains implementations of Wall Street Journal gainers downloader and processor.
"""

# pylint: disable=too-few-public-methods

import csv
import os
from datetime import datetime
from .base import GainerDownload, GainerProcess


class GainerDownloadWSJ(GainerDownload):
    """Handles downloading WSJ gainers data from the Wall Street Journal."""

    def __init__(self):
        """Initializes with the WSJ gainers URL."""
        super().__init__("https://www.wsj.com/market-data/stocks/us/gainers")

    def download(self):
        """Prints a message simulating downloading WSJ gainers data."""
        print("Downloading WSJ gainers data from:", self.url)


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
                symbol = row[1].strip()
                price, price_change, price_percent_change = self.extract_price_details(
                    row[4].strip()
                )
                if price:
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
        print(f"Saved WSJ normalized data to {output_file}")
