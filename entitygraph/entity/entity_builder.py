from __future__ import annotations

import re
import entitygraph

from rdflib import XSD, Graph, RDF, Literal, URIRef, BNode
from typing import List


# The Entity Builder class will be reworked completely to support the fluent API design pattern.
# This also means, that analogous ValueBuilder and DetailsBuilder (If possible) classes will be added in the future.
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
        self.type = type
        
        if type: 
            self.graph.add((self.node, RDF.type, type))
            
    def load(self, graph: Graph = None, serialized: str = None, format: str = "turtle") -> EntityBuilder: 
        if graph: 
            return self.from_graph(graph)
            
        if serialized: 
            return self.from_string(serialized, format)
            

    def add_type(self, type: URIRef) -> EntityBuilder: 
        """Adds an additional type definition for the current node

        Args:
            type (URIRef): QName of type

        Returns:
            EntityBuilder: this
        """
        self.graph.add((self.node, RDF.type, type))
        
        return self

    def add_value(self, property: URIRef, value: str | URIRef) -> EntityBuilder:
        if isinstance(value, URIRef):
            self.graph.add((self.node, property, value))
        else:
            self.graph.add((self.node, property, Literal(value)))

        return self
    
    def add_literal(self,  property: URIRef, value: Literal) -> EntityBuilder:
        self.graph.add((self.node, property, value))
        
        return self
    
    def add_string_value(self,  property: URIRef, value: str, lang = "en") -> EntityBuilder:
        if not self._is_valid_language_tag(lang): 
            raise ValueError("Not a valid language tag: "+lang)
        
        self.add_literal(property, Literal(value, lang=lang))
        
        return self
    
    def add_integer_value(self,  property: URIRef, value: int) -> EntityBuilder:
        self.add_literal(property, Literal(value, datatype=XSD.integer))
        return self
    
    def add_any_value(self,  property: URIRef, value: any) -> EntityBuilder:
        self.add_literal(property, Literal(value))
        return self

    def add_relation(self, property: URIRef, target_entity: entitygraph.Entity) -> EntityBuilder:
        self.graph.add((self.node, property, target_entity.uri))
        return self
    
    def link_to_entity(self, property: URIRef, target_entity: entitygraph.Entity) -> EntityBuilder:
        self.link_to_node(property, target_entity.uri)
        return self
    
    def link_to_node(self, property: URIRef, target: URIRef) -> EntityBuilder:
        self.graph.add((self.node, property, target))
        return self

    def build(self, save=True) -> entitygraph.Entity:
        entity = entitygraph.Entity(data=self.graph, scope=self._application_label, main_type=self.type)
        if save: 
            entity.save(encode=True)
        return entity

    @classmethod
    def from_string(cls, serialized: str, format: str = "turtle") -> EntityBuilder: 
        try: 
            builder = EntityBuilder()
            builder.graph.parse(data=serialized, format=format, encoding='utf-8') 
            return builder
        except Exception as err: 
            raise err
        
    @classmethod
    def from_graph(graph: Graph) -> EntityBuilder: 
        try: 
            builder = EntityBuilder()
            builder.graph = graph
            return builder
        except Exception as err: 
            raise err
        
    @classmethod
    def from_entity(self, entity: entitygraph.Entity) -> EntityBuilder:
        try: 
            builder = EntityBuilder()
            builder.graph = entity.as_graph()
            return builder
        except Exception as err: 
            raise err
        

    def _is_valid_language_tag(tag):
        # Define a regular expression pattern for a valid language tag
        pattern = r'^[a-zA-Z]{2,3}(-[a-zA-Z0-9]+)*(-[a-zA-Z]{2,4})?$'
        
        # Use re.match to check if the string matches the pattern
        match = re.match(pattern, tag)
        
        # If there's a match and the length is within the BCP 47 limits, it's valid
        if match and 1 <= len(tag) <= 35:
            return True
        else:
            return False