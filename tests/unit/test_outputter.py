from pytest import mark
from unittest.mock import patch

from tohsaka.outputters.base_outputter import BaseOutputter

class DummyOutputter(BaseOutputter):

    REQUIRED_FIELDS = ['has1', 'has2']

    def _output(self):
        return True

    def _add_item(self, item):
        return True


class TestBaseOutputter:

    @mark.parametrize('item,valid', [
        ({'has1': 1, 'has2': 1}, True),
        ({'has1': 1}, False),
        ({'has1': 1, 'has2': 1, 'has3': 1}, True),
        ({'has1': 1, 'has3': 1}, False),
        ({}, False),
        ({'has1': None, 'has2': None}, True),
    ])

    def test_go_and_valid(self, item, valid):
        outputter = DummyOutputter({})

        result = outputter.go(item)

        assert valid == result

    @patch('tohsaka.outputters.base_outputter.os.path.isdir', return_value=False)
    @patch('tohsaka.outputters.base_outputter.os.makedirs')
    def test_done(self, makedirs, isdir):
        outputter = DummyOutputter({})

        result = outputter.done()

        makedirs.assert_called_once()
        assert result