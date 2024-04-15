from json import JSONDecodeError

import entitygraph
import json
import logging
import requests

from entitygraph.utils import predicate_to_uri, uri_ref_to_prefixed, generate_value_identifier
from rdflib import URIRef
from typing import List, Tuple, Dict, Iterator

logger = logging.getLogger(__name__)

# List of all allowed URI's to save details under
# TODO: Load list from online recourse or let API take care of evaluation
allowed_details_properties = [
    "confidence",
    "explanation",
    "model",
    "created",
    "status",
    "updated",
    "cosSimilarity",
    "method",
    "script"
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

        if self._content is None:
            self._content = ""

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

    def has_changes(self) -> bool:
        """Indicates, that this Value has been updated
        """

        # Did anything happen to the content of this detail
        if self._updated:
            # Is this a new entity (id=None)...
            if self.entity_id is None:
                # ...and is any content set?
                return True if self.content else False
            # If the entity exists, compare to remote, if anything has changed
            else:
                return not self._load_detail() == self.content
        else:
            return False

    def _load_detail(self) -> str:
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

        # TODO Rework, if API is updated
        # 400/404 means detail does not exist, which, in the context of the entitygraph, means the detail is empty.
        if response.status_code in [400, 404]:
            return ""

        if response.status_code < 300:
            for loaded_value in response.json():
                if loaded_value["metadata"]["hash"] == self.value_identifier:
                    if self._predicate.split(".")[-1] in loaded_value["details"]:
                        try:
                            return json.loads(loaded_value["details"][self._predicate.split(".")[-1]])
                        except JSONDecodeError:
                            return loaded_value["details"][self._predicate.split(".")[-1]]

            # If nothing was found, return an empty string
            return ""

        try:
            response.raise_for_status()
        except requests.HTTPError as http_e:
            logger.error(f"Error when trying to load details from {endpoint} for value {self._value_predicate}.")
            raise http_e

    def set_content(self, content: str | int | float):
        """Adds the given content

        :param content: A literal.
        :type content: str | int | float
        """

        if type(content) not in (str, int, float, dict):
            logger.error(f"Function 'add_content' got unexpected type {type(content)}.")
            raise TypeError(f"Content for Details can only be of types str, int or float.")

        if self.content:
            self._remove_old = True

        self._content = content
        self._updated = True

    def remove_content(self, raise_error_if_not_exists: bool = True):
        """Removes content from this detail

        Since None type is used for identifying, if the content has not been accessed jet, it is set to an empty string,
        indicating, that it should be deleted.

        :param raise_error_if_not_exists: By default, this function raises an error, if called, when no content has
            been set. If this parameter is set to false, no error will be raised.
        :type raise_error_if_not_exists: bool
        """

        if self.content:
            self._updated = True
            self._content = ""
            if self.entity_id is not None:
                self._remove_old = True
        elif raise_error_if_not_exists:
            raise ValueError(f"Tried to delete non-existent detail with predicate {self.predicate} for value predicate "
                             f"{self.value_predicate} of entity {self.entity_id}.")


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

        super().__init__(application_label, entity_id=entity_id, **kwargs)
        self._icontainer = Detail
        self._content: dict[str, Detail] = {}

    def __getitem__(self, predicate: str | URIRef) -> Detail:
        """Getter for a Detail object

        :param predicate: A valid predicate in the context of the entitygraph.
        :type predicate: str | URIRef

        :return: A Detail object.
        :rtype: Detail
        """
        if uri_ref_to_prefixed(predicate).split(".")[-1] not in allowed_details_properties:
            logger.error(f"Invalid predicate {predicate}. Allowed predicates are {allowed_details_properties}")
            raise ValueError(f"Invalid predicate {predicate}")

        return super().__getitem__(predicate)

    def __setitem__(self, predicate: str | URIRef, literal: str):
        """Setter for a Value object

        :param predicate: A valid predicate in the context of the entitygraph.
        :type predicate: str | URIRef
        :param literal: A literal.
        :type literal: str
        """

        self.__getitem__(predicate).set_content(literal)

    def _load_all_predicates(self, relative_path: str):
        """Override of helper for allowing loading of all predicates (for iteration)

        :param relative_path: The relative path of the value/relation/detail.
        :type relative_path: str
        """

        prefixed_predicate = uri_ref_to_prefixed(URIRef(self._additional_class_arguments["value_predicate"]))
        value_identifier = generate_value_identifier(
                self._additional_class_arguments["value_predicate"], self._additional_class_arguments["value"])

        endpoint = f'api/entities/{self._entity_id}/values?prefixedProperty={prefixed_predicate}'
        headers = {'X-Application': self._application_label, 'accept': 'application/json'}
        response: requests.Response = entitygraph.base_api_client.make_request(
            'GET',
            endpoint,
            headers=headers,
            params={"valueIdentifier": value_identifier}
        )

        try:
            response.raise_for_status()
        except requests.HTTPError as http_e:
            logger.error(f"Error when trying to load predicates from {endpoint}.")
            raise http_e

        for loaded_value in response.json():
            if loaded_value["metadata"]["hash"] == value_identifier:
                for detail in loaded_value["details"]:
                    self.__getitem__(f"eav.{detail}")
                break

    def __iter__(self) -> Iterator[Detail]:
        """Allow iteration

        :return: The predicates of the saved data.
        :rtype: Iterator[Detail]
        """

        if self._entity_id is not None:
            self._load_all_predicates("values")
        return iter(value for value in self._content.values())

    def items(self) -> List[Tuple[str, str]]:
        """Analog to dict.items()

        :return: List of tuples of predicate and content.
        :rtype: List[Tuple[str, List[str]]]
        """

        return [(detail.predicate, detail.content) for detail in self if detail.content]

    def to_dict(self) -> Dict[str, str]:
        """Convert to dictionary

        Converts all values into a dictionary of the form predicate: content, for each predicate in the entity.

        :rtype: Dict[str, str]
        """

        return {predicate_to_uri(predicate): content for predicate, content in self.items()}
