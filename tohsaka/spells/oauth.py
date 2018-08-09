from spells.rest import Spell as BaseRest


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

    def get_headers(self):
        headers = BaseRest.get_headers(self)

        headers['X-Access-Token'] = self.config.get('token')
        headers['X-Client-ID'] = self.config.get('client_id')

        return headers
