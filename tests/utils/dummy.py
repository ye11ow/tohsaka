class DummyResponse:
    def __init__(self, html, status_code=200):
        self._html = html
        self._status_code = status_code

    @property
    def html(self):
        return self._html

    @property
    def status_code(self):
        return self._status_code

    def json(self):
        return 'json'