#!/usr/bin/env python3

import csv
import os
import sys
import re

def extract_number(value):
    """Extracts the first numerical value from a string"""
    match = re.search(r"[-+]?\d*\.?\d+", value)
    return match.group() if match else "0"

def normalize_csv(input_file):
    """Reads  raw stock market data CSV and outputs normalized version with standardized headers."""
    
    assert os.path.isfile(input_file), f"File not found: {input_file}"

    expected_headers = ["symbol", "price", "price_change", "price_percent_change"]

    ## Create output file name with '_norm' suffix
    base_name, ext = os.path.splitext(input_file)
    output_file = f"{base_name}_norm{ext}"

    with open(input_file, newline='', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        
        ## Read the first row (headers)
        raw_headers = next(reader)

        ## Handle CSVs that have an empty first column
        if raw_headers[0] == "":
            raw_headers = raw_headers[1:]  ## Remove the empty first column

        ## Normalize column names
        raw_headers = [col.strip().lower().replace(" ", "_") for col in raw_headers]

        print(f"DEBUG: Detected Headers - {raw_headers}")  ## <-- PRINT HEADERS FOR DEBUGGING

        ## Define  mapping for different header names
        header_mapping = {
            "symbol": "symbol",
            "price": "price",
            "change": "price_change",  ## Maps 'Change' to 'price_change'
            "change_%": "price_percent_change",  ## Maps 'Change %' to 'price_percent_change'
        }

        ## Convert headers using mapping
        normalized_headers = [header_mapping.get(h, h) for h in raw_headers]

        print(f"DEBUG: Normalized Headers - {normalized_headers}")  ## <-- PRINT NORMALIZED HEADERS

        ## Ensure all expected headers exist
        missing_headers = [h for h in expected_headers if h not in normalized_headers]
        assert not missing_headers, f"Missing expected headers: {missing_headers}"

        ## Reopen file as DictReader with corrected headers
        infile.seek(0)
        reader = csv.DictReader(infile, fieldnames=raw_headers)

        with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=expected_headers)
            writer.writeheader()

            next(reader)  ## Skip original header row

            for row in reader:
                normalized_row = {
                    "symbol": row.get("symbol", "").strip(),
                    "price": row.get("price", "").strip(),
                    "price_change": extract_number(row.get("change", "")),  ## Extract numeric value
                    "price_percent_change": extract_number(row.get("change_%", "")),  ## Extract numeric value
                }
                writer.writerow(normalized_row)

    print(f"✅ Normalized file created: {output_file}")
    return output_file

if __name__ == "__main__":
    assert len(sys.argv) == 2, "Usage: python bin/normalize_csv.py <path to raw gainers csv>"
    
    input_path = sys.argv[1]
    normalize_csv(input_path)
