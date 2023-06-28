import json


class ApiResponse:
    def __init__(self, status_code, text):
        self.code = status_code
        self.text = text
        self.success = status_code in range(200, 300)

    def __str__(self):
        return self.text

    def __repr__(self):
        return self.text

    def json(self):
        return json.loads(self.text)

    def raise_for_status(self):
        if not self.success:
            raise Exception(f"Request failed with status code {self.code} and message: {self.text}")
