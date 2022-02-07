from spells.rest import Spell as BaseSpell
from utils import log_util

logger = log_util.get_logger('tohsaka.fund')


class Spell(BaseSpell):

    REQUIRED_OPTIONS = ['code']

    def __init__(self, config):
        code = config['code']
        print(config)
        config['endpoint'] = f'https://fund.10jqka.com.cn/data/client/myfund/{code}'
        BaseSpell.__init__(self, config)

    @classmethod
    def name(self):
        return 'Fund'

    @classmethod
    def intro(self):
        return 'Get Fund data'

    def go(self):
        for item in BaseSpell.go(self):
            data = item['data'][0]
            net = float(data['net'])
            yield {
                'name': data['name'],
                'unit_value': net,
                'date': data['enddate'],
                'total_value': net * float(self.config['units'])
            }
