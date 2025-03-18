import pytest
from bin.gainers.factory import GainerFactory
from bin.gainers.yahoo import GainerDownloadYahoo, GainerProcessYahoo
from bin.gainers.wsj import GainerDownloadWSJ, GainerProcessWSJ


def test_gainer_factory_yahoo():
    factory = GainerFactory("yahoo")
    downloader = factory.get_downloader()
    processor = factory.get_processor()

    assert isinstance(downloader, GainerDownloadYahoo)
    assert isinstance(processor, GainerProcessYahoo)


def test_gainer_factory_wsj():
    factory = GainerFactory("wsj")
    downloader = factory.get_downloader()
    processor = factory.get_processor()

    assert isinstance(downloader, GainerDownloadWSJ)
    assert isinstance(processor, GainerProcessWSJ)


def test_gainer_factory_invalid_choice():
    with pytest.raises(AssertionError, match="Unrecognized gainer type"):
        GainerFactory("invalid")
