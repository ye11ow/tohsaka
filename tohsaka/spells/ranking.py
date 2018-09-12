import os

from requests_html import HTMLSession
from spells.forum import Spell as BaseSpell
from utils import log_util

logger = log_util.get_logger('tohsaka.ranking')


class Spell(BaseSpell):

    def __init__(self, config):
        BaseSpell.__init__(self, config)

    @classmethod
    def name(cls):
        return 'Ranking'

    @classmethod
    def intro(cls):
        return 'Get ranking-like data'

    def process_item(self, item):
        try:
            title = item.find(self.config.get('titleSelector'), first=True).text
            pub_date = self.get_date(item.find(self.config.get('dateSelector'), first=True))
            description = self.get_description(item.find(self.config.get('contentSelector'), first=True))
            addition = self.get_addition(item)
        except Exception as err:
            logger.warning('failed to process url %s', item)
            logger.warning(str(err))

            return {}

        response = {
            'id': title,
            'link': '',
            'title': title,
            'description': description,
            'pubDate': pub_date,
            'addition': addition
        }

        return response