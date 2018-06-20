import pytest
from unittest.mock import patch

from tohsaka.tohsaka import Tohsaka

class TestTohsaka:

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
        tohsaka = Tohsaka('test')
        tohsaka.config = {
            'spell': {
                'type': spell_type,
                'options': {}
            }
        }
        tohsaka.load_spell('test')

        assert callable(tohsaka.spell.go)


    @pytest.mark.parametrize('outputter_type', [
        'json'
    ])
    @patch('tohsaka.tohsaka.Tohsaka.__init__', return_value=None)
    def test_load_outputter(self, __init__, outputter_type):
        tohsaka = Tohsaka('test')
        tohsaka.config = {
            'outputter': {
                'type': outputter_type,
                'options': {}
            }
        }
        tohsaka.load_outputter()

        assert callable(tohsaka.outputter.go)