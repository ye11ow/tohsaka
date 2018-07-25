import tempfile
import json
import os
from os.path import join as pathjoin
from tohsaka import Tohsaka
from utils.file_util import load_json

class TestWeather:

    def test_weather(self):
        FILENAME = 'vancouver'
        tohsaka = Tohsaka('weather', {
            'appid': os.environ['OPENWEATHER_TOKEN'],
            'city': 'vancouver',
            'country': 'ca',
            'output_file': FILENAME
        })

        tohsaka.outputter.OUTPUT_FOLDER = tempfile.gettempdir()
        tohsaka.go()

        result = load_json(pathjoin(tohsaka.outputter.OUTPUT_FOLDER, FILENAME + '.json'))

        assert result
        assert 'city' in result[0]
        assert 'cnt' in result[0]