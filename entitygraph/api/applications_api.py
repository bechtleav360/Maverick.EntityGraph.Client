from entitygraph.base_client import BaseApiClient


class ApplicationsAPI(BaseApiClient):
    def list_applications(self):
        endpoint = "/api/applications"
        return self.make_request('GET', endpoint)

    def create_application(self, application_data):
        endpoint = "/api/applications"
        return self.make_request('POST', endpoint, data=application_data)

    def list_subscriptions(self, application_key):
        endpoint = f"/api/applications/{application_key}/subscriptions"
        return self.make_request('GET', endpoint)

    def generate_key(self, application_key, key_request):
        endpoint = f"/api/applications/{application_key}/subscriptions"
        return self.make_request('POST', endpoint, data=key_request)

    def create_configuration(self, application_key, configuration_key, configuration_data):
        endpoint = f"/api/applications/{application_key}/configuration/{configuration_key}"
        return self.make_request('POST', endpoint, data=configuration_data)

    def delete_configuration(self, application_key, configuration_key):
        endpoint = f"/api/applications/{application_key}/configuration/{configuration_key}"
        return self.make_request('DELETE', endpoint)

    def query_application(self, query):
        endpoint = "/api/applications/query"
        return self.make_request('POST', endpoint, data=query)

    def get_application(self, application_key):
        endpoint = f"/api/applications/{application_key}"
        return self.make_request('GET', endpoint)

    def delete_application(self, application_key):
        endpoint = f"/api/applications/{application_key}"
        return self.make_request('DELETE', endpoint)

    def revoke_token(self, application_key, label):
        endpoint = f"/api/applications/{application_key}/subscriptions/{label}"
        return self.make_request('DELETE', endpoint)