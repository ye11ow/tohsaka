import json

def load_json(filepath):
    result = None
    try:
        with open(filepath) as json_file:
            result = json.load(json_file)
    except:
        raise Exception('Failed to load file %s.' % (filepath))

    return result