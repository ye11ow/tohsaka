import hashlib
import os

from requests_html import HTMLSession
from spells.base_spell import BaseSpell
from utils import log_util
from utils import file_util

logger = log_util.get_logger('tohsaka')


class Spell(BaseSpell):

    REQUIRED_OPTIONS = ['entry']

    def __init__(self, config):
        BaseSpell.__init__(self, config)
        self.temp_dir = file_util.get_temp_dir()

    @classmethod
    def name(cls):
        return 'Forum'


    @classmethod
    def intro(cls):
        return 'Get forum-like data'


    def get_date(self, element):
        return element.text


    def get_description(self, element):
        return element.html


    def get_addition(self, html):
        return None


    def _go_page(self, url):
        session = HTMLSession()
        req = session.get(url)

        if req.history:
            logger.warning('Redirected to %s', req.url)

        if req.status_code != 200:
            logger.warning('Error when fetching url %s, with response code %d', req.url, req.status_code)
            return

        items = req.html.find(self.config.get('itemListSelector'))

        if len(items) == 0:
            logger.warning('Nothing found in url %s', req.url)

        logger.debug('%d items detected in the page', len(items))

        for item in items:
            response = self.process_item(item)
            yield response


    def _dedup(self, link):
        filename = hashlib.md5(link.encode('utf-8')).hexdigest()

        return file_util.dedup(os.path.join(self.temp_dir, filename))


    def go(self):
        page_param = self.config.get('page_param', None)

        if page_param:
            page_base_url = self.config.get('entry') + '&' + page_param + '='
            pages = int(self.config.get('pages', 1))

            for i in range(pages):
                logger.debug('Process page %d/%d', i + 1, pages)
                page_url = page_base_url + str(i + 1)
                results = self._go_page(page_url)
                for item in results:
                    yield item
        else:
            results = self._go_page(self.config.get('entry'))

        for item in results:
            yield item


    def process_item(self, item):
        if len(item.absolute_links) != 1:
            logger.error('More than one absolute links found inside item')
            return

        link = item.absolute_links.pop()

        if self._dedup(link):
            return {}

        session = HTMLSession()

        try:
            req = session.get(link)
        except Exception as err:
            logger.warning('failed to get link %s', link)
            logger.warning(str(err))

            return {}

        try:
            title = req.html.find(self.config.get('titleSelector'), first=True).text
            pub_date = self.get_date(req.html.find(self.config.get('dateSelector'), first=True))
            description = self.get_description(req.html.find(self.config.get('contentSelector'), first=True))
            addition = self.get_addition(req.html)
        except Exception as err:
            logger.warning('failed to process url %s', req.html.url)
            logger.warning(str(err))

            return {}

        response = {
            'link': link,
            'title': title,
            'description': description,
            'pubDate': pub_date,
            'addition': addition
        }

        return response
