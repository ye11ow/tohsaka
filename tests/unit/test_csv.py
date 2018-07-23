import tempfile
from os.path import join as pathjoin
from unittest.mock import patch
from outputters.csv import Outputter

class TestCSV:

    def test_add_item(self):
        outputter = Outputter({
            'filename': 'test'
        })

        outputter._add_item({
            'title': '123',
            'description': '345',
            'link': 'link'
        })

        assert len(outputter.data) == 1

    @patch('outputters.csv.open')
    def test_output_default(self, open):
        outputter = Outputter({
            'filename': 'test'
        })

        outputter._output()

        assert open.called
