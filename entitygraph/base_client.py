import json
import logging

import requests
from requests import Response, Request, PreparedRequest


class BaseApiClient:
    def __init__(self, api_key: str, base_url: str, ignore_ssl: bool = False):
        """
        Base Client for making requests to the entitygraph API.

        :param api_key: Authorization key.
        :param base_url: The host address of the entitygraph API.
        :param ignore_ssl: For ignoring ssl verification, if necessary.
        """
        self.base_url = base_url
        self.api_key = api_key
        self.ignore_ssl = ignore_ssl

    def make_request(self, method: str, endpoint: str, **kwargs):
        """
        Sends a request to the entitygraph API.

        :param method: Analog to requests module methods.
        :param endpoint: The relative entitygraph API endpoint.
        :param kwargs: Additional parameters for the request. The X-API-KEY is automatically added to the "headers"
            parameters. The "data" parameters is converted to a json string, if a dictionary or a list are given.

        :return: The requests response.
        """
        url = f"{self.base_url}/{endpoint}"
        kwargs["headers"] = kwargs["headers"] if "headers" in kwargs else {}
        kwargs["headers"]["X-API-KEY"] = self.api_key

        if "data" in kwargs and kwargs["data"] is not None and not isinstance(kwargs["data"], str):
            try:
                kwargs["data"] = json.dumps(kwargs["data"])
            except TypeError as t_e:
                logging.error(t_e)
                raise TypeError("The given data for the entitygraph must be json serializable.")

        request: Request = requests.Request(method, url, **kwargs)

        with requests.Session() as s:
            prepared_request: PreparedRequest = s.prepare_request(request)
            response: Response = s.send(prepared_request, verify=not self.ignore_ssl)

        if response.status_code not in range(200, 300):
            raise Exception(
                f"Request {{'url': {request.url}, 'headers': {request.headers}}} "
                f"failed with status {response.status_code}. Response: {response.text}")

        return response

    # async def make_async_request(self, method, endpoint, headers=None, params=None, data=None, files=None):
    #     url = f"{self.base_url}/{endpoint}"
    #     headers = headers or {}
    #     headers.update({
    #         'X-API-KEY': self.api_key
    #     })
    #
    #     if data and isinstance(data, dict):
    #         data = json.dumps(data)
    #
    #     async with httpx.AsyncClient(verify=not self.ignore_ssl) as client:
    #         if method.lower() == 'get':
    #             response = await client.get(url, headers=headers, params=params)
    #         elif method.lower() == 'post':
    #             response = await client.post(url, headers=headers, data=data, files=files)
    #         elif method.lower() == 'put':
    #             response = await client.put(url, headers=headers, data=data, files=files)
    #         elif method.lower() == 'delete':
    #             response = await client.delete(url, headers=headers)
    #         else:
    #             raise ValueError(f"HTTP method '{method}' not supported")
    #
    #     if response.status_code not in range(200, 300):
    #         raise Exception(
    #             f"Request failed with status {response.status_code}. Response: {response.text}")
    #
    #     return response
