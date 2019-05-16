import importlib.util
from glob import glob
from os.path import join as pathjoin
import os

from utils import log_util
from utils.file_util import load_json
from qualifiers.qualifier import Qualifier
from spells import TohsakaException

logger = log_util.get_logger('tohsaka')


class Tohsaka:

    item_per_log = 10

    MYSTIC_PATH = pathjoin(os.path.dirname(os.path.realpath(__file__)), 'mystic')
    SPELL_PATH = pathjoin(os.path.dirname(os.path.realpath(__file__)), 'spells')
    OUTPUTTER_PATH = pathjoin(os.path.dirname(os.path.realpath(__file__)), 'outputters')


    @classmethod
    def get_mystic_codes(cls):
        mystic = []

        for mystic_file in glob(pathjoin(cls.MYSTIC_PATH, '*.json')):
            mystic_json = load_json(mystic_file)

            mystic.append({
                'name': mystic_json.get('name'),
                'description': mystic_json.get('description', ''),
            })

        return mystic


    @classmethod
    def load_mystic_code(cls, mystic_code):
        filepath = pathjoin(cls.MYSTIC_PATH, mystic_code + '.json')

        return load_json(filepath)


    def __init__(self, mystic_code, params):
        logger.info('Tohsaka start!')

        self.config = self.load_mystic_code(mystic_code)
        logger.info(f'Loaded Mystic Code {mystic_code}')

        self._validate_params(params)

        self.spell = self._load_module('Spell', mystic_code, self.SPELL_PATH, params)
        self.outputter = self._load_module('Outputter', mystic_code, self.OUTPUTTER_PATH, params)


    def _load_module(self, module_name, mystic_code, base_path, params):
        lower_name = module_name.lower()
        module_type = self.config.get(lower_name).get('type')

        if module_type == 'Custom':
            module_path = pathjoin(self.MYSTIC_PATH, mystic_code, f'{lower_name}.py')
        else:
            module_path = pathjoin(base_path, f'{module_type.lower()}.py')

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
            logger.error(f'Failed to import the module {module_name} from {module_path}')
            raise Exception('Failed to import module')


    def _validate_params(self, params):
        defined_params = self.config.get('params', {})

        required = list(filter(lambda x: defined_params.get(x).get('required'), defined_params.keys()))

        for key in required:
            if not key in params:
                raise Exception(f'Required parameter "{key}" does not exist. Current params [{", ".join(params.keys())}].')

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

                    # support boolean param
                    if type(params[param]) == type(True):
                        if value == (f'<<{param}>>'):
                            value = params[param]
                            break
                    else:
                        value = value.replace(f'<<{param}>>', params[param])

                options[key] = value


    def go(self):
        qualifier = Qualifier(self.config)

        item_count = 0
        failed_count = 0
        filtered_count = 0

        logger.info('Tohsaka GO!')

        for item in self.spell.go():
            if item_count > 0 and item_count % self.item_per_log == 0:
                logger.info(f'{item_count} items processed. Success {item_count - failed_count - filtered_count}, failure {failed_count}, filtered {filtered_count}.')

            item_count += 1

            if not item:
                failed_count += 1
                continue

            if not qualifier.go(item):
                filtered_count += 1
                continue

            self.outputter.go(item)

        logger.info('GO Tohsaka!')
        logger.info(f'{item_count} items processed. Success {item_count - failed_count - filtered_count}, failure {failed_count}, filtered {filtered_count}.')

        self.outputter.done()
