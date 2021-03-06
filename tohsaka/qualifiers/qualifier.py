from utils.log_util import get_logger

logger = get_logger('tohsaka.qualifier')

class Qualifier:

    def __init__(self, config):
        self.config = config.get('qualify', None)

    def _qualify(self, item):
        if not self.config:
            return True

        fields = self.config.get('field', [])
        value = item
        for f in fields:
            value = value.get(f, {})

        if type(value) == dict:
            return False

        condition = self.config.get('condition', {}).get('type', None)
        target_value = int(self.config.get('condition', {}).get('value', 0))
        if condition == '>':
            if value > target_value:
                return True
            else:
                logger.debug(f'{item.get("title")} doesnt pass the qualify {value}/{target_value}')
                return False
        else:
            raise Exception(f'Unimplemented condition type {condition}. Qualify params: {self.config}')


    def go(self, item):
        return self._qualify(item)
