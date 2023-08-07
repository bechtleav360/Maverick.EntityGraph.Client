__version__ = "0.0.17"

from .base_client import BaseApiClient
from .admin import Admin
from .entity import Entity
from .entity_builder import EntityBuilder
from .bulk_builder import BulkBuilder
from .query import Query
from .transaction import Transaction
from .application import Application

_base_client: BaseApiClient = None



def connect(api_key: str, host: str = "https://entitygraph.azurewebsites.net", ignore_ssl: bool = False):
    global _base_client
    _base_client = BaseApiClient(api_key=api_key, base_url=host, ignore_ssl=ignore_ssl)
