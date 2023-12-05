from entitygraph.namespace_map import namespace_map
from rdflib import URIRef


def uri_is_valid_predicate(uri: (str, URIRef)) -> bool:
    """
    Validates a given URI using the namespace map.

    :return: Boolean, indicating, that the given URI is a valid predicate for usage in the entitygraph.
    """
    if isinstance(uri, URIRef):
        uri = str(uri)

    if not isinstance(uri, str):
        raise ValueError(f"Given URI must be of types string or URIRef. Got {type(uri)} instead.")

    for key in namespace_map:
        if uri.startswith(key):
            return True

    return False

