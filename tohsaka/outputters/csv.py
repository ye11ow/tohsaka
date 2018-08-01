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
        headers = sorted(list(headers))

        filepath = os.path.join(self.output_folder, self.file)

        if (not self.append) or (not os.path.exists(filepath)):
            with open(filepath, 'w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=list(headers))

                writer.writeheader()
                writer.writerows(self.data)
        else:
            with open(filepath, 'a', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=list(headers))

                writer.writerows(self.data)


    def _add_item(self, item):
        self.data.append(item)
