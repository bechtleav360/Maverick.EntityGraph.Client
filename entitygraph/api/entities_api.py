from entitygraph.base_client import BaseApiClient


class EntitiesAPI(BaseApiClient):
    # Annotations
    def create_link(self, source_id: str, prefixed_key: str, target_id: str, application_label: str = 'default',
                    response_mimetype: str = 'text/turtle'):
        """
        Create edge to existing entity identified by target id (within the same dataset).
        """
        endpoint = f"api/entities/{source_id}/links/{prefixed_key}/{target_id}"
        headers = {'X-Application': application_label, 'Accept': response_mimetype}
        return self.make_request('PUT', endpoint, headers=headers)

    def delete_link(self, source_id: str, prefixed_key: str, target_id: str, application_label: str = 'default',
                    response_mimetype: str = 'text/turtle'):
        """
        Deletes edge to existing entity identified by target id.
        """
        endpoint = f"api/entities/{source_id}/links/{prefixed_key}/{target_id}"
        headers = {'X-Application': application_label, 'Accept': response_mimetype}
        return self.make_request('DELETE', endpoint, headers=headers)

    def set_value(self, id: str, prefixed_key: str, value: str, lang: str = None, filename: str = None, application_label: str = 'default',
                  response_mimetype: str = 'text/turtle'):
        """
        Sets a specific value.

        :param response_mimetype: text/turtle or application/ld+json
        """
        endpoint = f"api/entities/{id}/values/{prefixed_key}"
        headers = {
            'X-Application': application_label,
            'Content-Type': 'text/plain' if isinstance(value, str) else 'application/octet-stream',
            'Accept': response_mimetype
        }
        params = {'lang': lang, 'filename': filename} if lang or filename else None
        return self.make_request('POST', endpoint, headers=headers, data=value, params=params)

    def remove_value(self, id: str, prefixed_key: str, lang: str = None, application_label: str = 'default',
                     response_mimetype: str = 'text/turtle'):
        """
        Removes a property value.
        """
        endpoint = f"api/entities/{id}/values/{prefixed_key}"
        headers = {'X-Application': application_label, 'Accept': response_mimetype}
        params = {'lang': lang} if lang else None
        return self.make_request('DELETE', endpoint, headers=headers, params=params)

    def get_value_list(self, id: str, application_label: str = 'default', response_mimetype: str = 'text/turtle'):
        """
        Returns a list of value properties of the selected entity.
        """
        endpoint = f"api/entities/{id}/values"
        headers = {'X-Application': application_label, 'Accept': response_mimetype}
        return self.make_request('GET', endpoint, headers=headers)

    def create_or_update_value_list(self, id: str, values: str | dict, application_label: str = 'default',
                                    response_mimetype: str = 'text/turtle'):
        """
        Create or update multiple value properties for the selected entity.
        """
        endpoint = f"api/entities/{id}/values"
        headers = {'X-Application': application_label, 'Content-Type': 'application/json', 'Accept': response_mimetype}
        return self.make_request('POST', endpoint, headers=headers, data=values)

    def get_links_by_type(self, id: str, prefixed_key: str, application_label: str = 'default', response_mimetype: str = 'text/turtle'):
        """
        Returns all links of the given type.
        """
        endpoint = f"api/entities/{id}/links/{prefixed_key}"
        headers = {'X-Application': application_label, 'Accept': response_mimetype}
        return self.make_request('GET', endpoint, headers=headers)

    def get_all_links(self, id: str, application_label: str = 'default', response_mimetype: str = 'text/turtle'):
        """
        Returns all links of an entity.
        """
        endpoint = f"api/entities/{id}/links"
        headers = {'X-Application': application_label, 'Accept': response_mimetype}
        return self.make_request('GET', endpoint, headers=headers)

    # Details
    def create_detail(self, entity_id: str, property_type: str, prefixed_value_key: str, prefixed_detail_key: str,
                      application_label: str = 'default', response_mimetype: str = 'text/turtle'):
        """
        Creates a statement about a statement use the post body as value.

        :param property_type: values or links
        :param response_mimetype: text/turtle or application/ld+json
        """
        endpoint = f"api/entities/{entity_id}/{property_type}/{prefixed_value_key}/details/{prefixed_detail_key}"
        headers = {'X-Application': application_label, 'Accept': response_mimetype}
        return self.make_request('POST', endpoint, headers=headers)

    def get_details(self, entity_id: str, property_type: str, prefixed_value_key: str, hash_value: bool, application_label: str = 'default',
                    response_mimetype: str = 'text/turtle'):
        """
        Returns all details for a value or link

        :param property_type: values or links
        :param response_mimetype: text/turtle or application/ld+json
        """
        endpoint = f"api/entities/{entity_id}/{property_type}/{prefixed_value_key}/details"
        headers = {'X-Application': application_label, 'Accept': response_mimetype}
        params = {'hash': hash_value}
        return self.make_request('GET', endpoint, headers=headers, params=params)

    def create_link_detail(self, id: str, property_type: str, prefixed_value_key: str, triples: str, application_label: str = 'default',
                           response_mimetype: str = 'text/turtle'):
        """
        Creates a statement about a statement use the post body as value.

        :param property_type: values or links
        :param response_mimetype: text/turtle or application/ld+json
        """
        endpoint = f"api/entities/{id}/{property_type}/{prefixed_value_key}/details"
        headers = {'X-Application': application_label, 'Content-Type': 'text/x-turtlestar', 'Accept': response_mimetype}
        return self.make_request('POST', endpoint, data=triples, headers=headers)

    def delete_detail(self, id: str, prefixed_value_key: str, prefixed_detail_key: str, multiple: bool = None, hash: str = None,
                      application_label: str = 'default', response_mimetype: str = 'text/turtle'):
        """
        Delete a specific detail for a value

        :param response_mimetype: text/turtle or application/ld+json
        """
        endpoint = f"api/entities/{id}/values/{prefixed_value_key}/details/{prefixed_detail_key}"
        params = {'multiple': multiple, 'hash': hash}
        headers = {'X-Application': application_label, 'Accept': response_mimetype}
        return self.make_request('DELETE', endpoint, params=params, headers=headers)

    def purge_details(self, id: str, prefixed_value_key: str, application_label: str = 'default', response_mimetype: str = 'text/turtle'):
        """
        Purge all details for a value

        :param response_mimetype: text/turtle or application/ld+json
        """
        endpoint = f"api/entities/{id}/values/{prefixed_value_key}/details"
        headers = {'X-Application': application_label, 'Accept': response_mimetype}
        return self.make_request('DELETE', endpoint, headers=headers)

    # Entities

    def list(self, limit: int = 100, offset: int = 0, application_label: str = 'default', response_mimetype: str = 'application/ld+json'):
        """
        :param response_mimetype: application/ld+json, text/turtle or text/n3
        """
        endpoint = 'api/entities'
        params = {'limit': limit, 'offset': offset}
        headers = {'X-Application': application_label, 'Accept': response_mimetype}
        return self.make_request('GET', endpoint, headers=headers, params=params)

    def create(self, data: str | dict, application_label: str = 'default', request_mimetype: str = 'application/ld+json',
               response_mimetype: str = 'application/ld+json'):
        endpoint = 'api/entities'
        headers = {'X-Application': application_label, 'Content-Type': request_mimetype, 'Accept': response_mimetype}
        return self.make_request('POST', endpoint, headers=headers, data=data)

    def read(self, id: str, property: str = None, application_label: str = 'default', response_mimetype: str = 'application/ld+json'):
        """
        Returns an entity with the given unique identifier.
        """
        endpoint = f'api/entities/{id}'
        headers = {'X-Application': application_label, 'Accept': response_mimetype}
        params = {'property': property} if property else None
        return self.make_request('GET', endpoint, headers=headers, params=params)

    def delete(self, id: str, application_label: str = 'default', response_mimetype: str = 'application/ld+json'):
        endpoint = f'api/entities/{id}'
        headers = {'X-Application': application_label, 'Accept': response_mimetype}
        return self.make_request('DELETE', endpoint, headers=headers)

    def embed(self, id: str, prefixedKey: str, data: str | dict, application_label: str = 'default', request_mimetype: str = 'application/ld+json',
              response_mimetype: str = 'application/ld+json'):
        endpoint = f'api/entities/{id}/{prefixedKey}'
        headers = {'X-Application': application_label, 'Content-Type': request_mimetype, 'Accept': response_mimetype}
        return self.make_request('POST', endpoint, headers=headers, data=data)
