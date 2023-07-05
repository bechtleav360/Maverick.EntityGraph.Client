import json


class ApiResponse:
    def __init__(self, status_code, text, headers: dict = None):
        self.code = status_code
        self.text = text
        self.headers = headers

    def __str__(self):
        return self.text

    def __repr__(self):
        return self.text

    def json(self):
        return json.loads(self.text)
