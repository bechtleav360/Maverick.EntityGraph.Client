import requests
import json

from entitygraph.api_response import ApiResponse


class BaseApiClient:
    def __init__(self, api_key: str, base_url: str, ignore_ssl: bool = False):
        self.base_url = base_url
        self.api_key = api_key
        self.ignore_ssl = ignore_ssl

    def make_request(self, method, endpoint, headers=None, params=None, data=None, files=None):
        url = f"{self.base_url}/{endpoint}"
        headers = headers or {}
        headers.update({
            'X-API-KEY': self.api_key
        })

        if data and isinstance(data, dict):
            data = json.dumps(data)

        response = requests.request(method, url, headers=headers, params=params,
                                    data=data, files=files, verify=not self.ignore_ssl)

        return ApiResponse(response.status_code, response.text)
