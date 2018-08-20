from requests_html import HTML
from spells.forum import Spell
from unittest.mock import patch
from unittest.mock import MagicMock
from utils.utils import load_html
from utils.dummy import DummyResponse

class DummyItem:
    def __init__(self, html):
        self._html = html

    @property
    def html(self):
        return self._html

class TestForum:

    def _create_spell(self, options={}):
        base = {
            'entry': 'http://localhost/index'
        }
        return Spell({**base, **options})

    def test_name(self):
        name = Spell.name()

        assert type(name) == str
        assert len(name) > 0

    def test_intro(self):
        name = Spell.intro()

        assert type(name) == str
        assert len(name) > 0

    @patch('spells.forum.HTMLSession')
    def test_get_items_from_page(self, HTMLSession):
        html = HTML(html=load_html('basepage'))
        HTMLSession.return_value.get.return_value = DummyResponse(html)

        spell = self._create_spell({
            'itemListSelector': '#unselect'
        })
        result = spell._get_items_from_page('test_url')

        for item in result:
            assert item


    @patch('spells.forum.HTMLSession')
    def test_get_items_from_page_failed_response(self, HTMLSession):
        HTMLSession.return_value.get.return_value = DummyResponse('', 404)

        spell = self._create_spell()

        result = spell._get_items_from_page('test_url')

        assert len(result) == 0


    @patch('spells.forum.HTMLSession')
    def test_process_item(self, HTMLSession):
        html = HTML(html=load_html('basepage'))
        LINK = 'test_link'
        HTMLSession.return_value.get.return_value = DummyResponse(html)

        spell = self._create_spell({
            'titleSelector': '.title',
            'dateSelector': '.date',
            'contentSelector': '.description'
        })

        result = spell.process_item(LINK)

        assert result['title'] == 'title'
        assert result['pubDate'] == 'date'
        assert result['description'] == '<div class="description">description</div>'
        assert result['link'] == LINK
        assert result['addition'] is None

    @patch('spells.forum.HTMLSession')
    def test_process_item_wrong_selector(self, HTMLSession):
        html = HTML(html=load_html('basepage'))
        HTMLSession.return_value.get.return_value = DummyResponse(html)

        spell = self._create_spell({
            'titleSelector': '.wrongtitle',
            'dateSelector': '.wrongdate',
            'contentSelector': '.wrongdescription'
        })

        result = spell.process_item('test')

        assert result == {}

    @patch('spells.forum.HTMLSession')
    @patch('spells.forum.file_util.touch', return_value=False)
    def test_go(self, touch, HTMLSession):
        html = HTML(html=load_html('basepage'))
        HTMLSession.return_value.get.return_value = DummyResponse(html)

        spell = self._create_spell({
            'itemListSelector': '#unselect',
            'titleSelector': '.title',
            'dateSelector': '.date',
            'contentSelector': '.description'
        })

        result = spell.go()

        count = 0
        for item in result:
            count += 1
            assert item

        assert count == 1

    @patch('spells.forum.HTMLSession')
    @patch('spells.forum.file_util.touch', return_value=False)
    def test_go_multi_page(self, touch, HTMLSession):
        html = HTML(html=load_html('basepage'))
        HTMLSession.return_value.get.return_value = DummyResponse(html)

        spell = self._create_spell({
            'page_param': 'page',
            'pages': '5',
            'itemListSelector': '#unselect',
            'titleSelector': '.title',
            'dateSelector': '.date',
            'contentSelector': '.description'
        })

        result = spell.go()

        count = 0
        for item in result:
            count += 1
            assert item

        assert count == 5
