import logging
import requests
import entitygraph

from entitygraph.utils import uri_is_valid_predicate
from rdflib import URIRef,SDO
from requests import Response

logger = logging.getLogger(__name__)


class Entity:
    def __init__(self, application_label: str, id_: str | None = None):
        """Represents an entity in the context of the entity graph

        The first and foremost change between the current Entity class implementation is the dependency upon the
        application class (Application in application.py).

        The old code did assume, that an Entity instantiation is always preceded by an application instantiation.
        Therefore, the application label was set from the outside.

        This behavior will be changed in the new Entity class, making the instantiation of an application class optional.
        Since an application label is still required for calling the API, it will now be a part of the constructor.

        Entities must, however, still implement lazy loading, which means that aside form the initial ID check, all
        data will be loaded on usage.
        To implement lazy loading, the Entity Object will implement properties, that call the entitygraph API on first
        usage and saves the result in a private property (starting with an underscore).

        :param application_label: Application label in the context of the entity graph.
        :type application_label: str
        :param id_: Entity ID in the context of the entity graph. None for no entity id (default).
        :type id_: str | None
        """

        self._application_label = application_label
        self._id = id_

        # Check, if id is valid
        if self._id is not None:
            self._load_types()
        else:
            self._types: (list[URIRef], None) = None

        self.values: entitygraph.ValueContainer = entitygraph.ValueContainer(self._application_label, entity_id=self._id)
        self.relations = entitygraph.RelationContainer(self._application_label, entity_id=self._id)

        if self._id is not None:
            logger.debug(f"Created entity for existing id {self._id} on application {self._application_label}.")
        else:
            logger.debug(f"Created new entity on {self._application_label} (not jet saved!).")

    @property
    def application_label(self):
        """Getter for this Value's entity ID
        """

        return self._application_label

    @property
    def key(self) -> str:
        """Property for the id without any prefixes
        """

        if self._id is not None:
            if '.' in self.id:
                return self.id.rsplit('.', 1)[-1]
            else:
                return self.id
        else:
            raise ValueError("New entity does not have a key jet.")

    @property
    def id(self) -> str:
        """Property for the full id
        """

        return self._id

    @property
    def types(self) -> list[URIRef]:
        """All types of this Entity
        """

        if self._id is not None and self._types is None:
            self._types = self._load_types()
        return self._types

    @types.setter
    def types(self, new_type: str | URIRef):
        """Add a new type to a new entity

        New type can only be added to new entities, that have not yet been saved on the entity graph.

        :param new_type: One of the types of this entity.
        :type new_type: str | URIRef
        """

        if self._id is not None:
            logger.error("Cannot add new type to an already existing entity.")
            raise ValueError("Cannot add new type to an already existing entity.")

        if isinstance(new_type, str):
            new_type = URIRef(new_type)
        elif not isinstance(new_type, URIRef):
            logger.error("Cannot add new type to an already existing entity.")
            raise ValueError("Cannot add new type to an already existing entity.")

        if not uri_is_valid_predicate(new_type):
            raise ValueError(f"Cannot add Type {new_type}. The given predicate must be a valid "
                             f"predicate in the context of the entity graph (i.e. part of the namespace_map).")

        if self._types is None:
            self._types = [new_type]
        else:
            self._types.append(new_type)

    @property
    def uri_ref(self) -> URIRef:
        """The URI of this entity
        """

        if self._id is not None:
            base_url: str = entitygraph.base_api_client.base_url.rstrip("/")
            return URIRef(f"{base_url}/api/s/{self._application_label}/entities/{self.id}")
        else:
            logger.error("Cannot access URI of an entity, that has not been saved jet.")
            raise ValueError("Cannot access URI of an entity, that has not been saved jet.")

    def _load_types(self) -> list[URIRef]:
        """Load this entity's types from the entitygraph API

        :return: A list of all the types of this Entity.
        :type: list[URIRef]
        """

        entity_info = self._load_entity()

        try:
            return [entity_type for entity_type in entity_info["type"] if entity_type.startswith("http")]
        except KeyError:
            logger.error("Did not find expected key '@type' in response.")
            raise KeyError("Missing key @type.")

    def _load_entity(self) -> dict:
        """This method calls the entitygraph API to ensure, that the ID given in a Constructor-Method exists

        :return: A dictionary representing this entity.
        :rtype: dict
        """

        endpoint = f'api/entities/{self._id}'
        headers = {'X-Application': self._application_label, 'accept': 'application/json'}
        response: Response = entitygraph.base_api_client.make_request('GET', endpoint, headers=headers)
        try:
            response.raise_for_status()
        except requests.HTTPError as http_e:
            logger.error(f"Error when trying to reach {endpoint} when checking id.")
            raise http_e

        return response.json()

    # The following methods might be implemented in the future, if needed
    def load_all_values(self):
        """
        Load all existing predicates of this entity from the entitygraph.
        Both the content and the details are not loaded.
        """
        raise NotImplementedError()

