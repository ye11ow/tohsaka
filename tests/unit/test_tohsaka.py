import pytest
from unittest.mock import patch
from unittest.mock import MagicMock
from copy import deepcopy

from tohsaka import Tohsaka

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

    def test_list_mystic(self):
        codes = Tohsaka.get_mystic_codes()

        for code in codes:
            for prop in ['name', 'description']:
                assert type(code[prop]) == str
                assert len(code[prop]) > 0

    @patch('tohsaka.Tohsaka.__init__', return_value=None)
    def test_load_spell(self, __init__):
        tohsaka = Tohsaka('rest', {})
        tohsaka.config = {
            'spell': {
                'type': 'rest',
                'options': {'endpoint': ''}
            }
        }
        tohsaka.spell = tohsaka._load_module('Spell', 'rest', tohsaka.SPELL_PATH, {})

        assert hasattr(tohsaka, 'spell')
        assert callable(tohsaka.spell.go)


    @pytest.mark.parametrize('outputter_type', [
        'json'
    ])
    @patch('tohsaka.Tohsaka.__init__', return_value=None)
    def test_load_outputter(self, __init__, outputter_type):
        tohsaka = Tohsaka('test', {})
        tohsaka.config = {
            'outputter': {
                'type': outputter_type,
                'options': {'endpoint': ''}
            }
        }

        tohsaka.outputter = tohsaka._load_module('Outputter', 'test', tohsaka.OUTPUTTER_PATH, {})

        assert hasattr(tohsaka, 'outputter')
        assert callable(tohsaka.outputter.go)

    @patch('tohsaka.Tohsaka.__init__', return_value=None)
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

    @patch('tohsaka.Tohsaka.__init__', return_value=None)
    def test_replace_params_boolean(self, __init__):
        tohsaka = Tohsaka('test', {})
        tohsaka.config = deepcopy({**self.BASE_PARAMS_DEF, **self.BASE_SPELL_CONFIG})

        base_params = self.BASE_PARAMS
        base_params['param4'] = True

        tohsaka._replace_params(tohsaka.config['spell']['options'], base_params)

        options = tohsaka.config.get('spell').get('options')

        assert options.get('config5') == True

    @patch('tohsaka.Tohsaka.__init__', return_value=None)
    def test_replace_params_override_default(self, __init__):
        tohsaka = Tohsaka('test', {})
        tohsaka.config = deepcopy({**self.BASE_PARAMS_DEF, **self.BASE_SPELL_CONFIG})

        base_params = self.BASE_PARAMS
        base_params['param4'] = 'param4'

        tohsaka._replace_params(tohsaka.config['spell']['options'], base_params)

        options = tohsaka.config.get('spell').get('options')

        assert options.get('config5') == 'param4'

    @patch('tohsaka.Tohsaka.__init__', return_value=None)
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


    @patch('tohsaka.Tohsaka.__init__', return_value=None)
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

    @patch('tohsaka.Qualifier')
    @patch('tohsaka.Tohsaka.__init__', return_value=None)
    def test_go_no_item(self, __init__, Qualifier):
        tohsaka = Tohsaka('test', {})
        tohsaka.config = None
        tohsaka.spell = MagicMock()
        tohsaka.spell.go.return_value = []
        tohsaka.outputter = MagicMock()

        tohsaka.go()

        Qualifier.assert_called_once()
        tohsaka.outputter.done.assert_called_once()

    @patch('tohsaka.Qualifier')
    @patch('tohsaka.Tohsaka.__init__', return_value=None)
    def test_go_has_item(self, __init__, Qualifier):
        tohsaka = Tohsaka('test', {})
        tohsaka.config = None
        tohsaka.spell = MagicMock()
        tohsaka.spell.go.return_value = [1, 2, 3, 4, 5, 6, 7, 8]
        tohsaka.outputter = MagicMock()

        tohsaka.go()

        Qualifier.assert_called_once()
        assert Qualifier.return_value.go.call_count == 8
        tohsaka.outputter.done.assert_called_once()


    @patch('tohsaka.Qualifier')
    @patch('tohsaka.Tohsaka.__init__', return_value=None)
    def test_go_has_invalid_item(self, __init__, Qualifier):
        tohsaka = Tohsaka('test', {})
        tohsaka.config = None
        tohsaka.spell = MagicMock()
        tohsaka.spell.go.return_value = [1, 2, 3, 4, {}, 6, None, 8]
        tohsaka.outputter = MagicMock()

        tohsaka.go()

        Qualifier.assert_called_once()
        assert Qualifier.return_value.go.call_count == 6
        tohsaka.outputter.done.assert_called_once()
