from requests_html import HTML
from tohsaka.spells.forum import Spell
from unittest.mock import patch
from unittest.mock import MagicMock
from .utils.utils import load_html

class DummyResponse(object):
    def __init__(self, html, status_code=200):
        self._html = html
        self._status_code = status_code

    @property
    def html(self):
        return self._html

    @property
    def status_code(self):
        return self._status_code

class DummyItem(object):
    def __init__(self, html):
        self._html = html

    @property
    def html(self):
        return self._html

class TestForum:

    @patch('tohsaka.spells.forum.HTMLSession')
    @patch('tohsaka.spells.forum.Spell.process_item', return_value=True)
    def test_go_page(self, process_item, HTMLSession):
        html = HTML(html=load_html('basepage'))
        HTMLSession.return_value.get.return_value = DummyResponse(html)

        spell = Spell({
            'itemListSelector': '#unselect'
        })
        result = spell._go_page('test_url')

        for item in result:
            assert item

        assert True


    @patch('tohsaka.spells.forum.HTMLSession')
    def test_process_item(self, HTMLSession):
        html = HTML(html=load_html('basepage'))
        HTMLSession.return_value.get.return_value = DummyResponse(html)

        spell = Spell({
            'titleSelector': '.title',
            'dateSelector': '.date',
            'contentSelector': '.description'
        })

        item = MagicMock()
        item.absolute_links = ['test']
        result = spell.process_item(item)

        assert result['title'] == 'title'
        assert result['pubDate'] == 'date'
        assert result['description'] == '<div class="description">description</div>'
        assert result['link'] == 'test'
        assert result['addition'] == None

    @patch('tohsaka.spells.forum.HTMLSession')
    def test_process_item_wrong_selector(self, HTMLSession):
        html = HTML(html=load_html('basepage'))
        HTMLSession.return_value.get.return_value = DummyResponse(html)

        spell = Spell({
            'titleSelector': '.wrongtitle',
            'dateSelector': '.wrongdate',
            'contentSelector': '.wrongdescription'
        })

        item = MagicMock()
        item.absolute_links = ['test']
        result = spell.process_item(item)

        assert result == {}


    def test_process_item_more_links(self):
        item = MagicMock()
        item.absolute_links = ['test', 'lin']

        spell = Spell({})
        result = spell.process_item(item)

        assert result == None