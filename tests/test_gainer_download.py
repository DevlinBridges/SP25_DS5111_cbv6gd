import pytest
from bin.gainers.yahoo import GainerDownloadYahoo
from bin.gainers.wsj import GainerDownloadWSJ
import os

def test_gainer_download_yahoo(capsys, tmp_path):
    yahoo_downloader = GainerDownloadYahoo()
    output_file = tmp_path / "yahoo_test.csv"
    yahoo_downloader.download(str(output_file))

    captured = capsys.readouterr()
    assert "Fetching Yahoo gainers from API" in captured.out
    assert output_file.exists()

@pytest.mark.skipif(os.getenv("CI") == "true", reason="Chrome not available in GitHub Actions")
def test_gainer_download_wsj(capsys, tmp_path):
    wsj_downloader = GainerDownloadWSJ()
    output_file = tmp_path / "wsj_test.csv"
    wsj_downloader.download(str(output_file))

    captured = capsys.readouterr()
    assert "Downloading WSJ gainers data" in captured.out
    assert output_file.exists()
