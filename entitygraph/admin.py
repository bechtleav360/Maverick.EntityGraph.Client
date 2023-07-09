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
        :param file_path: Path to the file to import
        :param file_mimetype: The mimetype of the file to import: text/turtle, application/ld+json, application/rdf+xml, application/n-triples, application/n-quads or application/vnd.hdt
        :param repository: The repository type in which the file should be imported: entities, schema, transactions or application
        """
        self.__api.import_file(file_path, file_mimetype, repository, self._application_label)

    def import_content(self, rdf_data: str, content_mimetype: str = "text/turtle", repository: str = "entities"):
        """
        :param rdf_data: The RDF data to import
        :param content_mimetype: The mimetype of the RDF data to import: text/turtle, application/ld+json, application/rdf+xml, application/n-triples, application/n-quads or application/vnd.hdt
        :param repository: The repository type in which the file should be imported: entities, schema, transactions or application
        """
        self.__api.import_content(rdf_data, repository, self._application_label, content_mimetype)

    def reset(self, repository: str = "entities"):
        self.__api.reset(repository, self._application_label)

    def exec_replace_subject_identifiers_job(self):
        self.__api.exec_replace_subject_identifiers_job(self._application_label)

    def exec_replace_object_identifiers_job(self):
        self.__api.exec_replace_object_identifiers_job(self._application_label)

    def exec_export_job(self):
        self.__api.exec_export_job(self._application_label)

    def exec_deduplication_job(self):
        self.__api.exec_deduplication_job(self._application_label)

    def exec_coercion_job(self):
        self.__api.exec_coercion_job(self._application_label)
