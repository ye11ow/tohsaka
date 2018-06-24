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


    def __init__(self, mystic_code, params):
        logger.info('Tohsaka start!')

        self.load_mystic_code(mystic_code)
        logger.info('Loaded Mystic Code %s' % mystic_code)

        self._validate_params(params)

        self.spell = self._load_module('Spell', mystic_code, self.SPELL_PATH, params)
        self.outputter = self._load_module('Outputter', mystic_code, self.OUTPUTTER_PATH, params)


    def load_mystic_code(self, mystic_code):
        filepath = os.path.join(self.MYSTIC_BASE_PATH, mystic_code + '.json')

        # load config
        try:
            with open(filepath) as mystic_file:
                mystic_json = json.load(mystic_file)

            self.config = mystic_json
        except:
            logger.error('Failed to load mystic code %s. Please check whether "%s" exists' % (mystic_code, filepath))
            raise Exception('Mystic code not found')


    def _load_module(self, module_name, mystic_code, base_path, params):
        lower_name = module_name.lower()
        module_type = self.config.get(lower_name).get('type')

        if module_type == 'Custom':
            module_path = os.path.join(self.MYSTIC_BASE_PATH, mystic_code, '%s.py' % (lower_name))
        else:
            module_path = os.path.join(base_path, '%s.py' % module_type.lower())

        try:
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)

            options = self.config[lower_name]['options']

            self._replace_params(options, params)

            return getattr(mod, module_name)(options)
        except:
            logger.error('Failed to import the module %s from %s' % (module_name, module_path))
            raise Exception('Failed to import module')


    def _validate_params(self, params):
        defined_params = self.config.get('params', {})

        required = list(filter(lambda x: defined_params.get(x).get('required'), defined_params.keys()))

        for key in required:
            if not key in params:
                raise Exception('Required parameter %s does not exist. Current params %s' % (key, ', '.join(params.keys()) ))

        return True


    def _replace_params(self, options, params):
        defined_params = self.config.get('params', {})

        # if any param is not set and has default value, apply it
        default = list(filter(lambda x: defined_params.get(x).get('default'), defined_params.keys()))

        for key in default:
            if key not in params:
                params[key] = defined_params.get(key).get('default')

        for key in options:
            value = options[key]
            if type(value) == str:
                for param in params:
                    value = value.replace('<<%s>>' % param, params[param])

                options[key] = value


    def go(self):
        qualifier = Qualifier(self.config)

        item_count = 0
        failed_count = 0
        filtered_count = 0

        logger.info('Tohsaka GO!')

        for item in self.spell.go():
            if item_count > 0 and item_count % self.item_per_log == 0:
                logger.info('%d item processed. Success %d, failure %d, filtered %d.' % (item_count, item_count - failed_count - filtered_count, failed_count, filtered_count))

            item_count += 1

            if not item:
                failed_count += 1
                continue

            if not qualifier.go(item):
                filtered_count += 1
                continue

            self.outputter.go(item)

        logger.info('GO Tohsaka!')
        logger.info('%d item processed. Success %d, failure %d, filtered %d.' % (item_count, item_count - failed_count - filtered_count, failed_count, filtered_count))

        self.outputter.done()
