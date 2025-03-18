import pytest
from bin.gainers.yahoo import GainerDownloadYahoo
from bin.gainers.wsj import GainerDownloadWSJ


def test_gainer_download_yahoo(capsys):
    yahoo_downloader = GainerDownloadYahoo()
    yahoo_downloader.download()

    captured = capsys.readouterr()
    assert "Downloading Yahoo gainers data" in captured.out


def test_gainer_download_wsj(capsys):
    wsj_downloader = GainerDownloadWSJ()
    wsj_downloader.download()

    captured = capsys.readouterr()
    assert "Downloading WSJ gainers data" in captured.out
