import tempfile
from os.path import join as pathjoin
from unittest.mock import patch
from outputters.json import Outputter

class TestJSON:

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

    @patch('outputters.json.open')
    def test_output(self, open):
        outputter = Outputter({
            'filename': 'test'
        })

        outputter._output()

        assert open.called