import entitygraph
import logging
import requests

from abc import ABC, abstractmethod
from entitygraph.utils import uri_ref_to_prefixed
from rdflib import URIRef
from requests import Response
from typing import Type, Tuple, List

logger = logging.getLogger(__name__)


class Container(ABC):
    def __init__(
            self,
            icontainer: Type[entitygraph.IContainerAbstract],
            application_label: str,
            entity_id: (str, None) = None,
            **kwargs
    ):
        """Container for multiple Values with lazy loading

        :param icontainer: A class that inherits from IContainerAbstract.
        :type icontainer: Type[IContainerAbstract]
        :param application_label: Application label in the context of the entity graph.
        :type application_label: str
        :param entity_id: Entity ID in the context of the entity graph. None for no entity id (default).
        :type entity_id: str | None
        :param kwargs: Additional keyword arguments for instantiating IContainerAbstract class instances.
        """

        self._icontainer = icontainer
        self._application_label = application_label
        self._entity_id = entity_id

        self._content: dict[str, Type[entitygraph.IContainerAbstract]] = {}
        self._additional_class_arguments = kwargs

    @property
    def application_label(self):
        """Getter for the application label in the context of the entity graph
        """

        return self._application_label

    @property
    def entity_id(self):
        """Getter for entity ID in the context of the entity graph
        """

        return self._entity_id

    @abstractmethod
    def load_all_predicates(self):
        """Allows loading all predicates (for iteration)
        """

        raise NotImplementedError()

    def _load_all_predicates(self, relative_path: str):
        """Helper for allowing loading of all predicates (for iteration)

        :param relative_path: The relative path of the value/relation/detail.
        :type relative_path: str
        """

        endpoint = f'api/entities/{self._entity_id}/{relative_path}'
        headers = {'X-Application': self._application_label, 'accept': 'application/json'}

        try:
            response: Response = entitygraph.base_api_client.make_request('GET', endpoint, headers=headers)
            response.raise_for_status()
        except requests.HTTPError as http_e:
            logger.error(f"Error when trying to load predicates from {endpoint}.")
            raise http_e

        return response.json()

    def __getitem__(self, predicate: str | URIRef) -> entitygraph.IContainerAbstract.__subclasses__():
        """Getter for a IContainer object

        :param predicate: A valid predicate in the context of the entitygraph.
        :type predicate: str | URIRef

        :return: A IContainer object.
        :rtype: entitygraph.IContainerAbstract.__subclasses__()
        """

        predicate = uri_ref_to_prefixed(predicate)
        if predicate not in self._content:
            self._content[predicate] = self._icontainer.create(
                predicate,
                application_label=self._application_label,
                entity_id=self.entity_id,
                **self._additional_class_arguments
            )

        return self._content[predicate]

    def __iter__(self) -> entitygraph.IContainerAbstract.__subclasses__():
        """Allow iteration

        :return: The predicates of the saved data.
        :rtype: entitygraph.IContainerAbstract.__subclasses__()
        """

        if self._entity_id is not None:
            self.load_all_predicates()
        return iter([value for value in self._content.values()])

    def items(self) -> List[Tuple[str, List[str]]]:
        """Analog to dict.items()

        :return: List of tuples of predicate and content.
        :rtype: List[Tuple[str, List[str]]]
        """

        return [(predicate, content.content_lst()) for predicate, content in self._content.items()]





