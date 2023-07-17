from typing import List

from rdflib import Graph, RDF, Literal, URIRef

import entitygraph
from entitygraph import Entity


class EntityBuilder:
    def __init__(self, types: URIRef | List[URIRef]):
        if entitygraph.client is None:
            raise Exception(
                "Not connected. Please connect using entitygraph.connect(api_key=..., host=...) before using Entity()")

        self._application_label: str = "default"
        self.graph = Graph()

        if isinstance(types, list):
            for t in types:
                self.graph.add((RDF.nil, RDF.type, t))
        else:
            self.graph.add((RDF.nil, RDF.type, types))

    def addValue(self, property: URIRef, value):
        self.graph.add((RDF.nil, property, Literal(value)))

        return self

    def addRelation(self, property: URIRef, target_entity: Entity):
        self.graph.add((RDF.nil, property, target_entity.uri))

        return self

    def build(self) -> Entity:
        entity = Entity(data=self.graph)
        entity._application_label = self._application_label
        return entity.save()
