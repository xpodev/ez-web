from json import dumps


class _EzResponse:
    def __init__(self):
        self.headers = {}
        self.status_code = 200
        self.body = None

    def status(self, code):
        self.status_code = code

    def header(self, key, value):
        self.headers[key] = value

    def json(self, data):
        self.headers["Content-Type"] = "application/json"
        self.body = dumps(data)

    def text(self, data):
        self.headers["Content-Type"] = "text/plain"
        self.body = data

    def html(self, data):
        self.headers["Content-Type"] = "text/html"
        self.body = data


response = _EzResponse()
