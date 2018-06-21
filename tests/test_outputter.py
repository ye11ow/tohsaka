from pytest import mark

from tohsaka.outputters.base_outputter import BaseOutputter

class DummyOutputter(BaseOutputter):

    REQUIRED_FIELDS = ['has1', 'has2']

    def _output(self, item):
        return True

    def done(self):
        pass

class TestBaseOutputter:

    def test_replace_params(self):
        outputter = DummyOutputter({
            'config1': 'no param',
            'config2': '<<param1>>',
            'config3': '<<param2>>123',
            'config4': '<<param1>>456<<param2>>'
        }, {
            'param1': '1marap',
            'param2': '2marap'
        })

        assert outputter.config.get('config1') == 'no param'
        assert outputter.config.get('config2') == '1marap'
        assert outputter.config.get('config3') == '2marap123'
        assert outputter.config.get('config4') == '1marap4562marap'

    @mark.parametrize('item,valid', [
        ({'has1': 1, 'has2': 1}, True),
        ({'has1': 1}, False),
        ({'has1': 1, 'has2': 1, 'has3': 1}, True),
        ({'has1': 1, 'has3': 1}, False),
        ({}, False),
        ({'has1': None, 'has2': None}, True),
    ])
    def test_go(self, item, valid):
        outputter = DummyOutputter({}, {})

        result = outputter.go(item)

        assert valid == result