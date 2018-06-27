import tempfile
from os.path import join as pathjoin
from unittest.mock import patch
from tohsaka.outputters.json import Outputter

class TestJSON:

    def test_add_item(self):
        outputter = Outputter({
            'filename': 'test'
        })

        outputter.go({
            'title': '123',
            'description': '345',
            'link': 'link'
        })

        assert len(outputter.data) == 1

    @patch('tohsaka.outputters.json.open')
    @patch('tohsaka.outputters.json.os')
    def test_done_f(self, os, open):
        outputter = Outputter({
            'filename': 'test'
        })

        outputter.done()

        assert open.called