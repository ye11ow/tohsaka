from tohsaka.outputters.rss import Outputter

class TestRestSpell:
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