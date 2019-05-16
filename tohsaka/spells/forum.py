import os

from requests_html import HTMLSession
from spells.base_spell import BaseSpell
from utils import log_util

logger = log_util.get_logger('tohsaka.fourm')


class Spell(BaseSpell):

    REQUIRED_OPTIONS = ['entry']

    def __init__(self, config):
        BaseSpell.__init__(self, config)
        self.headers = config.get('headers', {})

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


    def _get_items_from_page(self, url):
        session = HTMLSession()
        req = session.get(url,headers=self.headers)

        if req.history:
            logger.warning(f'Redirected to {req.url}')

        if req.status_code != 200:
            logger.warning(f'Error when fetching url {req.url}, with response code {req.status_code}')
            return []

        items = req.html.find(self.config.get('itemListSelector'))

        if len(items) == 0:
            logger.warning(f'Nothing found in url {req.url}')

        logger.debug(f'{len(items)} items detected in the page')

        return items


    def _get_id(self, link):
        return link


    def go(self):
        page_param = self.config.get('page_param', None)

        items = []

        if page_param:
            page_base_url = self.config.get('entry') + '&' + page_param + '='
            pages = int(self.config.get('pages', 1))

            for i in range(pages):
                logger.debug(f'Process page {i + 1}/{pages}')
                page_url = page_base_url + str(i + 1)
                items += self._get_items_from_page(page_url)
        else:
            items += self._get_items_from_page(self.config.get('entry'))

        logger.info(f'{len(items)} items detected.')

        for item in items:
            response = self.process_item(item)
            yield response


    def process_item(self, item):
        if len(item.absolute_links) != 1:
            logger.warning('Number of link is not 1', item)
            return {}

        link = item.absolute_links.pop()

        session = HTMLSession()

        try:
            req = session.get(link)
        except Exception as err:
            logger.warning(f'failed to get link {link}')
            logger.warning(str(err))

            return {}

        try:
            uid = self._get_id(link)
            title = req.html.find(self.config.get('titleSelector'), first=True).text
            pub_date = self.get_date(req.html.find(self.config.get('dateSelector'), first=True))
            description = self.get_description(req.html.find(self.config.get('contentSelector'), first=True))
            addition = self.get_addition(req.html)
        except Exception as err:
            logger.warning(f'failed to process url {req.html.url}')
            logger.warning(str(err))

            return {}

        response = {
            'id': uid,
            'link': link,
            'title': title,
            'description': description,
            'pubDate': pub_date,
            'addition': addition
        }

        return response
