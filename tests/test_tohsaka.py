from tohsaka.tohsaka import Tohsaka

class TestTohsaka:

    def test_list_spells(self):
        spells = Tohsaka.list_spells()

        for spell in spells:
            for prop in ['name', 'intro']:
                assert type(spell[prop]) == str
                assert len(spell[prop]) > 0


