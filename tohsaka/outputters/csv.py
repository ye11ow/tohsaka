import os
import csv

from outputters.base_outputter import BaseOutputter


class Outputter(BaseOutputter):
    """Outputter result into a CSV file
    """

    @property
    def REQUIRED_FIELDS(self):
        return []

    def __init__(self, config):
        BaseOutputter.__init__(self, config)

        self.file = config.get('filename', 'output') + '.csv'
        self.append = config.get('append', False)
        self.data = []

    def _output(self):
        headers = set()
        for item in self.data:
            headers.update(item.keys())

        if not self.append:
            with open(os.path.join(self.OUTPUT_FOLDER, self.file), 'w') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=list(headers))

                writer.writeheader()
                for item in self.data:
                    writer.writerow(item)
        else:
            with open(os.path.join(self.OUTPUT_FOLDER, self.file), 'a') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=list(headers))

                for item in self.data:
                    writer.writerow(item)


    def _add_item(self, item):
        self.data.append(item)
