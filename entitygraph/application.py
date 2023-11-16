import json
from typing import Type, List

from rdflib import Graph, URIRef
from requests import Response

import entitygraph
from entitygraph import Entity, Query, Admin, EntityBuilder, BulkBuilder


class Application:
    def __init__(self, label: str = None, flags: dict = {"isPersistent": True, "isPublic": True},
                 configuration: dict = {}):
        if entitygraph._base_client is None:
            raise Exception(
                "Not connected. Please connect using entitygraph.connect(api_key=..., host=...) before using Application()")

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

    def EntityBuilder(self, type: URIRef = None) -> EntityBuilder:
        entity_builder = EntityBuilder(type)
        entity_builder._application_label = self.label

        return entity_builder

    def BulkBuilder(self, entity_builders: list[EntityBuilder]) -> 'BulkBuilder':
        bulk_builder = BulkBuilder(entity_builders)
        bulk_builder._application_label = self.label

        return bulk_builder

    def Entity(self, data: Graph | str | dict = None, format: str = "turtle") -> 'Entity':
        entity = Entity(data=data, format=format)
        entity._application_label = self.label

        return entity

    def Query(self) -> 'Query':
        query = Query()
        query._application_label = self.label

        return query

    def Admin(self) -> 'Admin':
        admin = Admin()
        admin._application_label = self.label

        return admin

    def save(self) -> 'Application':
        endpoint = "api/applications"
        headers = {'Content-Type': 'application/json'}
        response: Response = entitygraph._base_client.make_request('POST',
                                                                   endpoint,
                                                                   headers=headers,
                                                                   data=json.dumps({
                                                                      "label": self.label,
                                                                      "flags": self.flags,
                                                                      "configuration": self.configuration
                                                                  }))

        self.key = response.json().get("key")

        return self

    def delete(self):
        self.__check_key()

        endpoint = f"api/applications/{self.key}"
        return entitygraph._base_client.make_request('DELETE', endpoint)

    def delete_by_label(self, label: str):
        app = self.get_by_label(label)
        if app is not None:
            endpoint = f"api/applications/{self.key}"
            return entitygraph._base_client.make_request('DELETE', endpoint)

    def delete_by_key(self, key: str):
        endpoint = f"api/applications/{key}"
        return entitygraph._base_client.make_request('DELETE', endpoint)

    def get_all(self) -> List['Application']:
        endpoint = "api/applications"
        response: Response = entitygraph._base_client.make_request('GET', endpoint)

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
        response: Response = entitygraph._base_client.make_request('GET', endpoint)

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
        response: Response = entitygraph._base_client.make_request('GET', endpoint)

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
        response: Response = entitygraph._base_client.make_request('POST', endpoint, headers=headers,
                                                                   data={"label": label})

        return response.json()['key']

    def get_subscriptions(self) -> List[dict]:
        self.__check_key()

        endpoint = f"api/applications/{self.key}/subscriptions"
        response: Response = entitygraph._base_client.make_request('GET', endpoint)

        return response.json()

    def delete_subscription(self, label: str):
        self.__check_key()

        endpoint = f"api/applications/{self.key}/subscriptions/{label}"
        return entitygraph._base_client.make_request('DELETE', endpoint)

    def set_configuration(self, key: str, value: str | dict):
        """
        Sets or updates a configuration parameter

        :param key: Configuration key
        :param value: Configuration value
        """
        self.__check_key()

        endpoint = f"api/applications/{self.key}/configuration/{key}"
        return entitygraph._base_client.make_request('POST', endpoint, data=value if isinstance(value, str) else json.dumps(value))

    def delete_configuration(self, key: str):
        self.__check_key()

        endpoint = f"api/applications/{self.key}/configuration/{key}"
        return entitygraph._base_client.make_request('DELETE', endpoint)
