from typing import List, Tuple

import entitygraph
import logging

from rdflib import URIRef

logger = logging.getLogger(__name__)


# This class contains the content vor a single predicate.
# The content can be a relation between different Entities, or simply literals.
class Value(entitygraph.ValuesAndRelationsBase):
    def __init__(self, application_label: str, predicate: URIRef, entity_id: str | None = None):
        """A single value used in an entity.

        :param application_label: Application label in the context of the entity graph.
        :type application_label: str
        :param predicate: Predicate in the context of the entity graph.
        :type predicate: str
        :param entity_id: Entity ID in the context of the entity graph. None for no entity id (default).
        :type entity_id: str | None
        """

        super().__init__(application_label, predicate, entity_id=entity_id)
        self._api_path = "values"

    def content_lst(self) -> list[str]:
        """Allows access on a copy of all content of this relation.

        :return: A copy of the content_lst of this class.
        :rtype: list[str]
        """
        return [content for content in self._content_lst]

    def add_literals(self, *literals: str):
        """Add one or more relation for this predicate.

        :param literals: One or more relations.
        :type literals: URIRef | str
        """

        self._add_content(*literals)


class ValueContainer(entitygraph.Container):
    def __init__(self, application_label: str, entity_id: str | None = None, **kwargs):
        """Override of Container constructor, adding the Value class

        :param application_label: Application label in the context of the entity graph.
        :type application_label: str
        :param entity_id: Entity ID in the context of the entity graph. None for no entity id (default).
        :type entity_id: str | None
        :param kwargs: Additional keyword arguments for instantiating Relation class instances:
            Optional:
                - entity_id
        """
        super().__init__(application_label, entity_id=entity_id, **kwargs)
        self._icontainer = Value
        self._content: dict[str, Value] = {}

    def __getitem__(self, predicate:str | URIRef) -> Value:
        """Getter for a Value object

        :param predicate: A valid predicate in the context of the entitygraph.
        :type predicate: str | URIRef

        :return: A Value object.
        :rtype: Value
        """

        return super().__getitem__(predicate)

    def __setitem__(self, predicate: str | URIRef, *literals):
        """Setter for a Value object

        :param predicate: A valid predicate in the context of the entitygraph.
        :type predicate: str | URIRef
        :param literals: One pr more literals.
        """

        self.__getitem__(predicate).add_literals(*literals)

    def load_all_predicates(self):
        """
        Allows loading all predicates (for iteration).
        """
        values_info = self._load_all_predicates("values")

        for value_obj in values_info:
            # Getting the item once instantiates a new Value object
            self.__getitem__(value_obj["property"])

    def items(self) -> List[Tuple[str, List[str]]]:
        """Analog to dict.items()

        :return: List of tuples of predicate and content.
        :rtype: List[Tuple[str, List[str]]]
        """

        return [(predicate, content.content_lst()) for predicate, content in self._content.items()]

