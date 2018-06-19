import sys
import argparse
import importlib.util
from glob import glob
import os, json

from utils import log_util
from tohsaka.qualifiers.qualifier import Qualifier

logger = log_util.get_logger('tohsaka')


class Tohsaka:

    item_per_log = 10

    MYSTIC_BASE_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'mystic')
    SPELL_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'spells')
    OUTPUTTER_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'outputters')


    @classmethod
    def list_spells(cls):
        spells = []

        for spell_file in glob(os.path.join(cls.SPELL_PATH, '*.py')):
            spec = importlib.util.spec_from_file_location('Spell', spell_file)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)

            if not hasattr(mod, 'Spell'):
                continue

            spells.append({
                'name': mod.Spell.name(),
                'intro': mod.Spell.intro(),
            })

        if len(spells) == 0:
            print('No spells found...')
            return []

        print('%d spells found...' % len(spells))
        for spell in spells:
            print('%s: %s' % (spell['name'], spell['intro']))

        return spells


    def __init__(self, mystic_code):
        logger.info('Tohsaka start!')

        self.load_mystic_code(mystic_code)
        logger.info('Loadded Mystic Code %s' % mystic_code)
        self.load_outputter()


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
        spell_type = self.config.get('spell').get('type')

        if spell_type == 'Custom':
            module_path = os.path.join(self.MYSTIC_BASE_PATH, mystic_code, 'spell.py')
        else:
            module_path = os.path.join(self.SPELL_PATH, '%s.py' % spell_type.lower())

        try:
            spec = importlib.util.spec_from_file_location('Spell', module_path)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)

            self.spell = mod.Spell(self.config.get('spell').get('options'))
        except:
            logger.error('Failed to import the spell from %s' % (module_path))
            raise Exception('Failed to import spell')


    def load_outputter(self):
        outputter_type = self.config.get('outputter').get('type')

        module_path = os.path.join(self.OUTPUTTER_PATH, '%s.py' % outputter_type.lower())

        try:
            spec = importlib.util.spec_from_file_location('Outputter', module_path)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)

            self.outputter = mod.Outputter(self.config.get('outputter').get('options'))
        except:
            logger.error('Failed to import the outputter from %s' % (module_path))
            raise Exception('Failed to import outputter')


    def go(self):
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

            self.outputter.go(item)

        self.outputter.done()
