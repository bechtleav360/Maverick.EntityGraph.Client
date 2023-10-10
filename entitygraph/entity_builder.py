from typing import List

from rdflib import Graph, RDF, Literal, URIRef, BNode

import entitygraph
from entitygraph import Entity


class EntityBuilder:
    

    def __init__(self, type: URIRef = None, scope: str = "default"):
        """ Builder for entities. 

        Args:
            type (URIRef, optional): The type of the new entity as URIRef. Defaults to None.
            scope (str, optional): The scope (or application) in which this . Defaults to "default".
        """

        self._application_label: str = scope
        self.graph = Graph()
        self.node = BNode()
        
        if type: 
            self.graph.add((self.node, RDF.type, type))
            
    def load(self, graph: Graph = None, serialized: str = None, format: str = "turtle"): 
        if graph: 
            return self.from_graph(graph)
            
        if serialized: 
            return self.from_string(serialized, format)
            
    
    def from_string(self, serialized: str, format: str = "turtle"): 
        try: 
            self.graph.parse(data=serialized, format=format, encoding='utf-8') 
            return self
        except Exception as err: 
            raise err
        
    def from_graph(self, graph: Graph): 
        try: 
            self.graph = graph
            return self
        except Exception as err: 
            raise err

    def from_entity(self, entity: Entity): 
        try: 
            self.graph = entity.as_graph()
            return self
        except Exception as err: 
            raise err

    def add_type(self, type: URIRef): 
        self.graph.add((self.node, RDF.type, type))
        
        return self

    def add_value(self, property: URIRef, value: str | URIRef):
        if isinstance(value, URIRef):
            self.graph.add((self.node, property, value))
        else:
            self.graph.add((self.node, property, Literal(value)))

        return self

    def add_relation(self, property: URIRef, target_entity: Entity):
        self.graph.add((self.node, property, target_entity.uri))

        return self

    def build(self) -> Entity:
        entity = Entity(data=self.graph, scope=self._application_label)
        return entity
