import pytest
from unittest.mock import patch

from tohsaka.tohsaka import Tohsaka

class TestTohsaka:

    BASE_PARAMS = {
        'params': {
            'key1': {
                'required': True
            },
            'key2': {
                'required': False
            },
            'key3': {
                'required': True
            },
        }
    }

    def test_list_spells(self):
        spells = Tohsaka.list_spells()

        for spell in spells:
            for prop in ['name', 'intro']:
                assert type(spell[prop]) == str
                assert len(spell[prop]) > 0


    @pytest.mark.parametrize('spell_type', [
        'forum',
        'rest'
    ])
    @patch('tohsaka.tohsaka.Tohsaka.__init__', return_value=None)
    def test_load_spell(self, __init__, spell_type):
        tohsaka = Tohsaka('test', {})
        tohsaka.config = {
            'spell': {
                'type': spell_type,
                'options': {}
            }
        }
        tohsaka.spell = tohsaka._load_module('Spell', 'test', tohsaka.SPELL_PATH, {})

        assert hasattr(tohsaka, 'spell')
        assert callable(tohsaka.spell.go)


    @pytest.mark.parametrize('outputter_type', [
        'json'
    ])
    @patch('tohsaka.tohsaka.Tohsaka.__init__', return_value=None)
    def test_load_outputter(self, __init__, outputter_type):
        tohsaka = Tohsaka('test', {})
        tohsaka.config = {
            'outputter': {
                'type': outputter_type,
                'options': {}
            }
        }

        tohsaka.outputter = tohsaka._load_module('Outputter', 'test', tohsaka.OUTPUTTER_PATH, {})

        assert hasattr(tohsaka, 'outputter')
        assert callable(tohsaka.outputter.go)

    @patch('tohsaka.tohsaka.Tohsaka.__init__', return_value=None)
    def test_replace_params(self, __init__):
        tohsaka = Tohsaka('test', {})

        tohsaka.config = {
            'spell': {
                'options': {
                    'config1': 'no param',
                    'config2': '<<param1>>',
                    'config3': '<<param2>>123',
                    'config4': '<<param1>>456<<param2>>'
                }
            }
        }

        tohsaka._replace_params(tohsaka.config['spell']['options'], {
            'param1': '1marap',
            'param2': '2marap',
            'param3': '3marap'
        })

        options = tohsaka.config.get('spell').get('options')

        assert options.get('config1') == 'no param'
        assert options.get('config2') == '1marap'
        assert options.get('config3') == '2marap123'
        assert options.get('config4') == '1marap4562marap'


    @patch('tohsaka.tohsaka.Tohsaka.__init__', return_value=None)
    def test_validate_params(self, __init__):
        tohsaka = Tohsaka('test', {})
        tohsaka.config = self.BASE_PARAMS

        result1 = tohsaka._validate_params({
            'key1': '1',
            'key2': '2',
            'key3': '3'
        })

        result2 = tohsaka._validate_params({
            'key1': '1',
            'key3': '3'
        })

        result3 = tohsaka._validate_params({
            'key1': False,
            'key2': '2',
            'key3': 0
        })

        assert (result1 & result2 & result3)


    @patch('tohsaka.tohsaka.Tohsaka.__init__', return_value=None)
    def test_validate_params_invalid(self, __init__):
        tohsaka = Tohsaka('test', {})
        tohsaka.config = self.BASE_PARAMS

        with pytest.raises(Exception):
            tohsaka._validate_params({
                'key2': '2',
                'key3': '3'
            })

        with pytest.raises(Exception):
            tohsaka._validate_params({
                'key2': '1'
            })

        with pytest.raises(Exception):
            tohsaka._validate_params({
                'key4': 0
            })
