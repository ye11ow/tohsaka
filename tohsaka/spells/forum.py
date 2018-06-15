from requests_html import HTMLSession
from dateutil import parser
from datetime import datetime
import pytz
from tohsaka.spells.base_spell import Spell
from utils import log_util

logger = log_util.get_logger('tohsaka')


class BaseForumSpell(Spell):

    def __init__(self, config):
        Spell.__init__(self, config)

    @property
    def name(self):
        return 'Forum'

    @property
    def intro(self):
        return 'Get forum-like data'

    def get_date(self, element):
        return element.text

    def get_description(self, element):
        return element.html

    def get_addition(self, html):
        return None

    def _go_page(self, url):
        session = HTMLSession()
        r = session.get(url)

        items = r.html.find(self._config.get('itemListSelector'))

        logger.debug('%d items detected in the page' % len(items))

        for item in items:
            response = self.process_item(item)

            yield response

    def go(self):
        page_param = self._config.get('page_param', None)

        if page_param:
            page_base_url = self._config.get('entry') + '&' + page_param + '='
            pages = int(self._config.get('pages', 1))

            for i in range(pages):
                logger.debug('Process page %d/%d' % (i + 1, pages))
                page_url = page_base_url + str(i + 1)
                results = self._go_page(page_url)
                for item in results:
                    yield item
        else:
            results = self._go_page(page_url)

        for item in results:
            yield item

    def process_item(self, item):
        if len(item.absolute_links) != 1:
            logger.error('More than one absolute links found inside item')
            return

        link = item.absolute_links.pop()

        session = HTMLSession()
        r = session.get(link)

        try:
            title = r.html.find(self._config.get('titleSelector'), first=True).text
            pubDate = self.get_date(r.html.find(self._config.get('dateSelector'), first=True))
            description = self.get_description(r.html.find(self._config.get('contentSelector'), first=True))
            addition = self.get_addition(r.html)
        except:
            logger.warn('failed to process url ' + r.html.url)
            return {}

        try:
            pubDate = parser.parse(pubDate).replace(tzinfo=pytz.timezone('Asia/Shanghai'))
        except:
            pubDate = datetime.now(pytz.utc).isoformat()

        response = {
            'link': link,
            'title': title,
            'description': description,
            'pubDate': pubDate,
            'addition': addition
        }

        return response



