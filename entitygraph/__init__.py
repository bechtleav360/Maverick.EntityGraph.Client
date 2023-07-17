__version__ = "0.0.1"

from .api.entities_api import EntitiesAPI
from .api.transactions_api import TransactionsAPI
from .api.applications_api import ApplicationsAPI
from .api.admin_api import AdminAPI
from .api.query_api import QueryAPI
from .client import Client
from .admin import Admin
from .entity import Entity
from .entity_builder import EntityBuilder
from .query import Query
from .transaction import Transaction
from .application import Application

client: Client = None


def connect(api_key: str, host: str = "https://entitygraph.azurewebsites.net", ignore_ssl: bool = False):
    global client
    client = Client(api_key=api_key, host=host, ignore_ssl=ignore_ssl)
