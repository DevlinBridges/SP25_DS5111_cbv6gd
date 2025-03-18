"""
Base module defining abstract classes for downloading and processing stock gainers data.
"""

from abc import ABC, abstractmethod
import re

# pylint: disable=too-few-public-methods

# DOWNLOADER (Abstract)
class GainerDownload(ABC):
    """Abstract class for downloading stock gainers data."""

    def __init__(self, url):
        """Initializes GainerDownload with the provided URL.

        Args:
            url (str): The URL from which to download stock gainers data.
        """
        self.url = url

    @abstractmethod
    def download(self):
        """Abstract method to download stock gainers data."""
        raise NotImplementedError("Subclasses must implement the download method")


# PROCESSOR (Abstract)
class GainerProcess(ABC):
    """Abstract class for processing stock gainers data."""

    @abstractmethod
    def normalize(self, input_file):
        """Abstract method to normalize stock gainers data from the input file.

        Args:
            input_file (str): Path to the CSV file containing raw stock gainers data.
        """
        raise NotImplementedError("Subclasses must implement the normalize method")

    @abstractmethod
    def save_with_timestamp(self, normalized_data, output_file):
        """Abstract method to save processed data with a timestamp.

        Args:
            normalized_data (list): List of processed stock data.
            output_file (str): File path where the output should be saved.
        """
        raise NotImplementedError("Subclasses must implement the save_with_timestamp method")

    def extract_price_details(self, price_str):
        """Extracts price details from a given string.

        Args:
            price_str (str): Raw price string containing price, price change, and percent change.

        Returns:
            tuple: (price, price change, price percent change) as strings.
        """
        if not price_str or price_str.strip() == "":
            return "", "", ""

        price_str = re.sub(r"\(N/A\)", "", price_str).strip()

        if "(" in price_str and ")" in price_str:
            match = re.match(
                r"([\d,.]+)\s*([+-][\d,.]+)?\s*\(\s*([+-]?\d*\.?\d+)%\s*\)?",
                price_str,
            )
        else:
            match = re.match(r"([\d,.]+)\s*([+-][\d,.]+)?", price_str)

        if match:
            price = re.sub(r"[^\d.]", "", match.group(1))
            price_change = (
                match.group(2).replace(",", "").strip() if match.group(2) else "0"
            )
            price_percent_change = (
                match.group(3).strip()
                if match.lastindex == 3 and match.group(3)
                else "0"
            )

            return price, price_change, price_percent_change

        return price_str, "0", "0"
