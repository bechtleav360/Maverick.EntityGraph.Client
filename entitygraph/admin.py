from pathlib import Path

import entitygraph
from entitygraph import AdminAPI


class Admin:
    def __init__(self):
        if entitygraph.client is not None:
            self.__api: AdminAPI = entitygraph.client.admin_api
        else:
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
        self.__api.import_file(file_path, file_mimetype, repository, self._application_label)

    def import_endpoint(self, sparql_endpoint: dict, repository: str = "entities"):
        """
        Imports rdf content from SPARQL endpoint into target repository

        :param repository: The repository type in which the file should be imported: entities, schema, transactions or application
        """

        self.__api.import_endpoint(sparql_endpoint, repository, self._application_label)

    def import_content(self, rdf_data: str, content_mimetype: str = "text/turtle", repository: str = "entities"):
        """
        Imports rdf content into the target repository

        :param rdf_data: The RDF data to import
        :param content_mimetype: The mimetype of the RDF data to import: text/turtle, application/ld+json, application/rdf+xml, application/n-triples, application/n-quads or application/vnd.hdt
        :param repository: The repository type in which the file should be imported: entities, schema, transactions or application
        """
        self.__api.import_content(rdf_data, repository, self._application_label, content_mimetype)

    def reset(self, repository: str = "entities"):
        """
        Removes all statements within the repository
        """
        self.__api.reset(repository, self._application_label)
