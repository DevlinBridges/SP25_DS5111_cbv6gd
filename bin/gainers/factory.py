"""Factory module for selecting stock gainers data sources."""

# pylint: disable=too-few-public-methods

from .wsj import GainerDownloadWSJ, GainerProcessWSJ
from .yahoo import GainerDownloadYahoo, GainerProcessYahoo


class GainerFactory:
    """Factory class to create appropriate downloader and processor for stock gainers."""

    def __init__(self, choice):
        """Initializes GainerFactory with the selected source.

        Args:
            choice (str): The source type, either "yahoo" or "wsj".
        """
        assert choice in ["yahoo", "wsj"], f"Unrecognized gainer type {choice}"
        self.choice = choice

    def get_downloader(self):
        """Returns the appropriate downloader based on the selected choice.

        Returns:
            GainerDownloadYahoo or GainerDownloadWSJ: The corresponding downloader instance.
        """
        return GainerDownloadYahoo() if self.choice == "yahoo" else GainerDownloadWSJ()

    def get_processor(self):
        """Returns the appropriate processor based on the selected choice.

        Returns:
            GainerProcessYahoo or GainerProcessWSJ: The corresponding processor instance.
        """
        return GainerProcessYahoo() if self.choice == "yahoo" else GainerProcessWSJ()
