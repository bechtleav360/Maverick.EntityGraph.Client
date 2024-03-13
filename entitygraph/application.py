import entitygraph
import json
import logging

from entitygraph.utils import uri_ref_to_prefixed, generate_value_identifier
from typing import List
from rdflib import BNode, Graph, Literal, RDF, URIRef
from requests import Response

logger = logging.getLogger(__name__)


class ApplicationNEW:
    @staticmethod
    def create_entity(entity: entitygraph.EntityNEW):
        """
        Create a new entity from an entity object.

        :param entity: A entity object without an ID.

        :return: The given entity.
        """
        if entity.id is not None:
            logger.error("Cannot create new entity, since it already exists. Use 'save_entity' instead.")
            raise ValueError("Cannot create new entity, since it already exists. Use 'save_entity' instead.")

        # Instantiate graph
        graph = Graph()
        node = BNode()

        # Add entity types to teh graph
        for entity_type in entity.types:
            graph.add((node, RDF.type, URIRef(entity_type)))

        # Add values to the graph
        for predicate, content_lst in entity.values.items():
            for literal in content_lst:
                graph.add((node, URIRef(predicate), Literal(literal)))

        # Add relations to the graph
        for predicate, content_lst in entity.relations.items():
            for uri_ref in content_lst:
                graph.add((node, URIRef(predicate), uri_ref))

        # Save entity
        entity_as_turtle = graph.serialize(format='turtle')
        logger.info("Creating new graph:")
        logger.info(f"{entity_as_turtle}")
        print(f"{entity_as_turtle}")

        headers = {
            'X-Application': entity.application_label,
            'Content-Type': "text/turtle",
            'Accept': "application/ld+json"
        }
        response: Response = entitygraph.base_api_client.make_request(
            'POST',
            'api/entities',
            headers=headers,
            data=entity_as_turtle.encode(encoding="UTF-8")
        )

        response.raise_for_status()
        new_entity_id = response.json()["@graph"][0]["@graph"][0]["@id"].split(":")[-1]
        logger.info(f"Created new entity with id {new_entity_id}")

        return entitygraph.EntityNEW(entity.application_label, id_=new_entity_id)

    @staticmethod
    def save_entity(entity: entitygraph.EntityNEW):
        """
        Save all changes for an already existing entity.

        :param entity: An entity object.

        :return: The given entity object.
        """
        def add_value_to_entity_remote(path: str, item: entitygraph.ValuesAndRelationsBase, content):
            prefixed = uri_ref_to_prefixed(URIRef(item.predicate))
            endpoint = f"api/entities/{item.entity_id}/{path}/{prefixed}"
            headers = {
                'X-Application': item.application_label,
                'Content-Type': 'text/plain',
                'Accept': 'application/ld+json'
            }
            params = {"languageTag": item.language}
            response: Response = entitygraph.base_api_client.make_request(
                'POST',
                endpoint,
                headers=headers,
                data=content,
                params=params
            )
            response.raise_for_status()

        def remove_value_from_entity_remote(path: str, item: entitygraph.ValuesAndRelationsBase, content):
            prefixed = uri_ref_to_prefixed(URIRef(item.predicate))
            endpoint = f"api/entities/{item.entity_id}/{path}/{prefixed}"
            headers = {
                'X-Application': item.application_label,
                'Accept': 'application/ld+json'
            }
            params = {
                "languageTag": item.language,
                "valueIdentifier": generate_value_identifier(item.predicate, content)
            }
            response: Response = entitygraph.base_api_client.make_request(
                'DELETE',
                endpoint,
                headers=headers,
                data=content,
                params=params
            )
            response.raise_for_status()

        for value in entity.values:
            for new_content in value.new_content():
                add_value_to_entity_remote("values", value, new_content)
            for removed_content in value.removed_content():
                remove_value_from_entity_remote("values", value, removed_content)

        for relation in entity.relations:
            for new_content in relation.new_content():
                add_value_to_entity_remote("relations", relation, new_content)
            for removed_content in relation.removed_content():
                remove_value_from_entity_remote("relations", relation, removed_content)

        return entity

    @staticmethod
    def delete_entity(entity: entitygraph.EntityNEW):
        """
        Delete an entity.

        :param entity: An entity object.
        """
        endpoint = f"api/entities/{entity.id}"
        headers = {
            'X-Application': entity.application_label,
            'Accept': 'application/ld+json'
        }
        response: Response = entitygraph.base_api_client.make_request(
            'DELETE',
            endpoint,
            headers=headers
        )
        response.raise_for_status()

    @staticmethod
    def delete_entity_by_id(entity_id: str, application_label: str):
        """
        Delete an entity.

        :param entity_id: Id od the entity to delete.
        :param application_label: The application label of the entity.
        """
        endpoint = f"api/entities/{entity_id}"
        headers = {
            'X-Application': application_label,
            'Accept': 'application/ld+json'
        }
        response: Response = entitygraph.base_api_client.make_request(
            'DELETE',
            endpoint,
            headers=headers
        )
        response.raise_for_status()


class Application:
    def __init__(self, label: str = None, flags: dict = {"isPersistent": True, "isPublic": True},
                 configuration: dict = {}):
        self.label: str = label
        self.key: str = None
        self.flags: dict = flags
        self.configuration: dict = configuration

    def __check_key(self):
        if not self.key:
            raise Exception(
                "This application has not been saved yet or does not exist. Please call .save() first to save the entity or use .get_by_label() to retrieve an existing application.")

    def __str__(self):
        return f"Application(label={self.label}, key={self.key}, flags={self.flags}, configuration={self.configuration})"

    def EntityBuilder(self, type: URIRef = None) -> entitygraph.EntityBuilder:
        entity_builder = entitygraph.EntityBuilder(type)
        entity_builder._application_label = self.label

        return entity_builder

    def BulkBuilder(self, entity_builders: list[EntityBuilder]) -> 'BulkBuilder':
        bulk_builder = entitygraph.BulkBuilder(entity_builders)
        bulk_builder._application_label = self.label

        return bulk_builder

    def Entity(self, data: Graph | str | dict = None, format: str = "turtle") -> 'Entity':
        entity = entitygraph.Entity(data=data, format=format)
        entity._application_label = self.label

        return entity

    def Query(self) -> 'Query':
        query = entitygraph.Query()
        query._application_label = self.label

        return query

    def Admin(self) -> 'Admin':
        admin = entitygraph.Admin()
        admin._application_label = self.label

        return admin

    def save(self) -> 'Application':
        endpoint = "api/applications"
        headers = {'Content-Type': 'application/json'}
        response: Response = entitygraph.base_api_client.make_request(
            'POST',
            endpoint,
            headers=headers,
            data=json.dumps({
              "label": self.label,
              "flags": self.flags,
              "configuration": self.configuration
            })
        )

        self.key = response.json().get("key")

        return self

    def delete(self):
        self.__check_key()

        endpoint = f"api/applications/{self.key}"
        return entitygraph.base_api_client.make_request('DELETE', endpoint)

    def delete_by_label(self, label: str):
        app = self.get_by_label(label)
        if app is not None:
            endpoint = f"api/applications/{self.key}"
            return entitygraph.base_api_client.make_request('DELETE', endpoint)

    def delete_by_key(self, key: str):
        endpoint = f"api/applications/{key}"
        return entitygraph.base_api_client.make_request('DELETE', endpoint)

    def get_all(self) -> List['Application']:
        endpoint = "api/applications"
        response: Response = entitygraph.base_api_client.make_request('GET', endpoint)

        cache = []
        for x in response.json():
            app = Application(label=x.get('label'),
                              flags=x.get('flags'),
                              configuration=x.get('configuration'),
                              )
            app.key = x.get('key')
            cache.append(app)

        return cache

    def get_by_key(self, key: str) -> 'Application':
        endpoint = f"api/applications/{key}"
        response: Response = entitygraph.base_api_client.make_request('GET', endpoint)

        response: dict = response.json()

        if response is not None:
            app = Application(label=response.get('label'),
                              flags=response.get('flags'),
                              configuration=response.get('configuration'),
                              )
            app.key = response.get('key')
            return app

    def get_by_label(self, label: str) -> 'Application':
        endpoint = "api/applications"
        response: Response = entitygraph.base_api_client.make_request('GET', endpoint)

        for x in response.json():
            if x.get('label') == label:
                app = Application(label=x.get('label'),
                                  flags=x.get('flags'),
                                  configuration=x.get('configuration'),
                                  )
                app.key = x.get('key')
                return app

    def create_subscription(self, label: str) -> str:
        """
        :param label: Subscription label
        :return: Subscription key
        """
        self.__check_key()
        endpoint = f"api/applications/{self.key}/subscriptions"
        headers = {'Content-Type': 'application/json'}
        response: Response = entitygraph.base_api_client.make_request(
            'POST',
            endpoint,
            headers=headers,
            data={"label": label}
        )

        return response.json()['key']

    def get_subscriptions(self) -> List[dict]:
        self.__check_key()

        endpoint = f"api/applications/{self.key}/subscriptions"
        response: Response = entitygraph.base_api_client.make_request('GET', endpoint)

        return response.json()

    def delete_subscription(self, label: str):
        self.__check_key()

        endpoint = f"api/applications/{self.key}/subscriptions/{label}"
        return entitygraph.base_api_client.make_request('DELETE', endpoint)

    def set_configuration(self, key: str, value: str | dict):
        """
        Sets or updates a configuration parameter

        :param key: Configuration key
        :param value: Configuration value
        """
        self.__check_key()

        endpoint = f"api/applications/{self.key}/configuration/{key}"
        return entitygraph.base_api_client.make_request('POST', endpoint,
                                                        data=value if isinstance(value, str) else json.dumps(value))

    def delete_configuration(self, key: str):
        self.__check_key()

        endpoint = f"api/applications/{self.key}/configuration/{key}"
        return entitygraph.base_api_client.make_request('DELETE', endpoint)


if __name__ == '__main__':

    a = "test"

    print(f"{a=}")

    # id_ = "b7cki7px"
    # from rdflib import SDO
    # entitygraph.connect("Tzre7295T10z1K")
    #
    # entity = entitygraph.EntityNEW("default")
    # entity.types = SDO.LearningResource
    # entity.values[SDO.name] = "new test 2"
    #
    # new_entity = ApplicationNEW.create_entity(entity)
    # print(new_entity.id)
    # print(new_entity.types)
    # new_entity.values.load_all_predicates()
    # print(new_entity.values.items())
    # ApplicationNEW.delete_entity(new_entity)

    # entity_2 = entitygraph.EntityNEW("default", id_=id_)
    # entity_2.relations.load_all_predicates()

    # new_entity.relations[SDO.description] = entity_2
    # print(new_entity.relations.items())

    # entity_2.values[SDO.keywords].remove_content(['"a", 5', '"a"'])
    # print(entity_2.values[SDO.keywords].content_lst())

    # ApplicationNEW.save_entity(entity_2)

    # asd
    # app = Application("default")
    # e = app.EntityBuilder(SDO.LearningResource)
    # e.add_value(SDO.name, "test")
    # new_e = e.build()
    # print(new_e.key)
