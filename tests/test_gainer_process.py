import pytest
import os
import csv
import glob
from bin.gainers.yahoo import GainerProcessYahoo
from bin.gainers.wsj import GainerProcessWSJ


@pytest.fixture
def yahoo_csv(tmp_path):
    """Mock Yahoo gainers CSV with realistic structure."""
    file_path = tmp_path / "test_yahoo_input.csv"
    with open(file_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Symbol", "Name", "Last Price", "Change", "Change %"])
        writer.writerow(["AAPL", "Apple Inc.", "150.00", "+1.23", "+0.82%"])
        writer.writerow(["GOOGL", "Alphabet Inc.", "2750.50", "+25.75", "+0.94%"])
    return file_path


@pytest.fixture
def wsj_csv(tmp_path):
    """Mock WSJ gainers CSV with realistic structure."""
    file_path = tmp_path / "test_wsj_input.csv"
    with open(file_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Symbol", "Name", "Last Price", "Change", "Change %"])
        writer.writerow(["MSFT", "Microsoft", "320.15", "+5.12", "+1.63%"])
        writer.writerow(["GOOGL", "Alphabet Inc.", "2750.50", "+25.75", "+0.94%"])
    return file_path


def test_gainer_process_yahoo(yahoo_csv, tmp_path):
    """Test Yahoo gainer processing and file creation."""
    processor = GainerProcessYahoo()
    normalized_data = processor.normalize(yahoo_csv)

    assert len(normalized_data) == 2
    assert normalized_data[0][0] == "AAPL"
    assert normalized_data[0][1] == "150.00"
    assert normalized_data[0][2] == "1.23"
    assert normalized_data[0][3] == "0.82"

    output_file = tmp_path / "yahoo_output.csv"
    processor.save_with_timestamp(normalized_data, output_file)

    matching_files = glob.glob(str(output_file) + "*")
    assert matching_files, f"Expected file {output_file} not found."

def test_gainer_process_wsj(wsj_csv, tmp_path):
    """Test WSJ gainer processing and file creation."""
    processor = GainerProcessWSJ()
    normalized_data = processor.normalize(wsj_csv)

    assert len(normalized_data) == 2
    assert normalized_data[1][0] == "GOOGL"
    assert normalized_data[1][1] == "2750.50"
    assert normalized_data[1][2] == "+25.75"
    assert normalized_data[1][3] == "+0.94"

    output_file = tmp_path / "wsj_output.csv"
    processor.save_with_timestamp(normalized_data, output_file)

    # Use glob to verify the presence of timestamped files
    matching_files = glob.glob(str(output_file) + "*")

    # Debugging output
    print(f"Expected output file prefix: {output_file}")
    print(f"Files in directory: {os.listdir(tmp_path)}")

    assert matching_files, f"Expected file {output_file} not found."
