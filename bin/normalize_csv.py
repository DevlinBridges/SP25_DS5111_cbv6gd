import csv
import os
import sys
import re

"""
normalize_csv.py

This script normalizes stock market data from a raw CSV file into a clean, standardized format.

Usage:
    python bin/normalize_csv.py <path_to_raw_csv>

Output:
    A new CSV file with '_norm' appended to the filename.
"""


def extract_price_details(price_str):
    """Extracts the actual price, price change, and percentage change from a formatted string."""
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
        price_change = match.group(2).replace(",", "").strip() if match.group(2) else "0"
        price_percent_change = match.group(3).strip() if match.lastindex == 3 and match.group(3) else "0"
        return price, price_change, price_percent_change

    return price_str, "0", "0"


def get_normalized_headers(reader):
    """Reads and normalizes headers from the CSV file."""
    raw_headers = next(reader)

    if raw_headers[0] == "":
        raw_headers = raw_headers[1:]

    raw_headers = [col.strip().lower().replace(" ", "_") for col in raw_headers]

    header_mapping = {
        "symbol": "symbol",
        "price": "price",
        "change": "price_change",
        "change_%": "price_percent_change",
    }

    return [header_mapping.get(h, h) for h in raw_headers]


def process_row(row):
    """Processes a single row of stock market data and extracts relevant fields."""
    if len(row) >= 5:
        symbol = row[0].strip()
        # Combine price, change, and percent change for consistent parsing
        raw_price = f"{row[2].strip()} {row[3].strip()} ({row[4].strip()})"
        price, price_change, price_percent_change = extract_price_details(raw_price)
        return {
            "symbol": symbol,
            "price": price,
            "price_change": price_change,
            "price_percent_change": price_percent_change,
        }
    return None


def normalize_csv(input_file):
    """Normalizes a CSV file containing raw stock market data into a clean, standardized format."""
    assert os.path.isfile(input_file), f"❌ File not found: {input_file}"

    expected_headers = ["symbol", "price", "price_change", "price_percent_change"]
    base_name, ext = os.path.splitext(input_file)
    output_file = f"{base_name}_norm{ext}"

    with open(input_file, newline="", encoding="utf-8") as infile:
        reader = csv.reader(infile)
        _ = get_normalized_headers(reader)

        with open(output_file, "w", newline="", encoding="utf-8") as outfile:
            writer = csv.DictWriter(outfile, fieldnames=expected_headers)
            writer.writeheader()
            rows_written = 0

            for row in reader:
                try:
                    result = process_row(row)
                    if not result:
                        continue

                    if result["price"] in ("", "0"):
                        print(f"⚠️ Skipping row due to invalid price: {row}")
                        continue

                    writer.writerow(result)
                    rows_written += 1
                except Exception as e:
                    print(f"⚠️ Skipping row due to error: {row} -> {e}")
                    continue

            if rows_written == 0:
                print("⚠️ No valid rows were processed.")

    print(f"✅ Normalized file created: {output_file}")
    return output_file


if __name__ == "__main__":
    assert len(sys.argv) == 2, "Usage: python bin/normalize_csv.py <path to raw gainers csv>"
    input_path = sys.argv[1]
    normalize_csv(input_path)
