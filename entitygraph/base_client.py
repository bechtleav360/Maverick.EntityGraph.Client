import requests
import json


class BaseApiClient:
    def __init__(self, api_key: str, base_url: str, ignore_ssl: bool = False):
        self.base_url = base_url
        self.api_key = api_key
        self.ignore_ssl = ignore_ssl

    def make_request(self, method, endpoint, headers=None, params=None, data=None):
        url = f"{self.base_url}/{endpoint}"
        headers = headers or {}
        headers.update({
            'X-API-KEY': self.api_key
        })

        response = requests.request(method, url, headers=headers, params=params,
                                    data=json.dumps(data) if data else None, verify=not self.ignore_ssl)

        if response.status_code in range(200, 300):
            return response.json()
        else:
            return response.status_code, response.text

