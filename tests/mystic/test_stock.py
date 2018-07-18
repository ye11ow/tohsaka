import tempfile
import json
from os.path import join as pathjoin
from tohsaka import Tohsaka
from utils.file_util import load_json

class TestStock:

    def test_stock(self):
        FILENAME = 'aapl'
        tohsaka = Tohsaka('stock', {
            'symbol': 'aapl',
            'output_file': FILENAME
        })

        tohsaka.outputter.OUTPUT_FOLDER = tempfile.gettempdir()
        tohsaka.go()

        result = load_json(pathjoin(tohsaka.outputter.OUTPUT_FOLDER, FILENAME + '.json'))

        assert result
        assert 'symbol' in result[0]
        assert 'latestPrice' in result[0]