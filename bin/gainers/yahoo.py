"""
This module contains implementations of Yahoo gainers downloader and processor.
"""

import csv
import os
from datetime import datetime
from .base import GainerDownload, GainerProcess


class GainerDownloadYahoo(GainerDownload):
    """Handles downloading Yahoo gainers data from the Yahoo Finance website."""
    # Suppress the warning because this class only needs one method
    # pylint: disable=too-few-public-methods

    def __init__(self):
        super().__init__("https://finance.yahoo.com/gainers")

    def download(self):
        """Simulates downloading Yahoo gainers data."""
        print("Downloading Yahoo gainers data from:", self.url)


class GainerProcessYahoo(GainerProcess):
    """Processes and normalizes Yahoo gainers data."""

    def normalize(self, input_file):
        """Reads and normalizes Yahoo gainers CSV data.

        Args:
            input_file (str): Path to the CSV file.

        Returns:
            list: Normalized data as a list of lists.
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
        """Saves the normalized data with a timestamp.

        Args:
            normalized_data (list): The processed data.
            output_file (str): The base name of the output file.
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"{output_file}_yahoo_{timestamp}.csv"
        with open(output_file, "w", newline="", encoding="utf-8") as outfile:
            writer = csv.writer(outfile)
            writer.writerow(["symbol", "price", "price_change", "price_percent_change"])
            writer.writerows(normalized_data)
        print(f"Saved Yahoo normalized data to {output_file}")
