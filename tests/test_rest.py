from tohsaka.spells.rest import Spell

class TestRestSpell:

    def test_name(self):
        name = Spell.name()

        assert type(name) == str
        assert len(name) > 0

    def test_intro(self):
        name = Spell.intro()

        assert type(name) == str
        assert len(name) > 0