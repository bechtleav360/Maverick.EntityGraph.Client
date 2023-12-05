import entitygraph


class Details:
    """
    This class will contain all details for a single literal/relation in a predicate.
    In principal, details are key: value pairs. It makes therefore sense to implement them in a similar way to
    a python dictionary (specifically using __getattr__ and __setattr__ methods).

    It is important to create some whitelist to ensure only well defined keys are used for details.
    If someone wants to add a new keyword, it should be done using whatever well defined precess exists for that.
    Optimally that list can be loaded from some easily accessible online source.

    It might also make sense to include descriptions for each key (again: dynamically loaded) if this helps using them
    properly.
    """
    def __init__(self, value_identifier=None):
        # The value identifier must not necessarily exist, if only one literal/relation exists for the predicate.
        self.value_identifier = value_identifier
        self._details = {}

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
