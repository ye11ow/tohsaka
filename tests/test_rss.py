import tempfile
from os.path import join as pathjoin
from unittest.mock import patch
from tohsaka.outputters.rss import Outputter

class TestRSS:
    """
    Add more cases related to pubDate
    """

    def test_add_entry(self):
        outputter = Outputter({
            'filename': 'test',
            'description': 'desc',
            'host': 'http://www.google.com'
        })

        outputter.go({
            'title': '123',
            'description': '345',
            'link': 'link',
            'pubDate': 'now'
        })

        assert len(outputter.fg.item()) == 1

    @patch('tohsaka.outputters.rss.FeedGenerator')
    @patch('tohsaka.outputters.rss.os.mkdir')
    def test_done(self, mkdir, FeedGenerator):
        temp_dir = pathjoin(tempfile.gettempdir(), 'EMPTYFOLDER')

        outputter = Outputter({
            'filename': 'test',
            'description': 'desc',
            'host': 'http://www.google.com'
        })
        outputter.OUTPUT_FOLDER = temp_dir

        outputter.done()

        mkdir.assert_called_once_with(temp_dir)
        FeedGenerator.return_value.atom_file.assert_called_once()