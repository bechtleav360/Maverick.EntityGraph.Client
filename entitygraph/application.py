import json
from typing import Type

import entitygraph
from entitygraph import ApplicationsAPI, Entity, Query, Admin


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

    def __str__(self):
        return f"Application(label={self.label}, key={self.key}, flags={self.flags}, configuration={self.configuration})"

    def Entity(self, data: str | dict = None, format: str = "turtle") -> 'Entity':
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
            "flags": json.dumps(self.flags),
            "configuration": json.dumps(self.configuration)
        }).json()
        self.key = res.get("key")
        return self

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
