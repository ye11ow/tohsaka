import pytest
from unittest.mock import patch
from copy import deepcopy

from tohsaka.tohsaka import Tohsaka

class TestTohsaka:

    BASE_PARAMS_DEF = {
        'params': {
            'param1': {
                'required': True
            },
            'param2': {
                'required': False
            },
            'param3': {
                'required': True
            },
            'param4': {
                'default': '4marap'
            }
        }
    }

    BASE_PARAMS = {
        'param1': '1marap',
        'param2': '2marap',
        'param3': '3marap'
    }

    BASE_SPELL_CONFIG = {
        'spell': {
            'options': {
                'config1': 'no param',
                'config2': '<<param1>>',
                'config3': '<<param2>>123',
                'config4': '<<param1>>456<<param2>>',
                'config5': '<<param4>>'
            }
        }
    }

    def test_list_spells(self):
        spells = Tohsaka.list_spells()

        for spell in spells:
            for prop in ['name', 'intro']:
                assert type(spell[prop]) == str
                assert len(spell[prop]) > 0

    def test_list_mystic(self):
        codes = Tohsaka.list_mystic_codes()

        for code in codes:
            for prop in ['name', 'description']:
                assert type(code[prop]) == str
                assert len(code[prop]) > 0

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
        tohsaka.config = deepcopy({**self.BASE_PARAMS_DEF, **self.BASE_SPELL_CONFIG})

        tohsaka._replace_params(tohsaka.config['spell']['options'], self.BASE_PARAMS)

        options = tohsaka.config.get('spell').get('options')

        assert options.get('config1') == 'no param'
        assert options.get('config2') == '1marap'
        assert options.get('config3') == '2marap123'
        assert options.get('config4') == '1marap4562marap'
        assert options.get('config5') == '4marap'

    @patch('tohsaka.tohsaka.Tohsaka.__init__', return_value=None)
    def test_replace_params_override_default(self, __init__):
        tohsaka = Tohsaka('test', {})
        tohsaka.config = deepcopy({**self.BASE_PARAMS_DEF, **self.BASE_SPELL_CONFIG})

        base_params = self.BASE_PARAMS
        base_params['param4'] = 'param4'

        tohsaka._replace_params(tohsaka.config['spell']['options'], base_params)

        options = tohsaka.config.get('spell').get('options')

        assert options.get('config5') == 'param4'

    @patch('tohsaka.tohsaka.Tohsaka.__init__', return_value=None)
    def test_validate_params(self, __init__):
        tohsaka = Tohsaka('test', {})
        tohsaka.config = deepcopy({**self.BASE_PARAMS_DEF, **self.BASE_SPELL_CONFIG})

        result1 = tohsaka._validate_params({
            'param1': '1',
            'param2': '2',
            'param3': '3'
        })

        result2 = tohsaka._validate_params({
            'param1': '1',
            'param3': '3'
        })

        result3 = tohsaka._validate_params({
            'param1': False,
            'param2': '2',
            'param3': 0
        })

        assert (result1 & result2 & result3)


    @patch('tohsaka.tohsaka.Tohsaka.__init__', return_value=None)
    def test_validate_params_invalid(self, __init__):
        tohsaka = Tohsaka('test', {})
        tohsaka.config = deepcopy({**self.BASE_PARAMS_DEF, **self.BASE_SPELL_CONFIG})

        with pytest.raises(Exception):
            tohsaka._validate_params({
                'param2': '2',
                'param3': '3'
            })

        with pytest.raises(Exception):
            tohsaka._validate_params({
                'param2': '1'
            })

        with pytest.raises(Exception):
            tohsaka._validate_params({
                'key4': 0
            })
