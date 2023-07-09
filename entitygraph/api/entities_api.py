from entitygraph.api_response import ApiResponse
from entitygraph.base_client import BaseApiClient


class EntitiesAPI(BaseApiClient):
    # Annotations
    def create_link(self, source_id: str, prefixed_key: str, target_id: str, application_label: str = 'default',
                    response_mimetype: str = 'text/turtle') -> ApiResponse | Exception:
        """
        Create edge to existing entity identified by target id (within the same dataset).

        :param source_id: ID of the source entity
        :param prefixed_key: Prefixed key of the edge
        :param target_id: ID of the target entity
        :param application_label: Label of the application
        :param response_mimetype: text/turtle, application/ld+json or application/json
        """
        endpoint = f"api/entities/{source_id}/links/{prefixed_key}/{target_id}"
        headers = {'X-Application': application_label, 'Accept': response_mimetype}
        return self._make_request('PUT', endpoint, headers=headers)

    def delete_link(self, source_id: str, prefixed_key: str, target_id: str, application_label: str = 'default',
                    response_mimetype: str = 'text/turtle') -> ApiResponse | Exception:
        """
        Deletes edge to existing entity identified by target id.

        :param source_id: ID of the source entity
        :param prefixed_key: Prefixed key of the edge
        :param target_id: ID of the target entity
        :param application_label: Label of the application
        :param response_mimetype: text/turtle, application/ld+json or application/json
        """
        endpoint = f"api/entities/{source_id}/links/{prefixed_key}/{target_id}"
        headers = {'X-Application': application_label, 'Accept': response_mimetype}
        return self._make_request('DELETE', endpoint, headers=headers)

    def set_value(self, entity_id: str, prefixed_key: str, value: str | bytes, lang: str = None, filename: str = None, application_label: str = 'default',
                  request_mimetype: str = 'text/plain', response_mimetype: str = 'text/turtle') -> ApiResponse | Exception:
        """
        Sets a specific value.

        :param prefixed_key: Prefixed key of the value
        :param value: Value
        :param lang: Language
        :param filename: Filename
        :param request_mimetype: text/plain or application/octet-stream
        :param response_mimetype: text/turtle or application/ld+json
        """
        endpoint = f"api/entities/{entity_id}/values/{prefixed_key}"
        headers = {
            'X-Application': application_label,
            'Content-Type': request_mimetype,
            'Accept': response_mimetype
        }
        params = {}
        if lang:
            params['lang'] = lang
        if filename:
            params['filename'] = filename
        return self._make_request('POST', endpoint, headers=headers, data=value, params=(params if params else None))

    def remove_value(self, entity_id: str, prefixed_key: str, lang: str = None, application_label: str = 'default',
                     response_mimetype: str = 'text/turtle') -> ApiResponse | Exception:
        """
        Removes a property value.

        :param prefixed_key: Prefixed key of the value
        :param lang: Language
        :param application_label: Label of the application
        :param response_mimetype: text/turtle or application/ld+json
        """
        endpoint = f"api/entities/{entity_id}/values/{prefixed_key}"
        headers = {'X-Application': application_label, 'Accept': response_mimetype}
        params = {'lang': lang} if lang else None
        return self._make_request('DELETE', endpoint, headers=headers, params=params)

    def get_value_list(self, entity_id: str, application_label: str = 'default', response_mimetype: str = 'text/turtle') -> ApiResponse | Exception:
        """
        Returns a list of value properties of the selected entity.

        :param application_label: Label of the application
        :param response_mimetype: text/turtle, application/ld+json or application/json
        """
        endpoint = f"api/entities/{entity_id}/values"
        headers = {'X-Application': application_label, 'Accept': response_mimetype}
        return self._make_request('GET', endpoint, headers=headers)

    def create_or_update_value_list(self, entity_id: str, values: str | dict, application_label: str = 'default',
                                    response_mimetype: str = 'text/turtle') -> ApiResponse | Exception:
        """
        Create or update multiple value properties for the selected entity.

        :param values: Values to be created or updated
        :param application_label: Label of the application
        :param response_mimetype: text/turtle, application/ld+json or application/json
        """
        endpoint = f"api/entities/{entity_id}/values"
        headers = {'X-Application': application_label, 'Content-Type': 'application/json', 'Accept': response_mimetype}
        return self._make_request('POST', endpoint, headers=headers, data=values)

    def get_links_by_type(self, entity_id: str, prefixed_key: str, application_label: str = 'default',
                          response_mimetype: str = 'text/turtle') -> ApiResponse | Exception:
        """
        Returns all links of the given type.

        :param prefixed_key: Prefixed key of the link
        :param application_label: Label of the application
        :param response_mimetype: text/turtle or application/ld+json
        """
        endpoint = f"api/entities/{entity_id}/links/{prefixed_key}"
        headers = {'X-Application': application_label, 'Accept': response_mimetype}
        return self._make_request('GET', endpoint, headers=headers)

    def get_all_links(self, entity_id: str, application_label: str = 'default',
                      response_mimetype: str = 'text/turtle') -> ApiResponse | Exception:
        """
        Returns all links of an entity.

        :param application_label: Label of the application
        :param response_mimetype: text/turtle or application/ld+json
        """
        endpoint = f"api/entities/{entity_id}/links"
        headers = {'X-Application': application_label, 'Accept': response_mimetype}
        return self._make_request('GET', endpoint, headers=headers)

    # Details
    def create_detail(self, entity_id: str, property_type: str, prefixed_value_key: str, prefixed_detail_key: str,
                      application_label: str = 'default', response_mimetype: str = 'text/turtle') -> ApiResponse | Exception:
        """
        Creates a statement about a statement use the post body as value.

        :param property_type: values or links
        :param prefixed_value_key: Prefixed key of the value
        :param prefixed_detail_key: Prefixed key of the detail
        :param application_label: Label of the application
        :param response_mimetype: text/turtle or application/ld+json
        """
        endpoint = f"api/entities/{entity_id}/{property_type}/{prefixed_value_key}/details/{prefixed_detail_key}"
        headers = {'X-Application': application_label, 'Accept': response_mimetype}
        return self._make_request('POST', endpoint, headers=headers)

    def get_details(self, entity_id: str, property_type: str, prefixed_value_key: str, hash_value: bool,
                    application_label: str = 'default', response_mimetype: str = 'text/turtle') -> ApiResponse | Exception:
        """
        Returns all details for a value or link

        :param property_type: values or links
        :param prefixed_value_key: Prefixed key of the value
        :param hash_value: Hash the value
        :param application_label: Label of the application
        :param response_mimetype: text/turtle or application/ld+json
        """
        endpoint = f"api/entities/{entity_id}/{property_type}/{prefixed_value_key}/details"
        headers = {'X-Application': application_label, 'Accept': response_mimetype}
        params = {'hash': hash_value}
        return self._make_request('GET', endpoint, headers=headers, params=params)

    def create_link_detail(self, entity_id: str, property_type: str, prefixed_value_key: str, triples: str,
                           application_label: str = 'default', response_mimetype: str = 'text/turtle') -> ApiResponse | Exception:
        """
        Creates a statement about a statement use the post body as value.

        :param property_type: values or links
        :param prefixed_value_key: Prefixed key of the value
        :param triples: Triples to be created
        :param application_label: Label of the application
        :param response_mimetype: text/turtle or application/ld+json
        """
        endpoint = f"api/entities/{entity_id}/{property_type}/{prefixed_value_key}/details"
        headers = {'X-Application': application_label, 'Content-Type': 'text/x-turtlestar', 'Accept': response_mimetype}
        return self._make_request('POST', endpoint, data=triples, headers=headers)

    def delete_detail(self, entity_id: str, prefixed_value_key: str, prefixed_detail_key: str, multiple: bool = None, hash: str = None,
                      application_label: str = 'default', response_mimetype: str = 'text/turtle') -> ApiResponse | Exception:
        """
        Delete a specific detail for a value

        :param prefixed_value_key: Prefixed key of the value
        :param prefixed_detail_key: Prefixed key of the detail
        :param multiple: Delete multiple details
        :param hash: Hash
        :param response_mimetype: text/turtle or application/ld+json
        """
        endpoint = f"api/entities/{entity_id}/values/{prefixed_value_key}/details/{prefixed_detail_key}"
        params = {'multiple': multiple, 'hash': hash}
        headers = {'X-Application': application_label, 'Accept': response_mimetype}
        return self._make_request('DELETE', endpoint, params=params, headers=headers)

    def purge_details(self, entity_id: str, prefixed_value_key: str, application_label: str = 'default',
                      response_mimetype: str = 'text/turtle') -> ApiResponse | Exception:
        """
        Purge all details for a value

        :param prefixed_value_key: Prefixed key of the value
        :param application_label: Label of the application
        :param response_mimetype: text/turtle or application/ld+json
        """
        endpoint = f"api/entities/{entity_id}/values/{prefixed_value_key}/details"
        headers = {'X-Application': application_label, 'Accept': response_mimetype}
        return self._make_request('DELETE', endpoint, headers=headers)

    # Entities

    def embed(self, entity_id: str, prefixed_key: str, data: str | dict, application_label: str = 'default',
              request_mimetype: str = 'application/ld+json', response_mimetype: str = 'application/ld+json') -> ApiResponse | Exception:
        """
        :param prefixed_key: Prefixed key of the value
        :param data: Data to be embedded
        :param application_label: Label of the application
        :param request_mimetype: application/ld+json or text/turtle
        :param response_mimetype: application/ld+json or text/turtle
        """
        endpoint = f'api/entities/{entity_id}/{prefixed_key}'
        headers = {'X-Application': application_label, 'Content-Type': request_mimetype, 'Accept': response_mimetype}
        return self._make_request('POST', endpoint, headers=headers, data=data)

    def list(self, limit: int = 100, offset: int = 0, application_label: str = 'default',
             response_mimetype: str = 'application/ld+json') -> ApiResponse | Exception:
        """
        Returns a list of entities

        :param limit: Maximum number of entities to return
        :param offset: Offset of the first entities to return
        :param application_label: Label of the application
        :param response_mimetype: application/ld+json, text/turtle or text/n3
        """
        endpoint = 'api/entities'
        params = {'limit': limit, 'offset': offset}
        headers = {'X-Application': application_label, 'Accept': response_mimetype}
        return self._make_request('GET', endpoint, headers=headers, params=params)

    def create(self, data: str | dict, application_label: str = 'default',
               request_mimetype: str = 'application/ld+json', response_mimetype: str = 'application/ld+json') -> ApiResponse | Exception:
        """
        :param data: Data to be created
        :param application_label: Label of the application
        :param request_mimetype: application/ld+json, text/turtle or text/n3
        :param response_mimetype: application/ld+json, text/turtle or text/n3
        """
        endpoint = 'api/entities'
        headers = {'X-Application': application_label, 'Content-Type': request_mimetype, 'Accept': response_mimetype}
        return self._make_request('POST', endpoint, headers=headers, data=data)

    def read(self, entity_id: str, property: str = None, application_label: str = 'default',
             response_mimetype: str = 'application/ld+json') -> ApiResponse | Exception:
        """
        Returns an entity with the given unique identifier.

        :param property: Property to be returned
        :param application_label: Label of the application
        :param response_mimetype: application/ld+json, text/turtle or text/n3
        """
        endpoint = f'api/entities/{entity_id}'
        headers = {'X-Application': application_label, 'Accept': response_mimetype}
        params = {'property': property} if property else None
        return self._make_request('GET', endpoint, headers=headers, params=params)

    def delete(self, entity_id: str, application_label: str = 'default',
               response_mimetype: str = 'application/ld+json') -> ApiResponse | Exception:
        """
        Deletes an entity with the given unique identifier.

        :param application_label: Label of the application
        :param response_mimetype: application/ld+json, text/turtle or text/n3
        """
        endpoint = f'api/entities/{entity_id}'
        headers = {'X-Application': application_label, 'Accept': response_mimetype}
        return self._make_request('DELETE', endpoint, headers=headers)
