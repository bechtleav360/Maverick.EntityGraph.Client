import entitygraph
import logging

from rdflib import URIRef

logger = logging.getLogger(__name__)


# TODO Add Relation functionality
# This class contains the content vor a single predicate.
# The content can be a relation between different Entities, or simply literals.
class Relation(entitygraph.ValuesAndRelationsBase):
    def __init__(self, application_label: str, predicate: URIRef, entity_id: str | None = None):
        """A single value used in the Entities

        :param application_label: Application label in the context of the entity graph.
        :type application_label: str
        :param predicate: Predicate in the context of the entity graph.
        :type predicate: str
        :param entity_id: Entity ID in the context of the entity graph. None for no entity id (default).
        :type entity_id: str | None
        """

        super().__init__(application_label, predicate, entity_id=entity_id)
        self._api_path = "relations"

    def content_lst(self) -> list[URIRef]:
        """Allows access on a copy of all content of this relation.

        :return: A copy of the content_lst of this class.
        :rtype: list[URIRef]
        """

        return [URIRef(content) for content in self._content_lst]

    def add_uri_refs(self, *refs: URIRef | str):
        """Add one or more relation for this predicate.

        :param refs: One or more relations.
        :type refs: URIRef | str
        """

        self._add_content(*refs, allowed_types=(URIRef, str))


class RelationContainer(entitygraph.Container):
    def __init__(self, application_label: str, entity_id: str | None = None, **kwargs):
        """Override of Container constructor, adding the Relation class

        :param application_label: Application label in the context of the entity graph.
        :type application_label: str
        :param entity_id: Entity ID in the context of the entity graph. None for no entity id (default).
        :type entity_id: str | None
        :param kwargs: Additional keyword arguments for instantiating Relation class instances:
            Optional:
                - entity_id
        """

        super().__init__(Relation, application_label, entity_id=entity_id, **kwargs)

    def __getitem__(self, predicate: str | URIRef) -> Relation:
        """Getter for a Relation object

        :param predicate: A valid predicate in the context of the entitygraph.
        :type predicate: str | URIRef

        :return: A Relation object.
        :rtype: Relation
        """

        return super().__getitem__(predicate)

    def __setitem__(self, predicate: str | URIRef, *literals):
        """Setter for a Relation object

        :param predicate: A valid predicate in the context of the entitygraph.
        :type predicate: str | URIRef
        :param literals: One pr more literals.
        """

        self.__getitem__(predicate).add_uri_refs(*literals)

    def load_all_predicates(self):
        """Allows loading all predicates (for iteration).
        """

        relations_info = self._load_all_predicates("relations")

        for value_obj in relations_info:
            # Getting the item once instantiates a new Value object
            self.__getitem__(value_obj["property"])

