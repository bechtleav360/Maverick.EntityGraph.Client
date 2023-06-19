from entitygraph.base_client import BaseApiClient


class TransactionsAPI(BaseApiClient):
    def read_transaction(self, id):
        endpoint = f"/api/transactions/{id}"
        return self.make_request('GET', endpoint)

    def list_transactions(self, limit=100, offset=0):
        endpoint = "/api/transactions"
        params = {"limit": limit, "offset": offset}
        return self.make_request('GET', endpoint, params=params)