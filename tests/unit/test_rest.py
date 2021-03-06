from unittest.mock import patch

from spells.rest import Spell

from utils.dummy import DummyResponse

class TestRestSpell:

    ENDPOINT = 'http://www.google.com'

    def test_name(self):
        name = Spell.name()

        assert type(name) == str
        assert len(name) > 0

    def test_intro(self):
        name = Spell.intro()

        assert type(name) == str
        assert len(name) > 0

    @patch('spells.rest.requests')
    def test_go(self, requests):
        requests.get.return_value = DummyResponse('', 200)

        rest = Spell({
            'endpoint': self.ENDPOINT
        })

        results = rest.go()

        for item in results:
            assert item

        requests.get.assert_called_once_with(self.ENDPOINT, headers=rest.get_headers())


    @patch('spells.rest.requests')
    def test_go_failed(self, requests):
        requests.get.return_value = DummyResponse('', 404)

        rest = Spell({
            'endpoint': self.ENDPOINT
        })

        results = rest.go()

        for item in results:
            assert not item

        requests.get.assert_called_once_with(self.ENDPOINT, headers=rest.get_headers())