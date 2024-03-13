import entitygraph
import json
import logging
import requests

from entitygraph.entity.container.container import Container
from entitygraph.entity.container.icontainer import IContainerAbstract
from rdflib import URIRef, SDO
from entitygraph.utils import uri_is_valid_predicate, uri_ref_to_prefixed, generate_value_identifier

logger = logging.getLogger(__name__)

# List of all allowed URI's to save details under
# TODO: Load list from online recourse
allowed_details_properties = [
    "https://w3id.org/eav/confidence",
    "https://w3id.org/eav/created",
    "https://w3id.org/eav/model",
    "https://w3id.org/eav/status",
    "https://w3id.org/eav/updated"
]


class Detail(IContainerAbstract):
    """
    This class will contain all details for a single literal/relation in a predicate.
    In principal, details are key: value pairs. It makes therefore sense to implement them in a similar way to
    a python dictionary (specifically using __getitem__ and __setitem__ methods).

    It is important to create some whitelist to ensure only well defined keys are used for details.
    If someone wants to add a new keyword, it should be done using whatever well defined process exists for that.
    Optimally that list can be loaded from some easily accessible online source.

    It might also make sense to include descriptions for each key (again: dynamically loaded) if this helps using them
    properly.
    """
    def __init__(
            self,
            application_label: str,
            predicate: str,
            value_predicate: str,
            value: str,
            entity_id: (str, None) = None
    ):
        super().__init__(application_label, entity_id=entity_id)

        self._value_predicate = value_predicate
        self._value_identifier = generate_value_identifier(self._value_predicate, value)
        self._predicate = predicate
        self._updated = False

        self._content: (str, int, float, None) = None

    @property
    def value_predicate(self) -> str:
        """
        Getter for the predicate of the value this details belongs to.

        :return: The predicate of the value this details belongs to.
        """
        return self._value_predicate

    @property
    def predicate(self) -> str:
        """
        Getter for the predicate of this detail.

        :return: The predicate of this detail.
        """
        return self._predicate

    @property
    def value_identifier(self):
        """
        Getter for this detail's value identifier.

        :return: This detail's value identifier.
        """
        return self._value_identifier

    @property
    def content(self):
        """
        Getter for this detail's content.

        :return: This detail's content.
        """
        return self._content

    @classmethod
    def create(cls, predicate, **kwargs):
        """
        Override of abstract class crete.

        :param predicate: Some content to be saved.
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
        """
        Indicates, that this Value has been updated.

        :return: Updated boolean
        """
        return self._updated

    def _load_all_details(self):
        """
        Load all existing details from the entitygraph.
        """
        logger.info(f"Reading details for predicate {self.predicate} for entity {self._entity_id} on application "
                    f"{self.application_label}.")

        prefixed = uri_ref_to_prefixed(URIRef(self._value_predicate))

        endpoint = f'api/entities/{self._entity_id}/values?prefixedProperty={prefixed}'
        headers = {'X-Application': self._application_label, 'accept': 'application/json'}
        response = entitygraph.base_api_client.make_request(
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

        return json.loads(response.text)

    def set_content(self, content: (str, int, float)):
        """
        Adds the given content.

        :param content: A literal.
        """
        if content not in (str, int, float):
            logger.error(f"Function 'add_content' got unexpected type {type(content)}.")
            raise TypeError(f"Content for Details can only be of types str, int or float.")

        # Only check remote, if entity already exists
        if self._entity_id is not None and self._content is None:
            self._content = self._load_all_details()

        # If this is the first added content and nothing got loaded, set details to empty dict
        self._content = content
        self._updated = True

    def remove_content(self):
        """
        Removes content from this detail.
        Since None type is used for identifying if the content has not been accessed jet, it is set to an empty string,
        indicating, that is should be deleted.
        """
        if self._entity_id is not None and self._content is None:
            self._content = self._load_all_details()

        self._content = ""
        self._updated = True


class DetailContainer(Container):
    def __init__(self, application_label: str, entity_id: (str, None) = None, **kwargs):
        super().__init__(Detail, application_label, entity_id=entity_id, **kwargs)

    def __getitem__(self, predicate: (str, URIRef)) -> Detail:
        return super().__getitem__(predicate)

