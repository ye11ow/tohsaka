from utils.log_util import get_logger

logger = get_logger('qualifier')

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
                logger.debug('%s doesnt pass the qualify %d/%d' % (item.get('title'), value, target_value))
                return False
        else:
            logger.error('Unimplemented condition type %s. Qualify params: %s' % (condition, str(self.config)))
            return True


    def go(self, item):
        return self._qualify(item)



# if __name__ == '__main__':
#     fields = {
#         "link": "hello",
#         "title": "word",
#         "pubdate": "2017-03-12",
#         "replies": "20",
#         "author": "me"
#     }

#     tohsaka_qualifier = Qualifier()
#     tohsaka_qualifier.start(fields)