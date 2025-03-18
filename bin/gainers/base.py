from abc import ABC, abstractmethod
import re

# DOWNLOADER (Abstract)
class GainerDownload(ABC):
    def __init__(self, url):
        self.url = url

    @abstractmethod
    def download(self):
        pass

# PROCESSOR (Abstract)
class GainerProcess(ABC):
    @abstractmethod
    def normalize(self, input_file):
        pass

    @abstractmethod
    def save_with_timestamp(self, normalized_data, output_file):
        pass

    def extract_price_details(self, price_str):
        if not price_str or price_str.strip() == "":
            return "", "", ""

        price_str = re.sub(r"\(N/A\)", "", price_str).strip()

        if "(" in price_str and ")" in price_str:
            match = re.match(
                r"([\d,.]+)\s*([+-][\d,.]+)?\s*\(\s*([+-]?\d*\.?\d+)%\s*\)?", price_str,
            )
        else:
            match = re.match(r"([\d,.]+)\s*([+-][\d,.]+)?", price_str)

        if match:
            price = re.sub(r"[^\d.]", "", match.group(1))
            price_change = match.group(2).replace(",", "").strip() if match.group(2) else "0"
            price_percent_change = match.group(3).strip() if match.lastindex == 3 and match.group(3) else "0"

            return price, price_change, price_percent_change

        return price_str, "0", "0"
