import requests
import json
import httpx
from requests import Response, Request, PreparedRequest


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

        request: Request = requests.Request(method, url, headers=headers, params=params,
                                            data=data, files=files)

        with requests.Session() as s:
            prepared_request: PreparedRequest = s.prepare_request(request)
            response: Response = s.send(prepared_request, verify=not self.ignore_ssl)

        if response.status_code not in range(200, 300):
            raise Exception(
                f"Request {{'url': {request.url}, 'headers': {request.headers}}} failed with status {response.status_code}. Response: {response.text}")

        return response

    async def make_async_request(self, method, endpoint, headers=None, params=None, data=None, files=None):
        url = f"{self.base_url}/{endpoint}"
        headers = headers or {}
        headers.update({
            'X-API-KEY': self.api_key
        })

        if data and isinstance(data, dict):
            data = json.dumps(data)

        async with httpx.AsyncClient(verify=not self.ignore_ssl) as client:
            if method.lower() == 'get':
                response = await client.get(url, headers=headers, params=params)
            elif method.lower() == 'post':
                response = await client.post(url, headers=headers, data=data, files=files)
            elif method.lower() == 'put':
                response = await client.put(url, headers=headers, data=data, files=files)
            elif method.lower() == 'delete':
                response = await client.delete(url, headers=headers)
            else:
                raise ValueError(f"HTTP method '{method}' not supported")

        if response.status_code not in range(200, 300):
            raise Exception(
                f"Request failed with status {response.status_code}. Response: {response.text}")

        return response
