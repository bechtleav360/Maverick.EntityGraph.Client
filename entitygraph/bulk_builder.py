from requests import Response

import entitygraph
from entitygraph import EntityBuilder, Entity


class BulkBuilder:
    def __init__(self, entity_builders: list[EntityBuilder]):
        if entitygraph._base_client is None:
            raise Exception(
                "Not connected. Please connect using entitygraph.connect(api_key=..., host=...) before using EntityBuilder()")

        self._application_label: str = "default"
        self.entity_builders = entity_builders

    def build(self):
        tmp = ''
        for entity_builder in self.entity_builders:
            tmp += entity_builder.graph.serialize(format='turtle')
        print(tmp)
        endpoint = f'api/entities'
        headers = {'X-Application': self._application_label, 'Content-Type': 'text/turtle', 'Accept': 'text/turtle'}
        entitygraph._base_client.make_request('POST', endpoint, headers=headers, data=tmp)
