from .wsj import GainerDownloadWSJ

def test_download():
    downloader = GainerDownloadWSJ()
    downloader.download("test_wsj_output.csv")

if __name__ == "__main__":
    test_download()
