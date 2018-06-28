import tempfile
from os.path import join as pathjoin
from unittest.mock import patch
from tohsaka.outputters.rss import Outputter

class TestRSS:
    """
    Add more cases related to pubDate
    """

    def test_add_item(self):
        outputter = Outputter({
            'filename': 'test',
            'description': 'desc',
            'host': 'http://www.google.com'
        })

        outputter._add_item({
            'title': '123',
            'description': '345',
            'link': 'link',
            'pubDate': 'now'
        })

        assert len(outputter.fg.item()) == 1

    def test_invalid_item(self):
        outputter = Outputter({
            'filename': 'test',
            'description': 'desc',
            'host': 'http://www.google.com'
        })

        outputter.go({
            'title': '123',
            'description': '345',
            'link': 'link'
        })

        assert len(outputter.fg.item()) == 0

    @patch('tohsaka.outputters.rss.FeedGenerator')
    def test_output(self, FeedGenerator):
        outputter = Outputter({
            'filename': 'test',
            'description': 'desc',
            'host': 'http://www.google.com'
        })

        outputter._output()

        FeedGenerator.return_value.atom_file.assert_called_once()