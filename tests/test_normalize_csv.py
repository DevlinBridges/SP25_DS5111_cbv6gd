import sys
sys.path.append('.')

import os
import pytest
import csv
from bin.normalize_csv import extract_price_details, normalize_csv

# -----------------------
#  TESTS FOR extract_price_details FUNCTION
# -----------------------

@pytest.mark.parametrize(
    "price_str, expected",
    [
        # Basic cases
        ("100 +2 (1.5%)", ("100", "+2", "1.5")),
        ("200 -3 (2.1%)", ("200", "-3", "2.1")),
        ("150 (0.0%)", ("150", "0", "0.0")),

        # Edge cases
        ("", ("", "", "")),  # Empty string
        ("NaN", ("NaN", "0", "0")),  # Invalid numeric
        ("300 (N/A)", ("300", "0", "0")),  # No percentage
        ("350 +5", ("350", "+5", "0")),  # No percentage in parentheses
    ],
)
def test_extract_price_details(price_str, expected):
    assert extract_price_details(price_str) == expected


# -----------------------
#  TEST FIXTURE: SAMPLE CSV FOR UNIT TESTING
# -----------------------

@pytest.fixture
def sample_csv(tmp_path):
    """Creates a sample raw stock CSV file for testing."""
    test_file = tmp_path / "test_input.csv"
    with open(test_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Symbol", "Price", "Change", "Change %"])  # Clean headers
        writer.writerow(["AAPL", "150 +2 (1.5%)", "+2", "1.5%"])  # Valid row
        writer.writerow(["GOOGL", "2800 -5 (0.8%)", "-5", "0.8%"])  # Valid row
        writer.writerow(["AMZN", "NaN", "", ""])  # Malformed row

    return test_file
