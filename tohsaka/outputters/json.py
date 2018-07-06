import os
import json

from outputters.base_outputter import BaseOutputter


class Outputter(BaseOutputter):
    """Outputter result into a JSON file
    """

    @property
    def REQUIRED_FIELDS(self):
        return []

    def __init__(self, config):
        BaseOutputter.__init__(self, config)

        self.file = config.get('filename', 'output') + '.json'
        self.data = []

    def _output(self):
        with open(os.path.join(self.OUTPUT_FOLDER, self.file), 'w') as json_file:
            json_file.write(json.dumps(self.data, indent=2, sort_keys=True))

    def _add_item(self, item):
        self.data.append(item)
