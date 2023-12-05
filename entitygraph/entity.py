import re
import json
import logging
import entitygraph

from entitygraph.namespace_map import namespace_map
from entitygraph.values import ValuesContainer
from pathlib import Path
from random import randint
from rdflib import Graph, URIRef, RDF
from requests import Response
from typing import List, BinaryIO, TextIO
from urllib.parse import urlparse


# This will be the new entity that is going to replace the current Entity class.
# To ensure functionality until the new Entity class is fully implemented,
# the old Entity and EntityIterable classes will stay unchanged.
# Since some python scrips always download the current develop version of the entitygraph client,
# it is important that before pushing the changes to develop,
# an (at least small) guide is created to ensure a quick and easy update.
class EntityNEW:
    """
    The first and foremost change between the current Entity class implementation is the dependency upon the
    application class (Application in application.py).

    The old code did assume, that an Entity instantiation is always preceded by an application instantiation.
    Therefore the application label was set from the outside.

    This behavior will be changed in the new Entity class, making the instantiation of an application class optional.
    Since an application label is still required for calling the API, it will now be a part of the constructor.

    Another important change is, that Entities MUST be instantiated with an existing ID. It is therefore necessary,
    that all Constructor-Methods check, if the ID exists.
    Entities must, however, still implement lazy loading, which means that aside form the initial ID check, all
    data will be loaded on usage.
    To implement lazy loading, the Entity Object will implement properties, that call the entitygraph API on first
    usage and saves the result in a private property (starting with an underscore). For reference see the self.types.

    To create new Entities, the EntityBuilder class must be used. Once an Entity is build, it will automatically
    return an Entity Object.
    """
    def __init__(self, application_label: str, id_: str):
        self.application_label = application_label
        self._id = id_

        self._check_id()

        self._types = None
        self.values = ValuesContainer()

    @property
    def types(self) -> list[str]:
        """
        All types of this Entity.

        :return: A list of all the types of this Entity.
        """
        if self._types is None:
            self._types = self._get_own_types()
        return self._types

    @property
    def key(self) -> str:
        """
        Property for the id without any prefixes.

        :return: The key.
        """
        if '.' in self.id:
            return self.id.rsplit('.', 1)[-1]
        else:
            return self.id

    @property
    def id(self) -> str:
        """
        Property for the full id.

        :return: The ID.
        """
        return self._id

    def _check_id(self):
        """
        This method calls the entitygraph API to ensure, that the ID given in a Constructor-Method exists.
        """
        raise NotImplementedError()

    def _get_own_types(self) -> list[str]:
        """
        Load this Entities types from the entitygraph API.

        :return: A list of all the types of this Entity.
        """
        raise NotImplementedError()

    def load_all_data(self):
        """
        Fully loads the entire entity from the entitygraph, including all values and details.
        """
        # The full data must be parsed into this entities properties
        raise NotImplementedError()






class EntityIterable:
    def __init__(self, application_label: str, property_: str = None):
        self.application_label: str = application_label
        self.property: str = property_
        self.cache: List[Entity] = []

    def __getitem__(self, item):
        if isinstance(item, slice):
            start = item.start or 0
            stop = item.stop or 10
            step = item.step or 1

            if step != 1:
                raise ValueError('Step values other than 1 are not supported')

            off = start
            lim = stop - start
        elif isinstance(item, int):
            off = 0
            lim = item
        else:
            off = 0
            lim = 10

        endpoint = 'api/entities'
        params = {'limit': lim, 'offset': off}
        headers = {'X-Application': self.application_label, 'Accept': 'application/ld+json'}
        entity_list = entitygraph.base_api_client.make_request('GET', endpoint, headers=headers, params=params).json()['@graph']

        for entity in entity_list:
            parsed_url = urlparse(entity['@id'])
            path_parts = parsed_url.path.strip('/').split('/')
            entity_id = path_parts[-1] if len(path_parts) > 0 else None

            # TODO After Entity rework, the instantiation of the Entity Object must be adjusted
            new_entity = Entity()
            new_entity._id = entity_id
            new_entity._application_label = self.application_label
            self.cache.append(entity_list)

        return self.cache


class Entity:
    
    def __init__(self, data: Graph | str | dict = None, format: str = 'turtle', scope = "default", main_type = None):
        logging.debug("Please use the EntityBuilder to create entity objects")
        self.__updated: bool = False
        self._id: str = None
        self._application_label: str = scope
        self._main_type = main_type

        # Section from-graph
        if isinstance(data, Graph):
            self.__graph: Graph = data
        else:
            if format == 'turtle':
                self.__graph: Graph = Graph().parse(data=data, format='turtle',
                                                    encoding='utf-8') if data is not None else None
            elif format == 'json-ld':
                self.__graph: Graph = Graph().parse(data=data, format='json-ld',
                                                    encoding='utf-8') if data is not None else None
            elif format == 'n3':
                self.__graph: Graph = Graph().parse(data=data, format='n3',
                                                    encoding='utf-8') if data is not None else None
            else:
                raise ValueError(f"Unsupported format: {format}")

    def __check_id(self):
        if not self._id:
            raise Exception(
                "This entity has not been saved yet or does not exist. Please call .save() first to save the entity or use .get_by_id() to retrieve an existing entity.")

    def __lazy_load(self) -> 'Entity':
        if self.__graph is None or self.__updated:
            return self.refresh()

    def __str__(self):
        return self.turtle()

    def as_graph(self) -> Graph:
        self.__lazy_load()
        return self.__graph

    def turtle(self) -> str:
        self.__lazy_load()
        return self.__graph.serialize(format='turtle')

    def json(self) -> dict:
        self.__lazy_load()
        return json.loads(self.__graph.serialize(format='json-ld'))

    def n3(self) -> str:
        self.__lazy_load()
        return self.__graph.serialize(format='n3')

    @property
    def key(self) -> str: 
        if '.' in self.identifier:
            return self.identifier.rsplit('.', 1)[-1]
        return self.identifier

    @property
    def identifier(self) -> str: 
        self.__check_id()
        return self._id

    @property
    def uri(self) -> URIRef:
        base_url: str = entitygraph.base_api_client.base_url.rstrip("/")
        return URIRef(f"{base_url}/api/s/{self._application_label}/entities/{self.identifier}")

    def __uriref_to_prefixed(self, url: URIRef) -> str:
        if not isinstance(url, URIRef):
            raise ValueError(
                f'Invalid input "{url}". Expected a URIRef instance, e.g., URIRef("https://schema.org/name") or "SDO.name"')

        url_str = str(url)

        for key in namespace_map:
            if url_str.startswith(key):
                return url_str.replace(key, f"{namespace_map[key]}.")

        raise ValueError(
            f'URL "{url}" does not match any namespace in the namespace_map. Please make sure the URL is correct or update the namespace_map.')

    def save(self, encode=True) -> 'Entity':
        if self._id:
            raise Exception("This entity has already been saved. Please use other methods to modify the entity.")

        content = self.turtle()

        if encode: 
            content = content.encode(encoding="UTF-8")
            

        endpoint = 'api/entities'
        headers = {'X-Application': self._application_label, 'Content-Type': "text/turtle", 'Accept': "text/turtle"}
        response: Response = entitygraph.base_api_client.make_request('POST', endpoint, headers=headers, data=content)

        # identifier = entity.json()["https://w3id.org/av360/megt#inserted"]["@id"]

        g = Graph().parse(data=response.text, format='turtle')
        
        for sub in g.subjects(RDF.type, self._main_type): 
            if self._id:
                raise Exception("Multiple entities of same type in response, unique entity id cannot be inferred.")       
            self._id = Entity.extract_local_name(s=str(sub))

        return self

    def refresh(self) -> 'Entity':
        """
        Retrieves the entity from the API and updates the local Entity object
        """
        self.__check_id()

        endpoint = f'api/entities/{self._id}'
        headers = {'X-Application': self._application_label, 'Accept': 'text/turtle'}
        response: Response = entitygraph.base_api_client.make_request('GET', endpoint, headers=headers)

        self.__graph = Graph().parse(data=response.text, format='turtle')
        self.__updated = False
        return self

    def get_by_id(self, entity_id: str) -> 'Entity':
        tmp = Entity()
        tmp._id = entity_id
        tmp._application_label = self._application_label

        return tmp

    def get_all(self, property: URIRef = None) -> EntityIterable:
        return EntityIterable(self._application_label,
                              self.__uriref_to_prefixed(property) if property else None)

    def delete(self) -> None:
        self.__check_id()

        endpoint = f'api/entities/{self._id}'
        headers = {'X-Application': self._application_label, 'Accept': "text/turtle"}
        entitygraph.base_api_client.make_request('DELETE', endpoint, headers=headers)

    def delete_by_id(self, entity_id: str) -> None:
        endpoint = f'api/entities/{entity_id}'
        headers = {'X-Application': self._application_label, 'Accept': "text/turtle"}
        entitygraph.base_api_client.make_request('DELETE', endpoint, headers=headers)

    def set_value(self, property: URIRef, value: str | URIRef, language: str = 'en') -> 'Entity':
        """
        Sets a specific value. If the value exceeds a certain length, it will be automatically stored as content

        :param property: Property (qualified URL)
        :param value: Value (no longer than 255 chars)
        :param language: Language (defaults to "en")
        """
        if not value: 
            return self

        if len(value) > 1000:
            return self.set_content(property=property, content=value, language=language)


        self.__check_id()
        
        # Convert property to prefixed version
        prefixed = self.__uriref_to_prefixed(property)

        if isinstance(value, URIRef):
            value = '<' + str(value) + '>'

        endpoint = f"api/entities/{self._id}/values/{prefixed}"
        headers = {
            'X-Application': self._application_label,
            'Content-Type': 'text/plain',
            'Accept': 'text/turtle'
        }
        params = {}
        if language:
            params['lang'] = language

        entitygraph.base_api_client.make_request('POST', endpoint, headers=headers, data=value,
                                                 params=(params if params else None))
        self.__updated = True
        return self

    def set_content(self, property: URIRef, content: Path | BinaryIO | TextIO | bytes | str,
                    filename: str = None):
        """
        Sets content.

        :param property: Property (qualified URL)
        :param content: Content (can be file, path, binary, string)
        :param filename: Filename (defaults to "file_{random}.txt")
        """
        if not content: 
            return self
        
        self.__check_id()

        # Convert property to prefixed version
        prefixed = self.__uriref_to_prefixed(property)

        if isinstance(content, str):
            content_data = content.encode()
        elif isinstance(content, Path):
            with content.open('rb') as f:
                content_data = f.read()
        elif isinstance(content, (BinaryIO, TextIO)):
            content_data = content.read()
        else:
            content_data = content

        if not filename:
            filename = f'file_{randint(1, 999999999)}.txt'

        endpoint = f"api/entities/{self._id}/values/{prefixed}"
        headers = {
            'X-Application': self._application_label,
            'Content-Type': 'application/octet-stream',
            'Accept': 'text/turtle'
        }
        params = {'filename': filename}

        entitygraph.base_api_client.make_request('POST', endpoint, headers=headers, data=content_data,
                                                 params=params)
        self.__updated = True
        return self

    def remove_value(self, property: URIRef, language: str = 'en'):
        """
        Removes a property value.

        :param property: Property (qualified URL)
        :param language: Language (defaults to "en")
        """
        self.__check_id()

        # Convert property to prefixed version
        prefixed = self.__uriref_to_prefixed(property)

        endpoint = f"api/entities/{self._id}/values/{prefixed}"
        headers = {'X-Application': self._application_label, 'Accept': 'text/turtle'}
        params = {'lang': language} if language else None

        entitygraph.base_api_client.make_request('DELETE', endpoint, headers=headers, params=params)

        self.__updated = True
        return self

    def create_edge(self, property: URIRef, target: 'Entity'):
        """
        Create edge to existing entity (within the same dataset)

        :param property: Property (qualified URL)
        :param target: Target entity (must be saved first)
        """
        if not target.identifier:
            raise Exception("Target entity has not been saved yet or does not exist. Please call .save() first to save the entity or use .get_by_id() to retrieve an existing entity.")

        # Convert property to prefixed version
        prefixed = self.__uriref_to_prefixed(property)

        endpoint = f"api/entities/{self.key}/relations/{prefixed}/{target.key}"
        headers = {'X-Application': self._application_label, 'Accept': 'text/turtle'}
        entitygraph.base_api_client.make_request('PUT', endpoint, headers=headers)

        self.__updated = True
        return self

    def delete_edge(self, property: URIRef, target: 'Entity'):
        """
        Delete edge to existing entity (within the same dataset)

        :param property: Property (qualified URL)
        :param target: Target entity (must be saved first)
        """
        self.__check_id()

        if not target._id:
            raise Exception(
                "Target entity has not been saved yet or does not exist. Please call .save() first to save the entity or use .get_by_id() to retrieve an existing entity.")

        # Convert property to prefixed version
        prefixed = self.__uriref_to_prefixed(property)

        endpoint = f"api/entities/{self._id}/links/{prefixed}/{target._id}"
        headers = {'X-Application': self._application_label, 'Accept': 'text/turtle'}
        entitygraph.base_api_client.make_request('DELETE', endpoint, headers=headers)

        self.__updated = True
        return self

    def embed(self, property: URIRef, data: str | dict):
        self.__check_id()

        # Convert property to prefixed version
        prefixed = self.__uriref_to_prefixed(property)

        endpoint = f'api/entities/{self._id}/{prefixed}'
        headers = {'X-Application': self._application_label, 'Content-Type': 'text/turtle', 'Accept': 'text/turtle'}
        entitygraph.base_api_client.make_request('POST', endpoint, headers=headers, data=data)

        self.__updated = True
        return self


    @staticmethod
    def match_entity_identifier(identifier: str) -> tuple[str, str] | None:
        """Checks whether the given string is a valid identifier (can be encoded with scope)

        Args:
            identifier (str): the string to check

        Returns:
            tuple[str, str] | None:  A tuple with identifier and scope, or none
        """
        match : re.Match[str] = re.match(r'^(?:([a-z]+)\.)?([a-zA-Z0-9]{8})$', identifier)
        if match: 
            return match.groups()
        else: 
            return None
            

    @staticmethod
    def match_internal_urn(identifier: str) -> tuple[str, str] | None:
        """ Checks whether the given identifier is an internal urn (usually coming back from SPARQL queries) 
            in the following format: 'urn:pwid:meg:e:{scope}.{id}'
        Args:
            tuple[str, str] | None:  A tuple with identifier and scope, or none
        """
        match = re.match(r'^urn:pwid:meg:e:(?:([a-z]+)\.)?([a-zA-Z0-9_-]{8})$', identifier, re.ASCII)
        if match is None:
            return
        else:
            return match.groups()
       
    @staticmethod
    def extract_local_name(s: str) -> str | None:
        """
        Function to determine if 's' is a URN or URI and extract the local name.

        Args:
        s (str): A string that is potentially a URN or URI.

        Returns:
        str: The local name extracted from the URN or URI, or None if 's' is neither.
        """    
        # Regular expression for a URN (simplified)
        urn_regex = r'^urn:[a-zA-Z0-9][a-zA-Z0-9-]{0,31}:[a-zA-Z0-9()+,\-.:=@;$_!*\'%/?#]+$'
        
        # Regular expression for a URI (simplified)
        uri_regex = r'^[a-zA-Z][a-zA-Z0-9+.-]*://'

        if re.match(urn_regex, s):
            # For a URN, the local name is after the last colon
            return s.split(':')[-1]
        elif re.match(uri_regex, s):
            # For a URI, the local name is typically the part after the last slash
            return s.split('/')[-1]
        else:
            return None

    @classmethod
    def from_entity_identifier(cls, identifier: str, scope: str = "default") -> 'Entity':
        """Creates an entity object for the given identifier. Will not check if the entity exists. 

        Args:
            identifier (str): an entity identifier
            scope (str, optional): The optional scope. Will be overriden by scope embedded in identifier. Defaults to "default".

        Raises:
            Exception: _description_
            Exception: _description_

        Returns:
            Entity: the (lazy loaded) entity 
        """
        matched = Entity.match_entity_identifier(identifier)
        if matched is None:
            matched = Entity.match_internal_urn(identifier)

        if matched: 
            tmp = Entity()            
            tmp._id = matched[1]
            if matched[0]: 
                tmp._application_label = matched[0]
            else: 
                tmp._application_label = scope
            return tmp
        else: 
            raise Exception(f"Invalid entity identifier: '{str}'")
