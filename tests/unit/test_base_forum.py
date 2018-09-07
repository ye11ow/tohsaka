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

class DummyLink:
    def __init__(self, links):
        self._links = links

    @property
    def absolute_links(self):
        return self._links

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
        HTMLSession.return_value.get.return_value = DummyResponse(html)

        spell = self._create_spell({
            'titleSelector': '.title',
            'dateSelector': '.date',
            'contentSelector': '.description'
        })

        item = DummyLink(['test_link'])


        result = spell.process_item(item)

        assert result['title'] == 'title'
        assert result['pubDate'] == 'date'
        assert result['description'] == '<div class="description">description</div>'
        assert result['link'] == 'test_link'
        assert result['addition'] is None


    def test_process_item_duplicated_link(self):
        spell = self._create_spell({
        })

        item = DummyLink(['test_link', 'test_link2'])

        result = spell.process_item(item)

        assert result == {}

    @patch('spells.forum.HTMLSession')
    def test_process_item_wrong_selector(self, HTMLSession):
        html = HTML(html=load_html('basepage'))
        HTMLSession.return_value.get.return_value = DummyResponse(html)

        spell = self._create_spell({
            'titleSelector': '.wrongtitle',
            'dateSelector': '.wrongdate',
            'contentSelector': '.wrongdescription'
        })

        item = DummyLink(['test_link'])

        result = spell.process_item(item)

        assert result == {}

    @patch('spells.forum.HTMLSession')
    def test_go(self, HTMLSession):
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
    def test_go_multi_page(self, HTMLSession):
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
