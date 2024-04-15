__version__ = "0.1.4"

from entitygraph.admin import Admin
from entitygraph.base_client import BaseApiClient
from entitygraph.entity.entity import Entity
from entitygraph.entity.container.icontainer import IContainerAbstract
from entitygraph.entity.container.container import Container
from entitygraph.entity.values_and_relations.details.detail import Detail, DetailContainer
from entitygraph.entity.values_and_relations.values_and_relations_base import ValuesAndRelationsBase
from entitygraph.entity.values_and_relations.value import Value, ValueContainer
from entitygraph.entity.values_and_relations.relation import Relation, RelationContainer
from entitygraph.transaction import Transaction
from entitygraph.application import Application

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


def connect(api_key: str, host: str = "https://graph.q14.net", ignore_ssl: bool = False):
    """
    Creates the BaseAPIClient instance necessary for connecting to the entitygraph API.

    :param api_key: Authorization key.
    :param host: The host address of the entitygraph API. Default: https://entitygraph.azurewebsites.net.
    :param ignore_ssl: For ignoring ssl verification, if necessary. Default: False.
    """
    global __base_api_client
    __base_api_client = BaseApiClient(api_key=api_key, base_url=host, ignore_ssl=ignore_ssl)

