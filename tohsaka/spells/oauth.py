import requests
from spells.rest import Spell as BaseRest
from utils import log_util

logger = log_util.get_logger('OAuth')


class Spell(BaseRest):

    REQUIRED_OPTIONS = ['client_id', 'token', 'endpoint']

    def __init__(self, config):
        BaseRest.__init__(self, config)

    @classmethod
    def name(self):
        return 'OAuth'

    @classmethod
    def intro(self):
        return 'Get OAuth data'

    def go(self):
        endpoint = self.config.get('endpoint')
        headers = {
            'X-Access-Token': self.config.get('token'),
            'X-Client-ID': self.config.get('client_id')
        }
        r = requests.get(endpoint, headers=headers)

        if r.status_code == 200:
            yield r.json()
        else:
            logger.warning('Failed to fetch %s with error code %d' % (endpoint, r.status_code))
            yield None