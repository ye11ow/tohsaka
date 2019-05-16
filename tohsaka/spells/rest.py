import requests
from spells.base_spell import BaseSpell
from utils import log_util

logger = log_util.get_logger('tohsaka.rest')


class Spell(BaseSpell):

    REQUIRED_OPTIONS = ['endpoint']

    def __init__(self, config):
        BaseSpell.__init__(self, config)

    @classmethod
    def name(self):
        return 'Rest'

    @classmethod
    def intro(self):
        return 'Get REST data'

    def get_headers(self):
        return {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

    def go(self):
        endpoint = self.config.get('endpoint')
        r = requests.get(endpoint, headers=self.get_headers())

        if r.status_code == 200:
            yield r.json()
        else:
            logger.warning(f'Failed to fetch {endpoint} with error code {r.status_code}')
            yield None
