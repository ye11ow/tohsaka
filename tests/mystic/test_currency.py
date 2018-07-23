import tempfile
import csv
from os.path import join as pathjoin
from tohsaka import Tohsaka


class TestCurrency:

    def test_currency(self):
        FILENAME = 'currency'
        tohsaka = Tohsaka('currency', {
            'from': 'USD',
            'to': 'CNY',
            'output_file': FILENAME
        })

        tohsaka.outputter.OUTPUT_FOLDER = tempfile.gettempdir()
        tohsaka.go()

        with open(pathjoin(tohsaka.outputter.OUTPUT_FOLDER, FILENAME + '.csv'), 'r') as csvfile:
            assert csv.Sniffer().has_header(csvfile.read(1024))