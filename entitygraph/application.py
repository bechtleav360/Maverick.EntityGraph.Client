import json
from typing import Type, List

from rdflib import Graph, RDF, URIRef

import entitygraph
from entitygraph import ApplicationsAPI, Entity, Query, Admin, EntityBuilder


class Application:
    def __init__(self, label: str = None, flags: dict = {"isPersistent": True, "isPublic": True},
                 configuration: dict = {}):
        if entitygraph.client is not None:
            self.__api: ApplicationsAPI = entitygraph.client.applications_api
        else:
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

    def EntityBuilder(self, types: URIRef | List[URIRef]) -> EntityBuilder:
        entity_builder = EntityBuilder(types)
        entity_builder._application_label = self.label

        return entity_builder

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
        res: dict = self.__api.create_application({
            "label": self.label,
            "flags": self.flags,
            "configuration": self.configuration
        }).json()
        self.key = res.get("key")
        return self

    def delete(self):
        self.__check_key()
        return self.__api.delete_application(self.key)

    def delete_by_label(self, label: str):
        app = self.get_by_label(label)
        if app is not None:
            return self.__api.delete_application(app.key)

    def delete_by_key(self, key: str):
        return self.__api.delete_application(key)

    def get_all(self) -> List['Application']:
        res: list = self.__api.list_applications().json()
        cache = []
        for x in res:
            app = Application(label=x.get('label'),
                              flags=x.get('flags'),
                              configuration=x.get('configuration'),
                              )
            app.key = x.get('key')
            cache.append(app)
        return cache

    def get_by_key(self, key: str) -> 'Application':
        res: dict = self.__api.get_application(key).json()

        if res is not None:
            app = Application(label=res.get('label'),
                              flags=res.get('flags'),
                              configuration=res.get('configuration'),
                              )
            app.key = res.get('key')
            return app

    def get_by_label(self, label: str) -> 'Application':
        res = self.__api.list_applications().json()

        for x in res:
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
        return self.__api.generate_key(self.key, {"label": label}).json()['key']

    def get_subscriptions(self) -> List[dict]:
        self.__check_key()
        return self.__api.list_subscriptions(self.key).json()

    def delete_subscription(self, label: str):
        self.__check_key()
        return self.__api.revoke_token(self.key, label)

    def set_configuration(self, key: str, value: str | dict):
        """
        Sets or updates a configuration parameter

        :param key: Configuration key
        :param value: Configuration value
        """
        self.__check_key()
        return self.__api.create_configuration(self.key, key, value)

    def delete_configuration(self, key: str):
        self.__check_key()
        return self.__api.delete_configuration(self.key, key)
