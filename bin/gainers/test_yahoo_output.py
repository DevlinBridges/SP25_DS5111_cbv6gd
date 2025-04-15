"""
Test script to download Yahoo gainers and verify output.
"""

from .yahoo import GainerDownloadYahoo

def test_download():
    downloader = GainerDownloadYahoo()
    downloader.download("test_yahoo_output.csv")

if __name__ == "__main__":
    test_download()
