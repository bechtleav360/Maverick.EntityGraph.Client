from entitygraph.base_client import BaseApiClient


class TransactionsAPI(BaseApiClient):
    def read_transaction(self, id, response_mimetype='application/ld+json'):
        endpoint = f"api/transactions/{id}"
        headers = {'Accept': response_mimetype}
        return self.make_request('GET', endpoint, headers=headers)

    def list_transactions(self, limit=100, offset=0, response_mimetype='application/ld+json'):
        endpoint = "api/transactions"
        params = {"limit": limit, "offset": offset}
        headers = {'Accept': response_mimetype}
        return self.make_request('GET', endpoint, params=params, headers=headers)