import entitygraph


class Details:
    """
    This class will contain all details for a single literal/relation in a predicate.
    In principal, details are key: value pairs. It makes therefore sense to implement them in a similar way to
    a python dictionary (specifically using __getattr__ and __setattr__ methods).

    It is important to create some whitelist to ensure only well defined keys are used for details.
    If someone wants to add a new keyword, it should be done using whatever well defined process exists for that.
    Optimally that list can be loaded from some easily accessible online source.

    It might also make sense to include descriptions for each key (again: dynamically loaded) if this helps using them
    properly.
    """
    def __init__(self, entity_id: str, predicate: str, value_identifier: (str, None) = None):
        self._entity_id = entity_id
        self._predicate = predicate

        # The value identifier must not necessarily exist, if only one literal/relation exists for the predicate.
        # Also depending on which method will be chosen to create the identifier, it might be better to implement a
        # method that automatically creates/loads the identifier, rather then setting it in the constructor.
        self._value_identifier = value_identifier
        self._details = {}

    @property
    def entity_id(self):
        """
        Getter for this detail's entity ID.

        :return: The ID of the entity this detail belongs to.
        """
        return self._entity_id

    @property
    def predicate(self):
        """
        Getter for this detail's predicate.

        :return: The predicate of the value this detail belongs to.
        """
        return self._predicate

    # Since an edge case exists, where the value identifier can change, (The identifier is None, if the predicate has
    # only one literal/relation, but as soon as another is added, this identifier changes) it might be useful to
    # also add a setter or any kind of update for the identifier
    @property
    def value_identifier(self):
        """
        Getter for this detail's predicate.

        :return: The predicate of the value this detail belongs to.
        """
        return self._value_identifier

    def load_all_details(self):
        """
        Load all existing details from the entitygraph.
        """
        raise NotImplementedError()

    def __getattr__(self, key: str) -> str:
        """
        Getter for a detail.

        :param key: The key of a single detail.

        :return: Value of this detail.
        """
        raise NotImplementedError()

    def __setattr__(self, key: str, value: str):
        """
        Setter for a Value.

        :param key: A valid key for a detail.
        :param value: Some string.
        """
        raise NotImplementedError()
