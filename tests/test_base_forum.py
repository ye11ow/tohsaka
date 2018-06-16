from requests_html import HTML
from tohsaka.spells.forum import BaseForumSpell
from unittest.mock import patch
from .utils.utils import load_html

class DummyR(object):
    def __init__(self, html):
        self._html = html

    @property
    def html(self):
        return self._html


class TestForum:

    @patch('tohsaka.spells.forum.HTMLSession')
    @patch('tohsaka.spells.forum.BaseForumSpell.process_item', return_value=True)
    def test_go_page(self, process_item, HTMLSession):
        html = HTML(html=load_html('basepage'))
        HTMLSession.return_value.get.return_value = DummyR(html)

        spell = BaseForumSpell({
            'itemListSelector': '#unselect'
        })
        result = spell._go_page('test_url')

        for item in result:
            assert item

        assert True
