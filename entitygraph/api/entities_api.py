from entitygraph.base_client import BaseApiClient


class EntitiesAPI(BaseApiClient):
    # Annotations
    def create_link(self, source_id, prefixed_key, target_id, application_label='default'):
        """
        Create edge to existing entity identified by target id (within the same dataset).
        """
        endpoint = f"/api/entities/{source_id}/links/{prefixed_key}/{target_id}"
        headers = {'X-Application': application_label}
        return self.make_request('PUT', endpoint, headers=headers)

    def delete_link(self, source_id, prefixed_key, target_id, application_label='default'):
        """
        Deletes edge to existing entity identified by target id.
        """
        endpoint = f"/api/entities/{source_id}/links/{prefixed_key}/{target_id}"
        headers = {'X-Application': application_label}
        return self.make_request('DELETE', endpoint, headers=headers)

    def set_value(self, id: str, prefixed_key, value, lang=None, filename=None, application_label='default'):
        """
        Sets a specific value.
        """
        endpoint = f"/api/entities/{id}/values/{prefixed_key}"
        headers = {
            'X-Application': application_label,
            'Content-Type': 'text/plain' if isinstance(value, str) else 'application/octet-stream',
        }
        params = {'lang': lang, 'filename': filename} if lang or filename else None
        return self.make_request('POST', endpoint, headers=headers, data=value, params=params)

    def remove_value(self, id: str, prefixed_key, lang=None, application_label='default'):
        """
        Removes a property value.
        """
        endpoint = f"/api/entities/{id}/values/{prefixed_key}"
        headers = {'X-Application': application_label}
        params = {'lang': lang} if lang else None
        return self.make_request('DELETE', endpoint, headers=headers, params=params)

    def get_value_list(self, id: str, application_label='default'):
        """
        Returns a list of value properties of the selected entity.
        """
        endpoint = f"/api/entities/{id}/values"
        headers = {'X-Application': application_label}
        return self.make_request('GET', endpoint, headers=headers)

    def create_or_update_value_list(self, id: str, values, application_label='default'):
        """
        Create or update multiple value properties for the selected entity.
        """
        endpoint = f"/api/entities/{id}/values"
        headers = {'X-Application': application_label, 'Content-Type': 'application/json'}
        return self.make_request('POST', endpoint, headers=headers, data=values)

    def get_links_by_type(self, id: str, prefixed_key, application_label='default'):
        """
        Returns all links of the given type.
        """
        endpoint = f"/api/entities/{id}/links/{prefixed_key}"
        headers = {'X-Application': application_label}
        return self.make_request('GET', endpoint, headers=headers)

    def get_all_links(self, id: str, application_label='default'):
        """
        Returns all links of an entity.
        """
        endpoint = f"/api/entities/{id}/links"
        headers = {'X-Application': application_label}
        return self.make_request('GET', endpoint, headers=headers)

    # Details
    def create_detail(self, entity_id, property_type, prefixed_value_key, prefixed_detail_key, application_label='default'):
        """
        Creates a statement about a statement use the post body as value.
        """
        endpoint = f"/api/entities/{entity_id}/{property_type}/{prefixed_value_key}/details/{prefixed_detail_key}"
        headers = {'X-Application': application_label}
        return self.make_request('POST', endpoint, headers=headers)

    def get_details(self, entity_id, property_type, prefixed_value_key, hash_value, application_label='default'):
        """
        Returns all details for a value or link
        """
        endpoint = f"/api/entities/{entity_id}/{property_type}/{prefixed_value_key}/details"
        headers = {'X-Application': application_label}
        params = {'hash': hash_value}
        return self.make_request('GET', endpoint, headers=headers, params=params)

    def create_link_detail(self, id: str, type, prefixed_value_key, triples, application_label='default'):
        """
        Creates a statement about a statement use the post body as value.
        """
        endpoint = f"/api/entities/{id}/{type}/{prefixed_value_key}/details"
        headers = {'X-Application': application_label, 'Content-Type': 'text/x-turtlestar'}
        return self.make_request('POST', endpoint, data=triples, headers=headers)

    def delete_detail(self, id: str, prefixed_value_key, prefixed_detail_key, multiple=None, hash=None,
                      application_label='default'):
        """
        Delete a specific detail for a value
        """
        endpoint = f"/api/entities/{id}/values/{prefixed_value_key}/details/{prefixed_detail_key}"
        params = {
            'multiple': multiple,
            'hash': hash
        }
        headers = {'X-Application': application_label}
        return self.make_request('DELETE', endpoint, params=params, headers=headers)

    def purge_details(self, id: str, prefixed_value_key, application_label='default'):
        """
        Purge all details for a value
        """
        endpoint = f"/api/entities/{id}/values/{prefixed_value_key}/details"
        headers = {'X-Application': application_label}
        return self.make_request('DELETE', endpoint, headers=headers)

    # Entities

    def list(self, limit=100, offset=0, application_label='default'):
        params = {'limit': limit, 'offset': offset}
        headers = {'X-Application': application_label, 'Content-Type': 'application/ld+json'}
        return self.make_request('GET', 'api/entities', headers=headers, params=params)

    def create(self, data, application_label='default'):
        headers = {'X-Application': application_label, 'Content-Type': 'application/ld+json'}
        return self.make_request('POST', 'api/entities', headers=headers, data=data)

    def read(self, id: str, property=None, application_label='default'):
        """
        Returns an entity with the given unique identifier.
        """
        headers = {'X-Application': application_label, 'Content-Type': 'application/ld+json'}
        params = {'property': property} if property else None
        return self.make_request('GET', f'api/entities/{id}', headers=headers, params=params)

    def delete(self, id: str, application_label='default'):
        headers = {'X-Application': application_label, 'Content-Type': 'application/ld+json'}
        return self.make_request('DELETE', f'api/entities/{id}', headers=headers)

    def embed(self, id: str, prefixedKey, data, application_label='default'):
        headers = {'X-Application': application_label, 'Content-Type': 'application/ld+json'}
        return self.make_request('POST', f'api/entities/{id}/{prefixedKey}', headers=headers, data=data)
