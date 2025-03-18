import sys
from bin.gainers.factory import GainerFactory

class ProcessGainer:
    def __init__(self, gainer_downloader, gainer_normalizer, input_file, output_file):
        self.downloader = gainer_downloader
        self.normalizer = gainer_normalizer
        self.input_file = input_file
        self.output_file = output_file

    def _download(self):
        self.downloader.download()

    def _normalize(self):
        return self.normalizer.normalize(self.input_file)

    def _save_to_file(self, normalized_data):
        self.normalizer.save_with_timestamp(normalized_data, self.output_file)

    def process(self):
        self._download()
        normalized_data = self._normalize()
        self._save_to_file(normalized_data)

if __name__ == "__main__":
    assert len(sys.argv) == 4, "Usage: python get_gainer.py <yahoo/wsj> <input_file> <output_file>"
    choice, input_file, output_file = sys.argv[1], sys.argv[2], sys.argv[3]

    factory = GainerFactory(choice)
    downloader = factory.get_downloader()
    normalizer = factory.get_processor()
    
    runner = ProcessGainer(downloader, normalizer, input_file, output_file)
    runner.process()
