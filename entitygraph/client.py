from entitygraph.api import AdminAPI, TransactionsAPI, ApplicationsAPI, QueryAPI, EntitiesAPI


class Client:
    def __init__(self, api_key: str, host: str = "https://entitygraph.azurewebsites.net/",
                 ignore_ssl: bool = False):
        self.base_url = host
        self.api_key = api_key
        self.ignore_ssl = ignore_ssl
        self._admin_api = None
        self._transactions_api = None
        self._applications_api = None

    @property
    def admin_api(self):
        if self._admin_api is None:
            self._admin_api = AdminAPI(self.api_key, self.base_url, self.ignore_ssl)
        return self._admin_api

    @property
    def transactions_api(self):
        if self._transactions_api is None:
            self._transactions_api = TransactionsAPI(self.api_key, self.base_url, self.ignore_ssl)
        return self._transactions_api

    @property
    def applications_api(self):
        if self._applications_api is None:
            self._applications_api = ApplicationsAPI(self.api_key, self.base_url, self.ignore_ssl)
        return self._applications_api

    @property
    def query_api(self):
        if self._query_api is None:
            self._query_api = QueryAPI(self.api_key, self.base_url, self.ignore_ssl)
        return self._query_api

    @property
    def entities_api(self):
        if self._entities_api is None:
            self._entities_api = EntitiesAPI(self.api_key, self.base_url, self.ignore_ssl)
        return self._entities_api
