#!/usr/bin/env python3

"""
normalize_csv.py

This script reads raw stock market data from a CSV file and outputs a normalized
version with standardized headers and formatted price details.

Features:
- Extracts and cleans price values, price changes, and percentage changes.
- Handles cases with missing price change percentages.
- Removes unnecessary empty columns in the input CSV.
- Ensures that all expected headers are present.
- Skips malformed rows and provides error handling.

Usage:
    python bin/normalize_csv.py <path_to_raw_csv>

Example:
    python bin/normalize_csv.py data/raw_gainers.csv

Output:
    A new CSV file with "_norm" appended to the filename, e.g., `data/raw_gainers_norm.csv`

Author: Devlin Bridges
Date: 2025-02-20
"""

import csv
import os
import sys
import re


def extract_price_details(price_str):
    """Extracts actual price, price change, and percentage change from a formatted string."""
    if not price_str or price_str.strip() == "":
        return "", "", ""

    ## ✅ Remove placeholders like (N/A)
    price_str = re.sub(r"\(N/A\)", "", price_str).strip()

    ## ✅ Check if parentheses exist, meaning a percentage is included
    if "(" in price_str and ")" in price_str:
        match = re.match(r"([\d,.]+)\s*([+-][\d,.]+)?\s*\(\s*([+-]?\d*\.?\d+)%\s*\)?", price_str)
    else:
        ## ✅ Handle cases where percentage is missing
        match = re.match(r"([\d,.]+)\s*([+-][\d,.]+)?", price_str)

    if match:
        price = re.sub(r"[^\d.]", "", match.group(1))  # ✅ Extract and clean price
        price_change = match.group(2).replace(",", "").strip() if match.group(2) else "0"
        price_percent_change = match.group(3).strip() if match.lastindex == 3 and match.group(3) else "0"

        return price, price_change, price_percent_change

    return price_str, "0", "0"  # ✅ Default return if parsing fails


def normalize_csv(input_file):
    """Reads raw stock market data CSV and outputs a normalized version with standardized headers."""

    assert os.path.isfile(input_file), f"❌ File not found: {input_file}"

    expected_headers = ["symbol", "price", "price_change", "price_percent_change"]

    ## ✅ Create output file name with '_norm' suffix
    base_name, ext = os.path.splitext(input_file)
    output_file = f"{base_name}_norm{ext}"

    with open(input_file, newline="", encoding="utf-8") as infile:
        reader = csv.reader(infile)

        ## ✅ Read and normalize headers
        raw_headers = next(reader)

        ## ✅ Remove first empty column if it exists
        if raw_headers[0] == "":
            raw_headers = raw_headers[1:]  

        ## ✅ Convert headers to lowercase and replace spaces with underscores
        raw_headers = [col.strip().lower().replace(" ", "_") for col in raw_headers]

        ## ✅ Define correct header mapping
        header_mapping = {
            "symbol": "symbol",
            "price": "price",
            "change": "price_change",
            "change_%": "price_percent_change",
        }

        ## ✅ Convert headers to expected format
        normalized_headers = [header_mapping.get(h, h) for h in raw_headers]

        ## ✅ Ensure all expected headers exist
        missing_headers = [h for h in expected_headers if h not in normalized_headers]
        assert not missing_headers, f"❌ Missing expected headers: {missing_headers}"

        ## ✅ Reopen file as DictReader with corrected headers
        infile.seek(0)
        reader = csv.reader(infile)

        ## ✅ Skip first row (headers)
        next(reader)

        with open(output_file, "w", newline="", encoding="utf-8") as outfile:
            writer = csv.DictWriter(outfile, fieldnames=expected_headers)
            writer.writeheader()

            for row in reader:
                ## ✅ Handle extra leading empty column by shifting values
                if row[0] == "":
                    row = row[1:]

                try:
                    symbol = row[1].strip()  # ✅ Symbol is at index 1
                    raw_price = row[4].strip()  # ✅ Price is at index 4 (after shifting)
                    price, price_change, price_percent_change = extract_price_details(
                        raw_price
                    )

                    normalized_row = {
                        "symbol": symbol,
                        "price": price,
                        "price_change": price_change,
                        "price_percent_change": price_percent_change,
                    }
                    writer.writerow(normalized_row)
                except IndexError:
                    print(f"⚠️ Skipping malformed row: {row}")
                    continue

    ## ✅ Reopen output file before returning (fixes test failure)
    with open(output_file, "r", encoding="utf-8") as f:
        _ = f.readlines()

    print(f"✅ Normalized file created: {output_file}")
    return output_file


if __name__ == "__main__":
    assert (
        len(sys.argv) == 2
    ), "Usage: python bin/normalize_csv.py <path to raw gainers csv>"

    input_path = sys.argv[1]
    normalize_csv(input_path)
