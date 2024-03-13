import hashlib
import logging

from entitygraph.namespace_map import namespace_map
from rdflib import URIRef

logger = logging.getLogger(__name__)


def uri_is_valid_predicate(uri: (str, URIRef)) -> bool:
    """
    Validates a given URI using the namespace map.

    :return: Boolean, indicating, that the given URI is a valid predicate for usage in the entitygraph.
    """
    if isinstance(uri, URIRef):
        uri = str(uri)

    if not isinstance(uri, str):
        logger.error(f"The given URI must be of types string or URIRef. Got {type(uri)} instead.")
        raise ValueError(f"The given URI must be of types string or URIRef. Got {type(uri)} instead.")

    for key in namespace_map:
        if uri.startswith(key):
            return True

    return False


def uri_ref_to_prefixed(url: URIRef) -> str:
    """
    Converts a URIRef into a prefix using the namespace_map.

    :param url: A URIRef (e.g. URIRef("https://schema.org/name") or "SDO.name).

    :return: The prefix for the given URIRef.
    """
    if not isinstance(url, URIRef):
        logger.error(f"Expected URIRef got {type(url)} instead.")
        raise ValueError(f'Invalid input "{url}". '
                         f'Expected a URIRef instance, e.g., URIRef("https://schema.org/name") or "SDO.name"')

    url_str = str(url)

    for key in namespace_map:
        if url_str.startswith(key):
            return url_str.replace(key, f"{namespace_map[key]}.")

    logger.error(f"The given URIRef {url} is not part of the namespace map.")
    raise ValueError(f'URL "{url}" does not match any namespace in the namespace_map. '
                     f'Please make sure the URL is correct.')


def generate_value_identifier(predicate: str, value: str) -> str:
    """
    Generates a value identifier from predicate and value as strings using SHA-256 hash.

    :param predicate: A predicate allowed in the entitygraph.
    :param value: A string.

    :return: The generated value identifier (SHA-256 hash).
    """
    # Check for None property or value
    if not isinstance(predicate, str):
        logger.error(f"Property must be a string. Got {type(predicate)} instead.")
        raise ValueError(f"Property must be a string. Got {type(predicate)} instead.")
    if not isinstance(value, str):
        logger.error(f"Value must be a string. Got {type(value)} instead.")
        raise ValueError(f"Value must be a string. Got {type(value)} instead.")

    try:
        combined_string = predicate + value
        # Calculate SHA-256 hash of the combined string
        sha256_hash = hashlib.sha256(combined_string.encode()).hexdigest()
        return sha256_hash

    except Exception as e:
        logger.error(f"Error generating value identifier from predicate '{predicate}' and value '{value}'.")
        raise ValueError(f"Error generating value identifier: {str(e)}")



