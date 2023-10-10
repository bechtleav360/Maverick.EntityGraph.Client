from typing import List

from rdflib import Graph, RDF, Literal, URIRef, BNode

import entitygraph
from entitygraph import Entity


class EntityBuilder:
    

    def __init__(self, type: URIRef = None):

        self._application_label: str = "default"
        self.graph = Graph()
        self.node = BNode()
        
        if type: 
            self.graph.add((self.node, RDF.type, type))
            
    def load(self, graph: Graph = None, serialized: str = None, format: str = "turtle"): 
        if graph: 
            self.graph = self.graph + graph
            
        if serialized: 
            self.graph.parse(data=serialized, format=format, encoding='utf-8') 

    def addType(self, type: URIRef): 
        self.graph.add((self.node, RDF.type, type))

    def addValue(self, property: URIRef, value: str | URIRef):
        if isinstance(value, URIRef):
            self.graph.add((self.node, property, value))
        else:
            self.graph.add((self.node, property, Literal(value)))

        return self

    def addRelation(self, property: URIRef, target_entity: Entity):
        self.graph.add((self.node, property, target_entity.uri))

        return self

    def build(self) -> Entity:
        entity = Entity(data=self.graph)
        return entity
