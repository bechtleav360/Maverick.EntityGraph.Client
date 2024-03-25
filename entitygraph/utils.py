import hashlib
import logging

from entitygraph.namespace_map import namespace_map
from rdflib import URIRef

logger = logging.getLogger(__name__)


def uri_is_valid_predicate(predicate: str | URIRef) -> bool:
    """Validates a given URI using the namespace map

    :param predicate: A predicate in the context of the entity graph.
    :type predicate: str | URIRef

    :return: Boolean, indicating, that the given URI is a valid predicate for usage in the entitygraph.
    :rtype: bool
    """

    if isinstance(predicate, URIRef):
        predicate = str(predicate)

    if not isinstance(predicate, str):
        logger.error(f"The given URI must be of types string or URIRef. Got {type(predicate)} instead.")
        raise ValueError(f"The given URI must be of types string or URIRef. Got {type(predicate)} instead.")

    if not predicate.startswith("http"):
        if predicate.split(".")[0] in namespace_map.values():
            return True
    else:
        for key in namespace_map:
            if predicate.startswith(key):
                return True

    return False


def uri_ref_to_prefixed(predicate: str | URIRef) -> str:
    """Converts a URIRef into a prefix using the namespace_map

    :param predicate: A URIRef (e.g. URIRef("https://schema.org/name"), a URL or SDO.name).
    :type predicate: str | URIRef

    :return: The prefix for the given URIRef.
    :rtype: str
    """

    if isinstance(predicate, URIRef):
        predicate = str(predicate)
    elif not isinstance(predicate, str):
        logger.error(f"Expected URIRef got {type(predicate)} instead.")
        raise ValueError(f'Invalid input "{predicate}". '
                         f'Expected a URIRef instance, e.g., URIRef("https://schema.org/name") or "SDO.name"')

    if not predicate.startswith("http"):
        if predicate.split(".")[0] not in namespace_map.values():
            logger.error(f"Unknown predicate {predicate}.")
            raise ValueError("Unknown predicate")

        return predicate
    else:
        for key in namespace_map:
            if predicate.startswith(key):
                return predicate.replace(key, f"{namespace_map[key]}.")

        logger.error(f"The given URIRef {predicate} is not part of the namespace map.")
        raise ValueError(f'URL "{predicate}" does not match any namespace in the namespace_map. '
                         f'Please make sure the URL is correct.')


def generate_value_identifier(predicate: str, value: str) -> str:
    """Generates a value identifier from predicate and value as strings using SHA-256 hash

    :param predicate: A predicate allowed in the entitygraph.
    :type predicate: str
    :param value: A string.
    :type value: str

    :return: The generated value identifier (SHA-256 hash).
    :rtype: str
    """
    # Check for None property or value
    if not isinstance(predicate, str):
        logger.error(f"Property must be a string. Got {type(predicate)} instead.")
        raise ValueError(f"Property must be a string. Got {type(predicate)} instead.")
    if not isinstance(value, str):
        logger.error(f"Value must be a string. Got {type(value)} instead.")
        raise ValueError(f"Value must be a string. Got {type(value)} instead.")

    corrected_predicate = predicate
    if not predicate.startswith("http"):
        for key, value_ in namespace_map.items():
            if value_ == predicate.split('.')[0]:
                corrected_predicate = key + predicate.split('.')[1]
                break

    if not corrected_predicate.startswith("http"):
        raise ValueError(f"Invalid predicate {corrected_predicate}")

    try:
        combined_string = corrected_predicate + value
        # Calculate SHA-256 hash of the combined string
        sha256_hash = hashlib.sha256(combined_string.encode()).hexdigest()
        return sha256_hash

    except Exception as e:
        logger.error(f"Error generating value identifier from predicate '{predicate}' and value '{value}'.")
        raise ValueError(f"Error generating value identifier: {str(e)}")



