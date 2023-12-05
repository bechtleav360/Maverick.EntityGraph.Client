__version__ = "0.0.23"

from .base_client import BaseApiClient
from .admin import Admin
from .entity import Entity
from .entity_builder import EntityBuilder
from .bulk_builder import BulkBuilder
from .query import Query
from .transaction import Transaction
from .application import Application

__base_api_client: (BaseApiClient, None) = None


def __getattr__(name):
    """
    Custom __getattr__ method for returning the base API Client to ensure a connection has been opened before usage.
    """
    if name == 'base_api_client':
        if __base_api_client is None:
            raise Exception("Not connected. Please create a connection to the entitygraph using entitygraph.connect.")
        else:
            return __base_api_client

    raise AttributeError(f"Module '{__name__}' has no attribute '{name}'")


def connect(api_key: str, host: str = "https://entitygraph.azurewebsites.net", ignore_ssl: bool = False):
    """
    Creates the BaseAPIClient instance necessary for connecting to the entitygraph API.

    :param api_key: Authorization key.
    :param host: The host address of the entitygraph API. Default: https://entitygraph.azurewebsites.net.
    :param ignore_ssl: For ignoring ssl verification, if necessary. Default: False.
    """
    global __base_api_client
    __base_api_client = BaseApiClient(api_key=api_key, base_url=host, ignore_ssl=ignore_ssl)
