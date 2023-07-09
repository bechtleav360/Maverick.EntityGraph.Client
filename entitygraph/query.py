import io

import pandas
from pandas import DataFrame
from rdflib import Graph

import entitygraph
from entitygraph import QueryAPI


class Query:
    def __init__(self):
        if entitygraph.client is not None:
            self.__api: QueryAPI = entitygraph.client.query_api
        else:
            raise Exception(
                "Not connected. Please connect using entitygraph.connect(api_key=..., host=...) before using Query()")

        self._application_label: str = "default"

    def select(self, query: str, repository: str = "entities") -> DataFrame:
        """
        :param query: SPARQL query. For example: 'SELECT ?entity  ?type WHERE { ?entity a ?type } LIMIT 100'
        :param repository: The repository type in which the query should search: entities, schema, transactions or application
        """
        response = self.__api.select(query, repository, self._application_label, "text/csv")
        return pandas.read_csv(io.StringIO(response.text))

    def construct(self, query: str, repository: str = "entities") -> Graph:
        """
        :param query: SPARQL query. For example: 'CONSTRUCT WHERE { ?s ?p ?o . } LIMIT 100'
        :param repository: The repository type in which the query should search: entities, schema, transactions or application
        :param response_format: text/turtle or application/ld+json
        """
        response = self.__api.construct(query, repository, self._application_label)
        return Graph().parse(data=response.text)
