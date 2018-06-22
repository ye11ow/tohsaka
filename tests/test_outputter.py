from pytest import mark

from tohsaka.outputters.base_outputter import BaseOutputter

class DummyOutputter(BaseOutputter):

    REQUIRED_FIELDS = ['has1', 'has2']

    def _output(self, item):
        return True

    def done(self):
        pass

class TestBaseOutputter:

    @mark.parametrize('item,valid', [
        ({'has1': 1, 'has2': 1}, True),
        ({'has1': 1}, False),
        ({'has1': 1, 'has2': 1, 'has3': 1}, True),
        ({'has1': 1, 'has3': 1}, False),
        ({}, False),
        ({'has1': None, 'has2': None}, True),
    ])
    def test_go(self, item, valid):
        outputter = DummyOutputter({})

        result = outputter.go(item)

        assert valid == result