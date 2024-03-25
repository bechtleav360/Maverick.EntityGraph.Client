import json
import logging
import requests

from requests import Response, Request, PreparedRequest

logger = logging.getLogger(__name__)


# TODO Add Sessions(?) and Threading for multiple calls at the same time
class BaseApiClient:
    def __init__(self, api_key: str, base_url: str, ignore_ssl: bool = False):
        """Base Client for making requests to the entitygraph API

        :param api_key: Authorization key.
        :type api_key: str
        :param base_url: The host address of the entitygraph API.
        :type base_url: str
        :param ignore_ssl: For ignoring ssl verification, if necessary. False by default.
        :type ignore_ssl: bool
        """
        self.base_url = base_url
        self.api_key = api_key
        self.ignore_ssl = ignore_ssl

    def make_request(self, method: str, endpoint: str, **kwargs) -> Response:
        """Sends a request to the entitygraph API

        :param method: Analog to requests module methods.
        :type method: str
        :param endpoint: The relative entitygraph API endpoint.
        :type endpoint: str
        :param kwargs: Additional parameters for the request. The X-API-KEY is automatically added to the "headers"
            parameters. The "data" parameters is converted to a json string, if a dictionary or a list are given.

        :return: The request's response.
        :rtype: Response
        """
        url = f"{self.base_url}/{endpoint}"
        kwargs["headers"] = kwargs["headers"] if "headers" in kwargs else {}
        kwargs["headers"]["X-API-KEY"] = self.api_key

        if "data" in kwargs and kwargs["data"] is not None and isinstance(kwargs["data"], dict):
            try:
                kwargs["data"] = json.dumps(kwargs["data"])
            except TypeError as t_e:
                logging.error(t_e)
                raise TypeError("The given data for the entitygraph must be json serializable.")

        logger.debug(f"Making {method} request to {url}. Arguments: {kwargs}")
        request: Request = requests.Request(method, url, **kwargs)

        with requests.Session() as s:
            prepared_request: PreparedRequest = s.prepare_request(request)
            response: Response = s.send(prepared_request, verify=not self.ignore_ssl)

        # Let the classes using this method handle the error
        if not response.ok:
            logger.warning(f"Request {{'url': {request.url}, 'headers': {request.headers}}} "
                           f"failed with status {response.status_code}. Response: {response.text}")

        return response
