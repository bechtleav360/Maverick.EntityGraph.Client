import io

import pandas
from pandas import DataFrame
from rdflib import Graph
from requests import Response

import entitygraph


class Query:
    def __init__(self):
        if entitygraph.base_client is None:
            raise Exception(
                "Not connected. Please connect using entitygraph.connect(api_key=..., host=...) before using Query()")

        self._application_label: str = "default"

    def select(self, query: str, repository: str = "entities") -> DataFrame:
        """
        :param query: SPARQL query. For example: 'SELECT ?entity  ?type WHERE { ?entity a ?type } LIMIT 100'
        :param repository: The repository type in which the query should search: entities, schema, transactions or application
        """
        endpoint = "api/query/select"
        params = {'repository': repository}
        headers = {'X-Application': self._application_label, 'Content-Type': 'text/plain', 'Accept': 'text/csv'}
        response: Response = entitygraph.base_client.make_request('POST', endpoint, headers=headers, params=params, data=query)

        return pandas.read_csv(io.BytesIO(response.content))

    def construct(self, query: str, repository: str = "entities") -> Graph:
        """
        :param query: SPARQL query. For example: 'CONSTRUCT WHERE { ?s ?p ?o . } LIMIT 100'
        :param repository: The repository type in which the query should search: entities, schema, transactions or application
        :param response_format: text/turtle or application/ld+json
        """
        endpoint = "api/query/construct"
        params = {'repository': repository}
        headers = {'X-Application': self._application_label, 'Content-Type': 'text/plain', 'Accept': 'text/turtle'}
        response: Response = entitygraph.base_client.make_request('POST', endpoint, headers=headers, params=params, data=query)

        return Graph().parse(data=response.text)
