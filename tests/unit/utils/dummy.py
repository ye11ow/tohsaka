class DummyResponse:
    def __init__(self, html, status_code=200, history=None, url='http://www.google.com'):
        self._html = html
        self._status_code = status_code
        self._history = history
        self._url = url

    @property
    def html(self):
        return self._html

    @property
    def status_code(self):
        return self._status_code

    @property
    def history(self):
        return self._history

    @property
    def url(self):
        return self._url

    def json(self):
        return 'json'

