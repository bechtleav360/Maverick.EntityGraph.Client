from abc import ABC, abstractmethod
from entitygraph.utils import uri_is_valid_predicate


class IContainerAbstract(ABC):
    def __init__(self, application_label: str, predicate: str, entity_id: str | None = None):
        """Init for IContainerAbstract interface

        :param application_label: Application label in the context of the entity graph.
        :type application_label: str
        :param predicate: Predicate in the context of the entity graph.
        :type predicate: str
        :param entity_id: Entity ID in the context of the entity graph. None for no entity id (default).
        :type entity_id: str | None
        """

        if not uri_is_valid_predicate(predicate):
            raise ValueError(f"Cannot add Value for given predicate {predicate}. The given predicate must be a valid "
                             f"predicate in the context of the entity graph (i.e. part of the namespace_map).")

        self._application_label = application_label
        self._predicate = predicate
        self._entity_id = entity_id

    @property
    def application_label(self):
        """Getter for the label of the application of the entitygraph
        """

        return self._application_label

    @property
    def entity_id(self):
        """Getter for this ValueContainers entity ID
        """

        return self._entity_id

    @property
    def predicate(self) -> str:
        """Getter for this instance's predicate
        """

        return self._predicate

    @classmethod
    @abstractmethod
    def create(cls, predicate: str, **kwargs):
        """Abstract constructor for classes implementing the IContainer interface

        :param predicate: Some content to be saved.
        :type predicate: str

        :return: Class instance.
        """

        raise NotImplementedError()

    @abstractmethod
    def has_changes(self) -> bool:
        """Indicates, that this classes data has been updated.
        """

        raise NotImplementedError()

