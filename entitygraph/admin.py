import io
import json
from pathlib import Path

import entitygraph


class Admin:
    def __init__(self):
        if entitygraph.base_client is None:
            raise Exception(
                "Not connected. Please connect using entitygraph.connect(api_key=..., host=...) before using Admin()")

        self._application_label: str = "default"

    def import_file(self, file_path: Path, file_mimetype: str = "text/turtle", repository: str = "entities"):
        """
        Imports rdf content from file into target repository

        :param file_path: Path to the file to import
        :param file_mimetype: The mimetype of the file to import: text/turtle, application/ld+json, application/rdf+xml, application/n-triples, application/n-quads or application/vnd.hdt
        :param repository: The repository type in which the file should be imported: entities, schema, transactions or application
        """
        endpoint = "api/admin/import/file"
        params = {'repository': repository, 'mimetype': file_mimetype}
        headers = {'X-Application': self._application_label}
        with open(file_path, 'rb') as file_mono:
            files = {'fileMono': file_mono}
            return entitygraph.base_client.make_request('POST', endpoint, params=params, headers=headers, files=files)

    def import_endpoint(self, sparql_endpoint: dict, repository: str = "entities"):
        """
        Imports rdf content from SPARQL endpoint into target repository

        :param repository: The repository type in which the file should be imported: entities, schema, transactions or application
        """
        endpoint = 'api/admin/import/endpoint'
        params = {'repository': repository}
        headers = {'X-Application': self._application_label}
        data = json.dumps(sparql_endpoint)
        return entitygraph.base_client.make_request('POST', endpoint, params=params, headers=headers, data=data)

    def import_content(self, rdf_data: str, content_mimetype: str = "text/turtle", repository: str = "entities"):
        """
        Imports rdf content into the target repository

        :param rdf_data: The RDF data to import
        :param content_mimetype: The mimetype of the RDF data to import: text/turtle, application/ld+json, application/rdf+xml, application/n-triples, application/n-quads or application/vnd.hdt
        :param repository: The repository type in which the file should be imported: entities, schema, transactions or application
        """
        endpoint = "api/admin/import/content"
        params = {'repository': repository}
        headers = {'X-Application': self._application_label, 'Content-Type': content_mimetype}
        data = io.BytesIO(rdf_data.encode())
        return entitygraph.base_client.make_request('POST', endpoint, params=params, headers=headers, data=data)

    def reset(self, repository: str = "entities"):
        """
        Removes all statements within the repository

        :param repository: The repository: entities, schema, transactions, application
        """
        endpoint = "api/admin/reset"
        params = {'repository': repository}
        headers = {'X-Application': self._application_label}
        return entitygraph.base_client.make_request('GET', endpoint, params=params, headers=headers)
