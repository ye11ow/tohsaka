from tohsaka.outputters.base_outputter import BaseOutputter
import os
import json


class Outputter(BaseOutputter):

    @property
    def REQUIRED_FIELDS(self):
        return []

    def __init__(self, config):
        BaseOutputter.__init__(self, config)

        self.file = config.get('filename', 'output') + '.json'
        folder = os.path.join(os.getcwd(), 'output')
        self.output_path = os.path.join(folder, self.file)

        if not os.path.isdir(folder):
            os.mkdir(folder)

        self.data = []

    def done(self):
        with open(self.output_path, 'w') as f:
            f.write(json.dumps(self.data, indent=2, sort_keys=True))

    def _output(self, item):
        self.data.append(item)
