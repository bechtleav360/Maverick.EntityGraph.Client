import json
from typing import List

from entitygraph.api_response import ApiResponse
from entitygraph.base_client import BaseApiClient


class ApplicationsAPI(BaseApiClient):
    def list_applications(self) -> ApiResponse | Exception:
        """
        :return: List of applications
        """
        endpoint = "api/applications"
        return self._make_request('GET', endpoint)

    def create_application(self, application_data: dict) -> ApiResponse | Exception:
        """
        :param application_data: Application data
        :return: Application
        """
        endpoint = "api/applications"
        headers = {'Content-Type': 'application/json'}
        return self._make_request('POST', endpoint, data=application_data)

    def list_subscriptions(self, application_key: str) -> ApiResponse | Exception:
        """
        :param application_key: Application key
        :return: List of subscriptions
        """
        endpoint = f"api/applications/{application_key}/subscriptions"
        return self._make_request('GET', endpoint)

    def generate_key(self, application_key: str, key_request: dict) -> ApiResponse | Exception:
        """
        CreateApiKeyRequest

        :param application_key: Application key
        :param key_request: Key request
        :return: ApiKeyWithApplicationResponse
        """
        endpoint = f"api/applications/{application_key}/subscriptions"
        headers = {'Content-Type': 'application/json'}
        return self._make_request('POST', endpoint, data=key_request)

    def create_configuration(self, application_key: str, configuration_key: str, configuration_data: str | dict) -> ApiResponse | Exception:
        """
        :param application_key: Application key
        :param configuration_key: Configuration key
        :param configuration_data: Configuration data
        :return: Application
        """
        endpoint = f"api/applications/{application_key}/configuration/{configuration_key}"
        return self._make_request('POST', endpoint, data=configuration_data if isinstance(configuration_data, str) else json.dumps(configuration_data))

    def delete_configuration(self, application_key: str, configuration_key: str) -> ApiResponse | Exception:
        """
        :param application_key: Application key
        :param configuration_key: Configuration key
        :return: Application
        """
        endpoint = f"api/applications/{application_key}/configuration/{configuration_key}"
        return self._make_request('DELETE', endpoint)

    def query_application(self, query: str, response_mimetype: str = 'text/turtle') -> ApiResponse | Exception:
        """
        :param query: SPARQL query. For example: 'CONSTRUCT WHERE { ?s ?p ?o . } LIMIT 100'
        :param response_mimetype: text/turtle or node/ld+json
        """
        endpoint = "api/applications/query"
        headers = {'Content-Type': 'text/plain', 'Accept': response_mimetype}
        return self._make_request('POST', endpoint, data=query)

    def get_application(self, application_key: str) -> ApiResponse | Exception:
        """
        :param application_key: Application key
        :return: Application
        """
        endpoint = f"api/applications/{application_key}"
        return self._make_request('GET', endpoint)

    def delete_application(self, application_key: str) -> ApiResponse | Exception:
        """
        :param application_key: Application key
        """
        endpoint = f"api/applications/{application_key}"
        return self._make_request('DELETE', endpoint)

    def revoke_token(self, application_key: str, label: str) -> ApiResponse | Exception:
        """
        :param application_key: Application key
        :param label: Subscription label
        """
        endpoint = f"api/applications/{application_key}/subscriptions/{label}"
        return self._make_request('DELETE', endpoint)
