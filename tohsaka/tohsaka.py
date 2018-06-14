import sys
import argparse
import importlib.util
from urllib.parse import urlparse
import os, json

from utils import log_util
from tohsaka.qualifiers.qualifier import Qualifier
from tohsaka.outputters.rss_outputter import Outputter

logger = log_util.get_logger('tohsaka')


class Tohsaka:

    item_per_log = 10

    MYSTIC_BASE_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'mystic')

    def __init__(self, mystic_code):
        logger.info('Tohsaka start!')

        self.load_mystic_code(mystic_code)


    def load_mystic_code(self, mystic_code):
        filepath = os.path.join(self.MYSTIC_BASE_PATH, mystic_code + '.json')

        # load config
        try:
            with open(filepath) as mystic_file:
                mystic_json = json.load(mystic_file)

            self.config = mystic_json
        except:
            logger.error('Failed to load mystic code (%s)' % (mystic_code))
            logger.error('Please check whether "%s" exists' % (filepath))
            raise Exception('Mystic code not found')

        # load spell
        if os.path.isfile(os.path.join(self.MYSTIC_BASE_PATH, mystic_code, 'spell.py')):
            try:
                spec = importlib.util.spec_from_file_location("Spell", os.path.join(self.MYSTIC_BASE_PATH, mystic_code, 'spell.py'))
                foo = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(foo)

                self.spell = foo.Spell(self.config)
            except:
                logger.error('Failed to import the spell for mystic code (%s)' % (mystic_code))
                raise Exception('Failed to import spell')


    def go(self):
        urlresult = urlparse(self.config.get('entry'))
        host = urlresult.scheme + '://' + urlresult.netloc

        outputter = Outputter(base_link=host, title=self.config.get('id'), description='Little secret', file=self.config.get('id')+'.xml')
        qualifier = Qualifier(self.config)

        item_count = 0
        failed_count = 0
        filtered_count = 0

        for item in self.spell.go():
            if item_count > 0 and item_count % 10 == 0:
                logger.info('%d item processed. Success %d, failure %d, filtered %d.' % (item_count, item_count - failed_count - filtered_count, failed_count, filtered_count))

            item_count += 1

            if not item:
                failed_count += 1
                continue

            if not qualifier.go(item):
                filtered_count += 1
                continue

            outputter.go(item)

        outputter.done()