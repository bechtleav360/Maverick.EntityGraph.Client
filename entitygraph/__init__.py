__version__ = "0.0.14"

from .base_client import BaseApiClient
from .admin import Admin
from .entity import Entity
from .entity_builder import EntityBuilder
from .query import Query
from .transaction import Transaction
from .application import Application

base_client: BaseApiClient = None
API_KEY: str = None
HOST: str = None
IGNORE_SSL: bool = False


def connect(api_key: str, host: str = "https://entitygraph.azurewebsites.net", ignore_ssl: bool = False):
    global API_KEY
    API_KEY = api_key
    global HOST
    HOST = host
    global IGNORE_SSL
    IGNORE_SSL = ignore_ssl

    global base_client
    base_client = BaseApiClient(api_key=api_key, base_url=host, ignore_ssl=ignore_ssl)
