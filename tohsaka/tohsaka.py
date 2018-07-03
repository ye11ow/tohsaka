import sys
import argparse
import importlib.util
from glob import glob
from os.path import join as pathjoin
import os, json

from utils import log_util
from tohsaka.qualifiers.qualifier import Qualifier
from tohsaka.spells import TohsakaException

logger = log_util.get_logger('tohsaka')


PRINT_FORMAT = '{0: <16} - {1}'
PARAM_FORMAT = '{0: <16} - {1: <64}'


def print_spells(): # pragma: no cover
    spells = Tohsaka.get_spells()

    print('Listing Spells...')
    print(PRINT_FORMAT.format('Name', 'Intro'))
    print('-' * 80)
    for spell in spells:
        print(PRINT_FORMAT.format(spell['name'], spell['intro']))
    print('\n')


def print_mystic_codes(): # pragma: no cover
    mystic_codes = Tohsaka.get_mystic_codes()

    print('Listing Mystic Codes...')
    print(PRINT_FORMAT.format('Name', 'Description'))
    print('-' * 80)
    for code in mystic_codes:
        print(PRINT_FORMAT.format(code['name'], code['description']))
    print('\n')


def print_mystic_code(mystic_code): # pragma: no cover
    mystic_json = Tohsaka.load_mystic_code(mystic_code)
    params = mystic_json.get('params', {})

    print('%s - %s' % (mystic_json.get('name'), mystic_json.get('description')))
    print('Parameters (%d):' % len(params.keys()))
    for key, value in params.items():
        required = value.get('required')
        if required:
            name = '(*)' + key
        else:
            name = key

        description = value.get('description')
        if value.get('default'):
            description += '. Default: %s' % value.get('default')

        print(PARAM_FORMAT.format(name, description))
    print('\n')


class Tohsaka:

    item_per_log = 10

    PARAM_INPUT_FORMAT = '{0}: {1}? '

    MYSTIC_PATH = pathjoin(os.path.dirname(os.path.realpath(__file__)), 'mystic')
    SPELL_PATH = pathjoin(os.path.dirname(os.path.realpath(__file__)), 'spells')
    OUTPUTTER_PATH = pathjoin(os.path.dirname(os.path.realpath(__file__)), 'outputters')

    @classmethod
    def get_spells(cls):
        spells = []

        for spell_file in glob(pathjoin(cls.SPELL_PATH, '*.py')):
            spec = importlib.util.spec_from_file_location('Spell', spell_file)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)

            if not hasattr(mod, 'Spell'):
                continue

            spells.append({
                'name': mod.Spell.name(),
                'intro': mod.Spell.intro(),
            })

        return spells


    @classmethod
    def get_mystic_codes(cls):
        mystic = []

        for mystic_file in glob(pathjoin(cls.MYSTIC_PATH, '*.json')):
            with open(mystic_file, 'r') as f:
                mystic_json = json.loads(f.read())

            mystic.append({
                'name': mystic_json.get('name'),
                'description': mystic_json.get('description', ''),
            })

        return mystic


    @classmethod
    def run(cls, mystic_code, input_params=None, save=None):
        mystic_json = cls.load_mystic_code(mystic_code)
        params = mystic_json.get('params', {})

        if not input_params:
            input_params = {}

            for key, value in params.items():
                required = value.get('required')
                if required:
                    name = '(*)' + key
                else:
                    name = key

                description = value.get('description')
                if value.get('default'):
                    description += '. (Default: %s)' % value.get('default')

                result = input(cls.PARAM_INPUT_FORMAT.format(name, description))

                if result:
                    input_params[key] = str(result)
                elif value.get('default'):
                    input_params[key] = value.get('default')
            print('\n')

            if save:
                Tohsaka.save(input_params, save)

        tohsaka = Tohsaka(mystic_code, input_params)
        tohsaka.go()


    @classmethod
    def save(cls, params, filepath):
        with open(filepath + '.json', 'w') as f:
            f.write(json.dumps(params, indent=4))


    @classmethod
    def load_mystic_code(cls, mystic_code):
        filepath = pathjoin(cls.MYSTIC_PATH, mystic_code + '.json')

        # load config
        try:
            with open(filepath) as mystic_file:
                mystic_json = json.load(mystic_file)

            return mystic_json
        except:
            logger.error('Failed to load mystic code %s. Please check whether "%s" exists.' % (mystic_code, filepath))
            raise Exception('Mystic code not found')


    def __init__(self, mystic_code, params):
        logger.info('Tohsaka start!')

        self.config = self.load_mystic_code(mystic_code)
        logger.info('Loaded Mystic Code %s' % mystic_code)

        self._validate_params(params)

        self.spell = self._load_module('Spell', mystic_code, self.SPELL_PATH, params)
        self.outputter = self._load_module('Outputter', mystic_code, self.OUTPUTTER_PATH, params)


    def _load_module(self, module_name, mystic_code, base_path, params):
        lower_name = module_name.lower()
        module_type = self.config.get(lower_name).get('type')

        if module_type == 'Custom':
            module_path = pathjoin(self.MYSTIC_PATH, mystic_code, '%s.py' % (lower_name))
        else:
            module_path = pathjoin(base_path, '%s.py' % module_type.lower())

        try:
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)

            options = self.config[lower_name]['options']

            self._replace_params(options, params)

            return getattr(mod, module_name)(options)
        except TohsakaException as err:
            raise err
        except Exception:
            logger.error('Failed to import the module %s from %s' % (module_name, module_path))
            raise Exception('Failed to import module')


    def _validate_params(self, params):
        defined_params = self.config.get('params', {})

        required = list(filter(lambda x: defined_params.get(x).get('required'), defined_params.keys()))

        for key in required:
            if not key in params:
                raise Exception('Required parameter "%s" does not exist. Current params [%s].' % (key, ', '.join(params.keys()) ))

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
            if isinstance(value, str):
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
