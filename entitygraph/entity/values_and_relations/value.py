import entitygraph
import logging
import requests

from abc import ABC
from entitygraph.entity.container.container import Container
from entitygraph.entity.values_and_relations.details.detail import Detail, DetailContainer
from entitygraph.utils import uri_is_valid_predicate, uri_ref_to_prefixed
from entitygraph.entity.container.icontainer import IContainerAbstract
from entitygraph.entity.values_and_relations.values_and_relations_base import ValuesAndRelationsBase
from rdflib import URIRef
from requests import Response

logger = logging.getLogger(__name__)


# This class contains the content vor a single predicate.
# The content can be a relation between different Entities, or simply literals.
class Value(ValuesAndRelationsBase):
    """
    A single value used in the Entities.
    """
    def __init__(self, application_label: str, predicate: URIRef, entity_id: (str, None) = None):
        super().__init__(application_label, predicate, entity_id=entity_id)
        self._api_path = "values"

    def content_lst(self) -> list[str]:
        """
        Allows access on a copy of all content of this Value/Relation.

        :return: A copy of the content_lst of this class.
        """
        return [content for content in self._content_lst]

    def add_literals(self, *literals: str):
        """
        Add one or more literal for this predicate.

        :param literals: One or more literals.
        """
        self._add_content(*literals)


class ValueContainer(Container):
    def __init__(self, application_label: str, entity_id: (str, None) = None, **kwargs):
        super().__init__(Value, application_label, entity_id=entity_id, **kwargs)

    def __getitem__(self, predicate: (str, URIRef)) -> Value:
        return super().__getitem__(predicate)

    def __setitem__(self, predicate: (str, URIRef), *literals):
        self.__getitem__(predicate).add_literals(*literals)

    def load_all_predicates(self):
        """
        Allows loading all predicates (for iteration).
        """
        self._load_all_predicates("values")

