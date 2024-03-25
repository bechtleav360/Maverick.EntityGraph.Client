import entitygraph
import logging
import requests

from abc import abstractmethod
from entitygraph.utils import uri_ref_to_prefixed
from rdflib import URIRef
from requests import Response
from typing import Set

logger = logging.getLogger(__name__)


# This class contains the content vor a single predicate.
# The content can be a relation between different Entities, or simply literals (=value).
class ValuesAndRelationsBase(entitygraph.IContainerAbstract):
    # The things one does to get code completion to work...
    class DetailsDict(dict):
        def __getitem__(self, value: str) -> entitygraph.DetailContainer:
            """Does nothing except set the return type.
            """
            return super().__getitem__(value)

        def __setitem__(self, value, content: entitygraph.DetailContainer):
            """Does nothing except set the value type.
            """
            super().__setitem__(value, content)

    def __init__(self, application_label: str, predicate: str, entity_id: str | None= None, language: str = "de"):
        """A single predicate/value or predicate/relation combination used in an entity.

        This class represents a combination of predicate and one (or multiple) literals, or of predicate and one
        (or multiple) literals. Literals/Relations are stored in a dynamically loaded list. This class does not
        support any logic specific to a predicate!
        This class and its derivatives are being instantiated automatically in the context of an entity.

        :param application_label: Application label in the context of the entity graph.
        :type application_label: str
        :param predicate: Predicate in the context of the entity graph.
        :type predicate: str
        :param entity_id: Entity ID in the context of the entity graph. None for no entity id (default).
        :type entity_id: str | None
        :param language: Default language for this value/relation.
        """

        super().__init__(application_label, predicate, entity_id=entity_id)
        self.language = language
        self._content_lst_private: list | None = None
        self._details = ValuesAndRelationsBase.DetailsDict()

        # String, indicating the api path. Either "values" or "relations".
        self._api_path: str | None = None
        # An indication, that the content of the Value Object has been changed.
        self._updated = False

    @property
    def _content_lst(self) -> list:
        """Getter for the content list with lazy loading.

        Cannot be used to change/set the content.
        """

        # Only check remote, if entity already exists
        # But only, if content has not been set jet
        if self._entity_id is not None and self._content_lst_private is None:
            self._content_lst_private = self._load_content()

        # Otherwise set it to a list
        if self._content_lst_private is None:
            self._content_lst_private = []

        return self._content_lst_private

    @classmethod
    def create(cls, predicate, **kwargs):
        """
        Override of abstract class crete.

        :param predicate: Predicate in the context of the entity graph.
        :type predicate: str
        :param kwargs: Additional parameters for this class:
            Required:
                - application_label
            Optional:
                - entity_id

        :return: An instance of this class.
        """

        if "application_label" not in kwargs:
            raise KeyError("Missing application label for creating a new Value.")

        if "entity_id" in kwargs:
            return cls(kwargs["application_label"], predicate, entity_id=kwargs["entity_id"])
        else:
            return cls(kwargs["application_label"], predicate)

    @abstractmethod
    def content_lst(self) -> list:
        """A private method that returns all content.
        """

        raise NotImplementedError()

    def new_content(self) -> list[str]:
        """Get all added content.
        """

        # TODO Check ID
        return [content for content in self._content_lst if content not in self._load_content()]

    def removed_content(self) -> list[str]:
        """Get all removed content.
        """

        # TODO Check ID
        return [content for content in self._load_content() if content not in self._content_lst]

    def _load_content(self) -> list:
        """Loads all values for this instance's property.

        :return: List of all values. If no values exist jet, an empty list if returned.
        :rtype: list
        """
        prefixed_predicate = uri_ref_to_prefixed(URIRef(self._predicate))

        # TODO CHANGE API!!!
        if self._api_path == "values":
            endpoint = f'api/entities/{self._entity_id}/{self._api_path}?prefixedProperty={prefixed_predicate}'
            headers = {'X-Application': self._application_label, 'accept': 'application/json'}
        else:
            endpoint = f'api/entities/{self._entity_id}/{self._api_path}/{prefixed_predicate}'
            headers = {'X-Application': self._application_label, 'accept': 'application/json'}

        try:
            response: Response = entitygraph.base_api_client.make_request('GET', endpoint, headers=headers)
            response.raise_for_status()
        except requests.HTTPError as http_e:
            logger.error(f"Error when trying to load content from {endpoint} for value {self._predicate}.")
            raise http_e

        if self._api_path == "values":
            return [value["value"] for value in response.json()]
        else:
            return []

    def _add_content(self, *content_lst, allowed_types=str):
        """Adds the given content.

        :param content_lst: One or multiple literal(s).
        :param allowed_types: A set of all types allowed as content.
        """
        if isinstance(*content_lst, tuple):
            content_lst = list(*content_lst)
        else:
            content_lst = [str(*content_lst)]

        if not isinstance(allowed_types, tuple):
            allowed_types = [allowed_types]

        bad_content_lst = [content for content in content_lst if type(content) not in allowed_types]
        if bad_content_lst:
            for bad_content in bad_content_lst:
                logger.error(f"Function 'add_content' got unexpected type {type(bad_content)}.")
            raise TypeError(f"Content for Values can only be of types str, int or float.")
        else:
            # Helper set for identifying duplicates
            seen = set()
            duplicates = [x for x in self._content_lst + content_lst if x in seen or seen.add(x)]
            if duplicates:
                for content in duplicates:
                    logger.error(f"Function 'add_content' got duplicate content {content}.")
                raise ValueError(f"{duplicates} already in content list.")

            self._content_lst_private.extend(content_lst)
            self._updated = True

    def remove_content(self, *content_lst, allowed_types: Set = str, remove_all: bool = False):
        """Removes content from this value.

        :param content_lst: A list of content to be removed.
        :type content_lst: sequence of str
        :param allowed_types: A set of all types allowed as content.
        :type allowed_types: Set
        :param remove_all: Boolean. If True, all content is deleted and content_lst is ignored.
        :type remove_all: bool
        """

        if remove_all:
            if self._content_lst:
                self._updated = True
            self._content_lst_private = []
        else:
            if isinstance(*content_lst, tuple):
                content_lst = list(*content_lst)
            elif isinstance(*content_lst, list):
                content_lst = content_lst[0]
            else:
                content_lst = [str(*content_lst)]

            bad_content_lst = [content for content in content_lst if content not in self._content_lst]
            if bad_content_lst:
                for bad_content in bad_content_lst:
                    if not isinstance(allowed_types, tuple):
                        allowed_types = [allowed_types]
                    if bad_content in allowed_types:
                        logger.error(f"Function 'remove_content' got unexpected content {bad_content}.")
                    else:
                        logger.error(f"Function 'remove_content' got unexpected content type {type(bad_content)}.")
                raise ValueError(f"Got content to be removed, that did not exist.")
            else:
                for content in content_lst:
                    self._content_lst.remove(content)
                self._updated = True

    def _reset_content(self):
        """Allows the user to reset the content of a value to its remote current remote state.
        """

        self._content_lst_private = None
        self._updated = False

    def has_changes(self) -> bool:
        """Indicates, that this Value has been updated.
        """

        return self._updated

    def get_details(self, value: str) -> entitygraph.DetailContainer:
        """Getter for the details for one value.

        :param value: The literal the details are attached to.
        :type value: str

        :return: All details for one value.
        """

        if value not in self._content_lst:
            logger.error(f"Predicate {self.predicate} does not contain value {value}.")
            raise ValueError(f"Value {value} does not exist for predicate {self.predicate}.")

        if value in self._details:
            return self._details[value]

    def add_detail(self, value: str, detail_predicate: str, content: str):
        """Add new detail for a single value.

        :param value: Literal to add a detail to.
        :type value: str
        :param detail_predicate: The predicate of this detail.
        :type detail_predicate: str
        :param content: The content of the detail to add.
        :type content: str
        """

        if value not in self._content_lst:
            logger.error(f"Predicate {self.predicate} does not contain value {value}.")
            raise ValueError(f"Value {value} does not exist for predicate {self.predicate}.")

        if value not in self._details:
            self._details[value] = entitygraph.DetailContainer(
                self._application_label,
                entity_id=self._entity_id,
                value_predicate=self._predicate,
                value=value
            )

        self._details[value][detail_predicate].set_content(content)



