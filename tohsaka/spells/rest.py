import requests
from tohsaka.spells.base_spell import BaseSpell
from utils import log_util

logger = log_util.get_logger('tohsaka')


class Spell(BaseSpell):

    def __init__(self, config):
        BaseSpell.__init__(self, config)

    @classmethod
    def name(self):
        return 'Rest'

    @classmethod
    def intro(self):
        return 'Get REST data'

    def go(self):
        endpoint = self._config.get('endpoint')
        r = requests.get(endpoint)

        yield r.json()