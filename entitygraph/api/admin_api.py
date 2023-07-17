import io
import json
from pathlib import Path

from entitygraph.api_response import ApiResponse
from entitygraph.base_client import BaseApiClient


class AdminAPI(BaseApiClient):

    def import_file(self, file_path: Path, file_mimetype: str = 'text/turtle', repository: str = 'entities',
                    application_label: str = 'default') -> ApiResponse | Exception:
        """
        Imports a file into the repository

        :param file_path: The path to the file
        :param file_mimetype: The mimetype of the file
        :param repository: The repository to import the file into: entities, schema, transactions, application
        :param application_label: The application label
        """
        endpoint = "api/admin/import/file"
        params = {'repository': repository, 'mimetype': file_mimetype}
        headers = {'X-Application': application_label}
        with open(file_path, 'rb') as file_mono:
            files = {'fileMono': file_mono}
            return self._make_request('POST', endpoint, params=params, headers=headers, files=files)

    def import_endpoint(self, sparql_endpoint: dict, repository: str = 'entities', application_label: str = 'default'):
        endpoint = 'api/admin/import/endpoint'
        params = {'repository': repository}
        headers = {'X-Application': application_label}
        data = json.dumps(sparql_endpoint)
        return self._make_request('POST', endpoint, params=params, headers=headers, data=data)

    def import_content(self, rdf_data: str, repository: str = 'entities', application_label='default',
                       request_mimetype: str = 'text/turtle') -> ApiResponse | Exception:
        """
        Imports RDF data into the repository

        :param rdf_data: The RDF data
        :param repository: The repository to import the file into: entities, schema, transactions, application
        :param application_label: The application label
        :param request_mimetype: The mimetype of the request
        """
        endpoint = "api/admin/import/content"
        params = {'repository': repository}
        headers = {'X-Application': application_label, 'Content-Type': request_mimetype}
        data = io.BytesIO(rdf_data.encode())
        return self._make_request('POST', endpoint, params=params, headers=headers, data=data)

    def reset(self, repository: str = 'entities', application_label: str = 'default') -> ApiResponse | Exception:
        """
        Resets the repository

        :param repository: The repository to import the file into: entities, schema, transactions, application
        :param application_label: The application label
        """
        endpoint = "api/admin/reset"
        params = {'repository': repository}
        headers = {'X-Application': application_label}
        return self._make_request('GET', endpoint, params=params, headers=headers)
