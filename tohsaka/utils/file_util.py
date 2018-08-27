import json
import tempfile
import os
from utils import log_util
from pathlib import Path


logger = log_util.get_logger('tohsaka.file_util')

def load_json(filepath):
    result = None
    try:
        with open(filepath) as json_file:
            result = json.load(json_file)
    except:
        raise Exception('Failed to load file %s.' % (filepath))

    return result

def get_temp_dir():
    path = os.path.join(tempfile.gettempdir(), 'tohsaka')
    if not os.path.isdir(path):
        os.mkdir(path)

    logger.debug('Using temp folder %s', path)

    return path


def touch(path):
    """Touch the file if it does not exist. Return the existence of the file

    Arguments:
        path {[string]} -- path of the file
    """
    if os.path.isfile(path):
        return True
    else:
        Path(path).touch()
        return False