from typing import List

from entitygraph.api_response import ApiResponse
from entitygraph.base_client import BaseApiClient


class ApplicationsAPI(BaseApiClient):
    def list_applications(self) -> ApiResponse:
        endpoint = "api/applications"
        return self.make_request('GET', endpoint)

    def create_application(self, application_data: dict) -> ApiResponse:
        endpoint = "api/applications"
        headers = {'Content-Type': 'application/json'}
        return self.make_request('POST', endpoint, data=application_data)

    def list_subscriptions(self, application_key: str) -> ApiResponse:
        endpoint = f"api/applications/{application_key}/subscriptions"
        return self.make_request('GET', endpoint)

    def generate_key(self, application_key: str, key_request: dict) -> ApiResponse:
        endpoint = f"api/applications/{application_key}/subscriptions"
        headers = {'Content-Type': 'application/json'}
        return self.make_request('POST', endpoint, data=key_request)

    def create_configuration(self, application_key: str, configuration_key: str, configuration_data: str | dict) -> ApiResponse:
        endpoint = f"api/applications/{application_key}/configuration/{configuration_key}"
        return self.make_request('POST', endpoint, data=configuration_data)

    def delete_configuration(self, application_key: str, configuration_key: str) -> ApiResponse:
        endpoint = f"api/applications/{application_key}/configuration/{configuration_key}"
        return self.make_request('DELETE', endpoint)

    def query_application(self, query: str, response_mimetype: str = 'text/turtle') -> ApiResponse:
        """
        :param response_mimetype: text/turtle or node/ld+json
        :param query: SPARQL query. For example: 'CONSTRUCT WHERE { ?s ?p ?o . } LIMIT 100'
        """
        endpoint = "api/applications/query"
        headers = {'Content-Type': 'text/plain', 'Accept': response_mimetype}
        return self.make_request('POST', endpoint, data=query)

    def get_application(self, application_key: str) -> ApiResponse:
        endpoint = f"api/applications/{application_key}"
        return self.make_request('GET', endpoint)

    def delete_application(self, application_key: str) -> ApiResponse:
        endpoint = f"api/applications/{application_key}"
        return self.make_request('DELETE', endpoint)

    def revoke_token(self, application_key: str, label: str) -> ApiResponse:
        endpoint = f"api/applications/{application_key}/subscriptions/{label}"
        return self.make_request('DELETE', endpoint)
