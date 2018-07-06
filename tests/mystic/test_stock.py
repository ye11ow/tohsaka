import tempfile
import json
from os.path import join as pathjoin
from tohsaka.tohsaka import Tohsaka

class TestStock:

    def test_stock(self):
        FILENAME = 'aapl'
        tohsaka = Tohsaka('stock', {
            'symbol': 'aapl',
            'output_file': FILENAME
        })

        tohsaka.outputter.OUTPUT_FOLDER = tempfile.gettempdir()
        tohsaka.go()


        with open(pathjoin(tohsaka.outputter.OUTPUT_FOLDER, FILENAME + '.json'), 'r') as json_file:
            result = json.loads(json_file.read())

        assert result
        assert 'symbol' in result[0]
        assert 'latestPrice' in result[0]