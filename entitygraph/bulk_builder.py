from requests import Response

import entitygraph


class BulkBuilder:
    def __init__(self, entity_builders: list[entitygraph.EntityBuilder]):
        self._application_label: str = "default"
        self.entity_builders = entity_builders

    def build(self):
        tmp = ''
        for entity_builder in self.entity_builders:
            tmp += entity_builder.graph.serialize(format='turtle')

        endpoint = f'api/entities'
        headers = {'X-Application': self._application_label, 'Content-Type': 'text/turtle', 'Accept': 'text/turtle'}
        entitygraph.base_api_client.make_request('POST', endpoint, headers=headers, data=tmp)
