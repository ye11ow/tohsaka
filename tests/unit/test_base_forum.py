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
    @patch('spells.forum.Spell.process_item', return_value=True)
    def test_go_page(self, process_item, HTMLSession):
        html = HTML(html=load_html('basepage'))
        HTMLSession.return_value.get.return_value = DummyResponse(html)

        spell = self._create_spell({
            'itemListSelector': '#unselect'
        })
        result = spell._go_page('test_url')

        for item in result:
            assert item

        assert True


    @patch('spells.forum.HTMLSession')
    @patch('spells.forum.Spell._dedup', return_value=False)
    def test_go_page_failed_response(self, _dedup, HTMLSession):
        HTMLSession.return_value.get.return_value = DummyResponse('', 404)

        spell = self._create_spell()

        result = spell._go_page('test_url')

        for item in result:
            assert item is None

    @patch('spells.forum.HTMLSession')
    @patch('spells.forum.Spell._dedup', return_value=True)
    def test_go_page_dedupped(self, _dedup, HTMLSession):
        html = HTML(html=load_html('basepage'))
        HTMLSession.return_value.get.return_value = DummyResponse(html)

        spell = self._create_spell({
            'titleSelector': '.title',
            'dateSelector': '.date',
            'contentSelector': '.description'
        })

        item = MagicMock()
        item.absolute_links = ['test']
        result = spell.process_item(item)

        assert result == {}


    @patch('spells.forum.HTMLSession')
    @patch('spells.forum.Spell._dedup', return_value=False)
    def test_process_item(self, _dedup, HTMLSession):
        html = HTML(html=load_html('basepage'))
        HTMLSession.return_value.get.return_value = DummyResponse(html)

        spell = self._create_spell({
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

    @patch('spells.forum.HTMLSession')
    @patch('spells.forum.Spell._dedup', return_value=False)
    def test_process_item_wrong_selector(self, _dedup, HTMLSession):
        html = HTML(html=load_html('basepage'))
        HTMLSession.return_value.get.return_value = DummyResponse(html)

        spell = self._create_spell({
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

        spell = self._create_spell()
        result = spell.process_item(item)

        assert result == None


    @patch('spells.forum.Spell._go_page', return_value=['RESULT'])
    def test_go_single_page(self, _go_page):
        spell = Spell({
            'entry': 'http://localhost/index'
        })

        result = spell.go()

        for item in result:
            assert item == 'RESULT'


    @patch('spells.forum.Spell._go_page', return_value=['RESULT'])
    def test_go_multi_page(self, _go_page):
        PAGES = 2

        spell = self._create_spell({
            'page_param': 'page',
            'pages': PAGES
        })

        result = spell.go()

        for item in result:
            assert item == 'RESULT'

        assert _go_page.call_count == PAGES