from entitygraph.base_client import BaseApiClient


class QueryAPI(BaseApiClient):
    def select(self, query, repository='entities', application_label='default', response_mimetype='text/csv'):
        endpoint = "api/query/select"
        params = {'repository': repository}
        headers = {'X-Application': application_label, 'Content-Type': 'text/plain', 'Accept': response_mimetype}
        return self.make_request('POST', endpoint, headers=headers, params=params, data=query)

    def construct(self, query, repository='entities', application_label='default', response_mimetype='text/turtle'):
        endpoint = "api/query/construct"
        params = {'repository': repository}
        headers = {'X-Application': application_label, 'Content-Type': 'text/plain', 'Accept': response_mimetype}
        return self.make_request('POST', endpoint, headers=headers, params=params, data=query)