import pytest
import os
from bin.gainers.wsj import GainerDownloadWSJ

@pytest.mark.skipif(
    os.getenv("CI") == "true",
    reason="Chrome not available in GitHub Actions environment"
)
def test_download(tmp_path):
    wsj_downloader = GainerDownloadWSJ()
    output_file = tmp_path / "wsj_test.csv"
    wsj_downloader.download(str(output_file))

    assert output_file.exists()
