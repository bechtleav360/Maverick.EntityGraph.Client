import entitygraph
import json
import logging
import requests

from rdflib import URIRef
from entitygraph.utils import uri_ref_to_prefixed, generate_value_identifier

logger = logging.getLogger(__name__)

# List of all allowed URI's to save details under
# TODO: Load list from online recourse
allowed_details_properties = [
    "confidence",
    "created",
    "model",
    "status",
    "updated"
]


class Detail(entitygraph.IContainerAbstract):
    def __init__(
            self,
            application_label: str,
            predicate: str,
            value_predicate: str,
            value: str,
            entity_id: str | None = None
    ):
        """Represents a single detail for a single literal/relation in a predicate

        :param application_label: Application label in the context of the entity graph.
        :type application_label: str
        :param predicate: A valid Details predicate.
        :type predicate: str
        :param value_predicate: Predicate of the value this detail belongs to.
        :type value_predicate: str
        :param value: The literal/relation this detail belongs to.
        :type value: str
        :param entity_id: Entity ID in the context of the entity graph. None for no entity id (default).
        :type entity_id: str | None
        """

        super().__init__(application_label, predicate, entity_id=entity_id)

        self._value_predicate = value_predicate
        self._value_identifier = generate_value_identifier(self._value_predicate, value)
        self._updated = False
        self._remove_old = False

        self._content: (str, int, float, None) = None

    @property
    def value_predicate(self) -> str:
        """Getter for the predicate of the value this details belongs to
        """

        return self._value_predicate

    @property
    def value_identifier(self) -> str:
        """Getter for this detail's value identifier
        """

        return self._value_identifier

    @property
    def content(self) -> str:
        """Getter for this detail's content
        """

        if self._entity_id is not None and self._content is None:
            self._content = self._load_detail()

        return self._content

    @property
    def remove_old(self) -> bool:
        """Getter for checking, if an old literal has to be removed
        """

        return self._remove_old

    @classmethod
    def create(cls, predicate, **kwargs):
        """Override of abstract class crete

        :param predicate: Some content to be saved.
        :type predicate: str
        :param kwargs: Additional parameters for this class:
            Required:
                - application_label,
                - value,
                - value_predicate
            Optional:
                - entity_id

        :return: An instance of this class.
        """

        if "application_label" not in kwargs:
            raise KeyError("Missing application label for creating a new Value.")
        if "value_predicate" not in kwargs:
            raise KeyError("Missing value predicate for creating a new Detail.")
        if "value" not in kwargs:
            raise KeyError("Missing value for creating a new Detail.")

        return cls(predicate=predicate, **kwargs)

    def content_lst(self) -> list[str]:
        """Allows access on a copy of all content of this value
        """

        return [json.dumps(self.content)]

    def has_changes(self) -> bool:
        """Indicates, that this Value has been updated
        """

        return self._updated

    def _load_detail(self) -> dict:
        """Load the content of this detail from the entitygraph
        """

        logger.info(f"Reading details for predicate {self.predicate} for entity {self._entity_id} on application "
                    f"{self.application_label}.")

        prefixed_predicate = uri_ref_to_prefixed(URIRef(self._value_predicate))

        endpoint = f'api/entities/{self._entity_id}/values?prefixedProperty={prefixed_predicate}'
        headers = {'X-Application': self._application_label, 'accept': 'application/json'}
        response: requests.Response = entitygraph.base_api_client.make_request(
            'GET',
            endpoint,
            headers=headers,
            params={"valueIdentifier": self._value_identifier}
        )

        try:
            response.raise_for_status()
        except requests.HTTPError as http_e:
            logger.error(f"Error when trying to load details from {endpoint} for value {self._value_predicate}.")
            raise http_e

        return [loaded_details for loaded_details in response.json()
                if response.json()["metadata"]["hash"] == self.value_identifier][0][self._predicate]

    def set_content(self, content: str | int | float):
        """Adds the given content

        :param content: A literal.
        :type content: str | int | float
        """

        if type(content) not in (str, int, float):
            logger.error(f"Function 'add_content' got unexpected type {type(content)}.")
            raise TypeError(f"Content for Details can only be of types str, int or float.")

        if self.content:
            self._remove_old = True

        self._content = str(content)
        self._updated = True

    def remove_content(self):
        """Removes content from this detail

        Since None type is used for identifying, if the content has not been accessed jet, it is set to an empty string,
        indicating, that it should be deleted.
        """

        if self.content:
            self._remove_old = True
            self._updated = True


class DetailContainer(entitygraph.Container):
    def __init__(self, application_label: str, entity_id: str | None = None, **kwargs):
        """Override of Container constructor, adding the Detail class

        :param application_label: Application label in the context of the entity graph.
        :type application_label: str
        :param entity_id: Entity ID in the context of the entity graph. None for no entity id (default).
        :type entity_id: str | None
        :param kwargs: Additional keyword arguments for instantiating Detail class instances:
            Required:
                - value,
                - value_predicate
            Optional:
                - entity_id
        """

        super().__init__(Detail, application_label, entity_id=entity_id, **kwargs)

    def __getitem__(self, predicate: str | URIRef) -> Detail:
        """Getter for a Detail object

        :param predicate: A valid predicate in the context of the entitygraph.
        :type predicate: str | URIRef

        :return: A Detail object.
        :rtype: Detail
        """

        return super().__getitem__(predicate)

    def load_all_predicates(self):
        """Allows loading all predicates (for iteration)
        """

        values_info = self._load_all_predicates("values")

        for value_obj in values_info:
            # Getting the item once instantiates a new Value object
            self.__getitem__(value_obj["property"])
