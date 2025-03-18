
import csv
import os
import sys
import re

"""
normalize_csv.py

This script normalizes stock market data from a raw CSV file into a clean, standardized format.

Features:
- Extracts and cleans price values, price changes, and percentage changes.
- Handles cases with missing price change percentages.
- Removes rows with missing or invalid data.
- Ensures the output CSV file has the expected headers.

Usage:
    python bin/normalize_csv.py <path_to_raw_csv>

Example:
    python bin/normalize_csv.py data/raw_gainers.csv

Output:
    A new CSV file with '_norm' appended to the filename, e.g., `data/raw_gainers_norm.csv`
"""

def extract_price_details(price_str):
    """Extracts the actual price, price change, and percentage change from a formatted string."""
    if not price_str or price_str.strip() == "":
        return "", "", ""

    # Remove placeholders like (N/A)
    price_str = re.sub(r"\(N/A\)", "", price_str).strip()

    # Check if parentheses exist, meaning a percentage is included
    if "(" in price_str and ")" in price_str:
        match = re.match(
            r"([\d,.]+)\s*([+-][\d,.]+)?\s*\(\s*([+-]?\d*\.?\d+)%\s*\)?",
            price_str,
        )
    else:
        # Handle cases where percentage is missing
        match = re.match(r"([\d,.]+)\s*([+-][\d,.]+)?", price_str)

    if match:
        price = re.sub(r"[^\d.]", "", match.group(1))  # Extract and clean price
        price_change = (
            match.group(2).replace(",", "").strip() if match.group(2) else "0"
        )
        price_percent_change = (
            match.group(3).strip() if match.lastindex == 3 and match.group(3) else "0"
        )

        return price, price_change, price_percent_change

    return price_str, "0", "0"  # Default return if parsing fails


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
    symbol = row[1].strip()
    raw_price = row[4].strip()
    price, price_change, price_percent_change = extract_price_details(raw_price)

    return {
        "symbol": symbol,
        "price": price,
        "price_change": price_change,
        "price_percent_change": price_percent_change,
    }


def normalize_csv(input_file):
    """Normalizes a CSV file containing raw stock market data into a clean, standardized format."""
    assert os.path.isfile(input_file), f"❌ File not found: {input_file}"

    expected_headers = ["symbol", "price", "price_change", "price_percent_change"]

    # Create output file name with '_norm' suffix
    base_name, ext = os.path.splitext(input_file)
    output_file = f"{base_name}_norm{ext}"

    with open(input_file, newline="", encoding="utf-8") as infile:
        reader = csv.reader(infile)
        _ = get_normalized_headers(reader)

        with open(output_file, "w", newline="", encoding="utf-8") as outfile:
            writer = csv.DictWriter(outfile, fieldnames=expected_headers)
            writer.writeheader()

            rows_written = 0  # Track how many rows are written

            for row in reader:
                if row[0] == "":
                    row = row[1:]

                try:
                    processed_row = process_row(row)

                    # Skip rows with invalid data (empty strings or defaults like '0')
                    if processed_row["price"] in ("", "0"):
                        print(f"⚠️ Skipping row due to invalid data: {row}")
                        continue  # Skip invalid rows

                    writer.writerow(processed_row)
                    rows_written += 1
                except IndexError:
                    print(f"⚠️ Skipping malformed row: {row}")
                    continue

            if rows_written == 0:
                print("⚠️ No valid rows were processed.")

    # Reopen output file before returning (fixes test failure)
    with open(output_file, "r", encoding="utf-8") as f:
        _ = f.readlines()

    print(f"✅ Normalized file created: {output_file}")
    return output_file


if __name__ == "__main__":
    """Main entry point for running the script from the command line."""
    assert (
        len(sys.argv) == 2
    ), "Usage: python bin/normalize_csv.py <path to raw gainers csv>"

    input_path = sys.argv[1]
    normalize_csv(input_path)
