from entitygraph.base_client import BaseApiClient


class QueryAPI(BaseApiClient):
    def query_bindings(self, query, application_label='default'):
        endpoint = "/api/query/select"
        headers = {'X-Application': application_label, 'Content-Type': 'text/plain'}
        return self.make_request('POST', endpoint, headers=headers, data=query)

    def query_statements(self, query, application_label='default'):
        endpoint = "/api/query/construct"
        headers = {'X-Application': application_label, 'Content-Type': 'text/plain'}
        return self.make_request('POST', endpoint, headers=headers, data=query)