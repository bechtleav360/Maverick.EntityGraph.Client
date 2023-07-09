import io
from pathlib import Path

from entitygraph.api_response import ApiResponse
from entitygraph.base_client import BaseApiClient


class AdminAPI(BaseApiClient):
    # jobs-ctrl
    def exec_replace_subject_identifiers_job(self, application_label: str = 'default') -> ApiResponse | Exception:
        """
        Executes the replace subject identifiers job

        :param application_label: The application label
        """
        endpoint = "api/admin/jobs/execute/normalize/subjectIdentifiers"
        headers = {'X-Application': application_label}
        return self._make_request('POST', endpoint, headers=headers)

    def exec_replace_object_identifiers_job(self, application_label: str = 'default') -> ApiResponse | Exception:
        """
        Executes the replace object identifiers job

        :param application_label: The application label
        """
        endpoint = "api/admin/jobs/execute/normalize/objectIdentifiers"
        headers = {'X-Application': application_label}
        return self._make_request('POST', endpoint, headers=headers)

    def exec_export_job(self, application_label: str = 'default') -> ApiResponse | Exception:
        """
        Executes the export job

        :param application_label: The application label
        """
        endpoint = "api/admin/jobs/execute/export"
        headers = {'X-Application': application_label}
        return self._make_request('POST', endpoint, headers=headers)

    def exec_deduplication_job(self, application_label: str = 'default') -> ApiResponse | Exception:
        """
        Executes the deduplication job

        :param application_label: The application label
        """
        endpoint = "api/admin/jobs/execute/deduplication"
        headers = {'X-Application': application_label}
        return self._make_request('POST', endpoint, headers=headers)

    def exec_coercion_job(self, application_label: str = 'default') -> ApiResponse | Exception:
        """
        Executes the coercion job

        :param application_label: The application label
        """
        endpoint = "api/admin/jobs/execute/coercion"
        headers = {'X-Application': application_label}
        return self._make_request('POST', endpoint, headers=headers)

    # admin

    def import_file(self, file_path: Path, file_mimetype: str = 'text/turtle', repository: str = 'entities',
                    application_label: str = 'default') -> ApiResponse | Exception:
        """
        Imports a file into the repository

        :param file_path: The path to the file
        :param file_mimetype: The mimetype of the file
        :param repository: The repository to import the file into: entities, schema, transactions, application
        :param application_label: The application label
        """
        endpoint = "api/admin/bulk/import/file"
        params = {'repository': repository, 'mimetype': file_mimetype}
        headers = {'X-Application': application_label}
        with open(file_path, 'rb') as file_mono:
            files = {'fileMono': file_mono}
            return self._make_request('POST', endpoint, params=params, headers=headers, files=files)

    def import_content(self, rdf_data: str, repository: str = 'entities', application_label='default',
                       request_mimetype: str = 'text/turtle') -> ApiResponse | Exception:
        """
        Imports RDF data into the repository

        :param rdf_data: The RDF data
        :param repository: The repository to import the file into: entities, schema, transactions, application
        :param application_label: The application label
        :param request_mimetype: The mimetype of the request
        """
        endpoint = "api/admin/bulk/import/content"
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
        endpoint = "api/admin/bulk/reset"
        params = {'repository': repository}
        headers = {'X-Application': application_label}
        return self._make_request('GET', endpoint, params=params, headers=headers)
