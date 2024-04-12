import csv
import entitygraph
import json
import io
import logging
import requests

from entitygraph.namespace_map import namespace_map
from entitygraph.utils import uri_ref_to_prefixed, generate_value_identifier
from rdflib import BNode, Graph, Literal, RDF, URIRef
from requests import Response

logger = logging.getLogger(__name__)


def save_detail(entity_id: str, detail: entitygraph.Detail):
    """
    Save a detail

    :param entity_id: The id of the entity, this detail belongs to.
    :param detail: A detail class object.
    """
    headers = {
        'X-Application': detail.application_label,
        'Content-Type': "text/plain",
        'Accept': "text/turtle"
    }
    params = {"valueIdentifier": detail.value_identifier}
    response: Response = entitygraph.base_api_client.make_request(
        'POST',
        f'api/entities/{entity_id}/values/{detail.value_predicate}/details/{detail.predicate}',
        headers=headers,
        data=json.dumps(detail.content) if isinstance(detail.content, dict) else str(detail.content).encode('utf-8'),
        params=params
    )
    response.raise_for_status()


def delete_detail(entity_id: str, detail: entitygraph.Detail):
    """
    Delete a detail.

    :param entity_id: The id of the entity, this detail belongs to.
    :param detail: A detail class object.
    """
    headers = {
        'X-Application': detail.application_label,
        'Accept': "text/turtle"
    }
    params = {"valueIdentifier": detail.value_identifier}
    response: Response = entitygraph.base_api_client.make_request(
        'DELETE',
        f'api/entities/{entity_id}/values/{detail.value_predicate}/details/{detail.predicate}',
        headers=headers,
        params=params
    )
    response.raise_for_status()


class Application:
    """Static class providing API connection methods for entities/query/application labels
    """
    @staticmethod
    def load_applications(tag: str | None = None) -> list:
        """Loads all applications from the entity graph and returns it as dictionary

        :param tag: Identifier for a subset of applications.
        :type tag: str | None

        :return: List of application labels
        :rtype: list
        """

        try:
            logger.info(f"Requesting all application from entity graph with tag {tag}")

            params = {}
            if tag:
                params["tag"] = tag

            response: Response = entitygraph.base_api_client.make_request(
                'GET',
                'api/applications',
                params=params
            )
            response.raise_for_status()

            result = []
            for app in json.loads(response.text):
                if app['label']:
                    logging.info(f"Found application with label: {app['label']}")
                    result.append(app['label'])
            return result
        except requests.exceptions.ReadTimeout as err_rt:
            logger.error(f"Request to update link failed due to timeout, rescheduling execution. Traceback: {err_rt}")
            raise err_rt
        except requests.exceptions.HTTPError as err_h:
            logger.error(
                f"Request to update link failed with code {err_h.response.status_code} and message: "
                f"{err_h.response.reason} (URL: <{err_h.request.url}>). Traceback: {err_h}"
            )
            if err_h.response.text:
                logger.error(f"Error details: \n {err_h.response.text}", )

            raise err_h
        except Exception as err:
            logger.error(f"failed to query graph. reason: {err}")
            raise err

    @staticmethod
    def run_query(query: str, application_label: str) -> list:
        """Runs a query on the entity graph and returns the result as a list of dictionaries

        :param query: The query string to run.
        :type query: str
        :param application_label: The application label in the context of the entitygraph.
        :type application_label: str

        :returns: A list of dictionaries representing the query result.
        :rtype: list
        """

        try:
            logger.info(f"Running query on application label '{application_label}': \n {query}")

            response: Response = entitygraph.base_api_client.make_request(
                'POST',
                'api/query/select',
                data=query.encode("utf-8"),
                headers={
                    "Content-Type": "text/plain",
                    "Accept": "text/csv;charset=UTF-8",
                    "X-Application": application_label,
                },
            )
            response.raise_for_status()

            result = []
            if not response.text:
                logging.info(f"No candidates found in scope '{application_label}'")
                return result

            io_string = io.StringIO(response.text)

            class CustomDictReader(csv.DictReader):
                def __next__(self):
                    row = super().__next__()
                    # Decode each field value based on the response's encoding
                    return {
                        key: value_.decode(response.encoding)
                        if isinstance(value_, bytes) else value_
                        for key, value_ in row.items()
                    }

            reader = CustomDictReader(io_string, delimiter=',')
            return list(reader)

        except requests.exceptions.ReadTimeout as err_rt:
            logger.error("Request to query graph failed due to timeout")
            raise err_rt

        except requests.exceptions.HTTPError as err_h:
            logger.error(f"Request to query graph failed with code {err_h.response.status_code} and message: "
                          f"{err_h.response.reason} (URL: <err_h.request.url>)")
            if err_h.response.text:
                logging.error(f"Error details: \n {err_h.response.text}")
            raise err_h

        except Exception as err:
            logger.error(f"Failed to run query: {err}")
            raise err

    @staticmethod
    def create_entity(entity: entitygraph.Entity):
        """
        Create a new entity from an entity object.

        :param entity: An entity object without an ID.

        :return: The given entity.
        """
        if entity.id is not None:
            logger.error("Cannot create new entity, since it already exists. Use 'save_entity' instead.")
            raise ValueError("Cannot create new entity, since it already exists. Use 'save_entity' instead.")

        # Instantiate graph
        graph = Graph()
        node = BNode()

        if entity.types is None:
            logger.error("To create an entity, add at least one type must have been added.")
            raise ValueError("To create an entity, add at least one type must have been added.")

        if not entity.values.items():
            logger.error("To create an entity, add at least one value must have been added.")
            raise ValueError("To create an entity, add at least one value must have been added.")

        # Add entity types to teh graph
        for entity_type in entity.types:
            graph.add((node, RDF.type, URIRef(entity_type)))

        # Add values to the graph
        for predicate, content_lst in entity.values.items():
            for literal in content_lst:
                name = ""
                for key, entity_value in namespace_map.items():
                    if entity_value == predicate.split('.')[0]:
                        name = key + predicate.split('.')[1]
                        break
                if not name:
                    raise ValueError(f"Could not find predicate {predicate}")

                graph.add((node, URIRef(name), Literal(literal)))

        # TODO Relations
        # # Add relations to the graph
        # for predicate, content_lst in entity.relations.items():
        #     for uri_ref in content_lst:
        #         name = ""
        #         for key, value_ in namespace_map.items():
        #             if value_ == predicate.split('.')[0]:
        #                 name = key + predicate.split('.')[1]
        #                 break
        #         if not name:
        #             raise ValueError(f"Could not find predicate {predicate}")
        #
        #         graph.add((node, URIRef(name), uri_ref))

        # Save entity
        entity_as_turtle = graph.serialize(format='turtle')
        logger.info("Creating new graph:")
        logger.info(f"{entity_as_turtle}")

        headers = {
            'X-Application': entity.application_label,
            'Content-Type': "text/turtle",
            'Accept': "application/ld+json"
        }
        response: Response = entitygraph.base_api_client.make_request(
            'POST',
            'api/entities',
            headers=headers,
            data=entity_as_turtle.encode(encoding="UTF-8")
        )

        response.raise_for_status()
        new_entity_id = response.json()["@graph"][0]["@graph"][0]["@id"].split(":")[-1]
        if entity.application_label in new_entity_id:
            new_entity_id = new_entity_id.split(".")[-1]
        print(f"Created new entity with id {new_entity_id}")
        logger.info(f"Created new entity with id {new_entity_id}")

        # Save details
        for predicate, content_lst in entity.values.items():
            for literal_ in content_lst:
                details: entitygraph.DetailContainer = entity.values[predicate].details(literal_)
                for detail in details:
                    if detail.has_changes():
                        if detail.remove_old:
                            delete_detail(new_entity_id, detail)
                        if detail.content:
                            save_detail(new_entity_id, detail)

        entity.add_id(new_entity_id)

        return entitygraph.Entity(entity.application_label, id_=new_entity_id)

    @staticmethod
    def save_entity(entity: entitygraph.Entity):
        """
        Save all changes for an already existing entity.

        :param entity: An entity object.

        :return: The given entity object.
        """

        if entity.id is None:
            logger.error("Only already existing entities can be saved using this method. To create a new entity use "
                         "'create_entity' instead.")
            raise ValueError("Only already existing entities can be saved using this method. To create a new entity "
                             "use 'create_entity' instead.")
        def add_value_to_entity_remote(path: str, item: entitygraph.ValuesAndRelationsBase, content: str):
            """Helper for adding new values to the entity graph

            :param path: Either value or relations.
            :type path: str
            :param item: A value/relation object.
            :type item: entitygraph.ValuesAndRelationsBase
            :param content: A literal to be added to this value/relation.
            :type content: str
            """

            prefixed = uri_ref_to_prefixed(URIRef(item.predicate))
            endpoint = f"api/entities/{item.entity_id}/{path}/{prefixed}"
            headers = {
                'X-Application': item.application_label,
                'Content-Type': 'text/plain',
                'Accept': 'application/ld+json'
            }
            params = {"languageTag": item.language}
            response: Response = entitygraph.base_api_client.make_request(
                'POST',
                endpoint,
                headers=headers,
                data=content,
                params=params
            )
            response.raise_for_status()

        def remove_value_from_entity_remote(path: str, item: entitygraph.ValuesAndRelationsBase, content):
            """Helper for removing a value from the entity graph

            :param path: Either value or relations.
            :type path: str
            :param item: A value/relation object.
            :type item: entitygraph.ValuesAndRelationsBase
            :param content: A literal to be removed from this value/relation.
            :type content: str
            """

            prefixed = uri_ref_to_prefixed(URIRef(item.predicate))
            endpoint = f"api/entities/{item.entity_id}/{path}/{prefixed}"
            headers = {
                'X-Application': item.application_label,
                'Accept': 'application/ld+json'
            }
            params = {
                "languageTag": item.language,
                "valueIdentifier": generate_value_identifier(item.predicate, content)
            }
            response: Response = entitygraph.base_api_client.make_request(
                'DELETE',
                endpoint,
                headers=headers,
                params=params
            )
            response.raise_for_status()

        for value_ in entity.values:
            for new_content in value_.new_content():
                add_value_to_entity_remote("values", value_, new_content)
            for removed_content in value_.removed_content():
                remove_value_from_entity_remote("values", value_, removed_content)

        # TODO Relations
        # for relation in entity.relations:
        #     for new_content in relation.new_content():
        #         add_value_to_entity_remote("relations", relation, new_content)
        #     for removed_content in relation.removed_content():
        #         remove_value_from_entity_remote("relations", relation, removed_content)

        # Save details
        for predicate, content_lst in entity.values.items():
            for literal_ in content_lst:
                details: entitygraph.DetailContainer = entity.values[predicate].details(literal_)
                for detail in details:
                    if detail.has_changes():
                        if detail.remove_old:
                            delete_detail(entity.id, detail)
                        if detail.content:
                            save_detail(entity.id, detail)

        return entity

    @staticmethod
    def delete_entity(entity: entitygraph.Entity):
        """Delete an entity

        :param entity: An entity object.
        :type entity: entitygraph.Entity
        """

        endpoint = f"api/entities/{entity.id}"
        headers = {
            'X-Application': entity.application_label,
            'Accept': 'application/ld+json'
        }
        response: Response = entitygraph.base_api_client.make_request(
            'DELETE',
            endpoint,
            headers=headers
        )
        response.raise_for_status()

    @staticmethod
    def delete_entity_by_id(entity_id: str, application_label: str):
        """Delete an entity by its ID

        :param entity_id: ID of the entity to delete.
        :type entity_id: str
        :param application_label: The application label of the entity.
        :type application_label: str
        """

        endpoint = f"api/entities/{entity_id}"
        headers = {
            'X-Application': application_label,
            'Accept': 'application/ld+json'
        }
        response: Response = entitygraph.base_api_client.make_request(
            'DELETE',
            endpoint,
            headers=headers
        )
        response.raise_for_status()

