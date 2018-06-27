from tohsaka.outputters.base_outputter import BaseOutputter
import os
import json


class Outputter(BaseOutputter):

    OUTPUT_FOLDER = os.path.join(os.getcwd(), 'output')

    @property
    def REQUIRED_FIELDS(self):
        return []

    def __init__(self, config):
        BaseOutputter.__init__(self, config)

        self.file = config.get('filename', 'output') + '.json'
        self.data = []

    def done(self):
        if not os.path.isdir(self.OUTPUT_FOLDER):
            os.mkdir(self.OUTPUT_FOLDER)

        with open(os.path.join(self.OUTPUT_FOLDER, self.file), 'w') as f:
            f.write(json.dumps(self.data, indent=2, sort_keys=True))

    def _output(self, item):
        self.data.append(item)
