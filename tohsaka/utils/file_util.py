import json
import tempfile
import os
from pathlib import Path


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

    return path


def dedup(path):
    if os.path.isfile(path):
        return True
    else:
        Path(path).touch()
        return False