import json

from rdflib import Graph


class Converter(object):
    @staticmethod
    def json_to_turtle(json_ld):
        # Parse the JSON-LD into an RDF graph
        g = Graph()
        g.parse(data=json.dumps(json_ld), format='json-ld')

        # Serialize the graph in Turtle format
        turtle = g.serialize(format='turtle').decode("utf-8")

        return turtle


    @staticmethod
    def n3_to_turtle(n3):
        # Parse the N3 data into an RDF graph
        g = Graph()
        g.parse(data=n3, format='n3')

        # Serialize the graph in Turtle format
        turtle = g.serialize(format='turtle').decode("utf-8")

        return turtle

    @staticmethod
    def turtle_to_json(turtle):
        # Parse the Turtle data into an RDF graph
        g = Graph()
        g.parse(data=turtle, format='turtle')

        # Serialize the graph in JSON-LD format
        json_ld = g.serialize(format='json-ld').decode("utf-8")

        return json.loads(json_ld)

    @staticmethod
    def turtle_to_n3(turtle):
        # Parse the Turtle data into an RDF graph
        g = Graph()
        g.parse(data=turtle, format='turtle')

        # Serialize the graph in N3 format
        n3 = g.serialize(format='n3').decode("utf-8")

        return n3
