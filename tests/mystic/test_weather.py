import tempfile
import json
import os
from os.path import join as pathjoin
from tohsaka.tohsaka import Tohsaka

class TestWeather:

    def test_weather(self):
        FILENAME = 'shanghai'
        tohsaka = Tohsaka('weather', {
            'appid': os.environ['OPENWEATHER_TOKEN'],
            'city': 'shanghai',
            'country': 'cn',
            'output_file': FILENAME
        })

        tohsaka.outputter.OUTPUT_FOLDER = tempfile.gettempdir()
        tohsaka.go()

        with open(pathjoin(tohsaka.outputter.OUTPUT_FOLDER, FILENAME + '.json'), 'r') as json_file:
            result = json.loads(json_file.read())

        assert result
        assert 'city' in result[0]
        assert 'cnt' in result[0]