import entitygraph

from entitygraph.details import Details
from entitygraph.entity import Entity
from entitygraph.utils import uri_is_valid_predicate
from rdflib import URIRef, SDO


# This class contains the content vor a single predicate.
# The content can be a relation between different Entities, or simply literals.
class Value:
    """
    A single value used in the Entities.
    """
    def __init__(self, predicate: URIRef):
        if not uri_is_valid_predicate(predicate):
            raise ValueError(f"Cannot add Value for given predicate {predicate}. The given predicate must be a valid "
                             f"predicate in the context of the entity graph (i.e. part of the namespace_map).")

        self._predicate = predicate
        self._content: (list, None) = None
        # An indication, that the content of the Value Object has been changed.
        self._updated = False

    @property
    def predicate(self):
        """
        Getter for this instance's property.
        """
        return self._predicate

    def _load_content(self) -> list:
        """
        Loads all values for this instance's property.

        :return: List of all values. If no values exist jet, an empty list if returned.
        """
        raise NotImplementedError()

    @property
    def content(self) -> list:
        """
        Getter for this Values content with lazy loading.

        :return: List of all values.
        """
        if self._content is None or self._updated:
            self._content = self._load_content()
        return self._content

    def add_content(self, content: (str, Entity)):
        """
        Adds the given content.

        :param content: Either a literal or an entity object.
        """
        if isinstance(content, Entity):
            self._add_relation(content)
        else:
            self._add_literal(content)

    def get_details_by_value_identifier(self, value_identifier) -> dict[Details]:
        """
        Accesses all details using the value identifier.

        :param value_identifier: A value identifier to specify which details to return.

        :return: A dictionary containing a details for the identifier.
        """
        raise NotImplementedError()

    # TODO Before working on this method, it need to be cleared up, how exactly value identifiers are created/loaded.
    def get_details_by_content(self, content) -> dict[Details]:
        """
        Accesses all details using the exact content.

        :param content: A literal or Entity
        :return: A dictionary containing a details for the content.
        """

    # This method should upload the content directly to the entitygraph
    def _add_literal(self, literal: str):
        """
        Adds the given literal.

        :param literal: A literal to add to this predicate.
        """
        # All methods which change the content must set self._updated to True
        # This ensures, that if the content is accessed, it is properly (re-)loaded.
        self._updated = True

        # All methods that add content should directly upload the content to the entitygraph API.
        raise NotImplementedError()

    # This method should upload the content directly to the entitygraph
    def _add_relation(self, entity: Entity):
        """
        Creates a link between this entity and the target entity.

        :param entity: An entity to add a connection to.
        """
        # All methods which change the content must set self._updated to True
        # This ensures, that if the content is accessed, it is properly (re-)loaded.
        self._updated = True

        # All methods that add content should directly upload the content to the entitygraph API.
        raise NotImplementedError()

    # It is important to ensure that this method works for both different use cases of
    # only having one literal/relation vs multiple literals/relations.
    def get_details(self, something_to_identify_the_specific_content) -> Details:
        """
        Method for accessing a single detail for a single literal/relation.

        :return: An instance of the Detail class.
        """
        raise NotImplementedError()


# The following class is a container for multiple Value class objects.
# Usage as follows:
"""
values = ValuesContainer
some_entity = Entity("label", "id")
# Adding a literal or relation
values[SDO.keywords] = "Math"
values[SDO.knowsAbout] = some_entity
# Accessing a Value
my_value: Value = values[SDO.keywords]
"""
# Some suggestions for additional methods to add to the class:
# - methods for removing entire values or single literals/relations
# - maybe a clear method for easier refreshing (fully loading all data from the graph)
# - maybe a class method for instantiating the ValuesContainer with already available data
# It is also important to remember that all methods should focus on situations where the Entity containing the
# ValueContainer already exists in the entitygraph.
# Methods for creating new Entities should be implemented in the EntityBuilder/ValueBuilder classes.
class ValuesContainer:
    """
    Container for multiple Values with lazy loading.
    """
    def __init__(self):
        self._values = {}

    def __getattr__(self, predicate: (str, URIRef)) -> Value:
        """
        Getter for a Value.

        :param predicate: A valid predicate in the context of the entitygraph.

        :return: A Value Object.
        """
        if predicate not in self._values:
            self._values[predicate] = Value(predicate)

        return self._values[predicate]

    def __setattr__(self, predicate: (str, URIRef), content: str):
        """
        Setter for a Value.

        :param predicate: A valid predicate in the context of the entitygraph.
        :param content: A literal.
        """
        value = self.__getattr__(predicate)
        value.add_content(content)


values = ValuesContainer
values[SDO.keywords] = "Math"
























