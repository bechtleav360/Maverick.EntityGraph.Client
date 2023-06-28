from entitygraph.api_response import ApiResponse
from entitygraph.base_client import BaseApiClient


class TransactionsAPI(BaseApiClient):
    def read_transaction(self, transaction_id: str, response_mimetype: str = 'application/ld+json') -> ApiResponse | Exception:
        """
        :param transaction_id: Transaction ID
        :param response_mimetype: application/ld+json, text/turtle, application/n-quads or text/n3
        """
        endpoint = f"api/transactions/{transaction_id}"
        headers = {'Accept': response_mimetype}
        return self.make_request('GET', endpoint, headers=headers)

    def list_transactions(self, limit: int = 100, offset: int = 0,
                          response_mimetype: str = 'application/ld+json') -> ApiResponse | Exception:
        """
        :param limit: Maximum number of transactions to return
        :param offset: Offset of the first transaction to return
        :param response_mimetype: application/ld+json, text/turtle, application/n-quads or text/n3
        """
        endpoint = "api/transactions"
        params = {"limit": limit, "offset": offset}
        headers = {'Accept': response_mimetype}
        return self.make_request('GET', endpoint, params=params, headers=headers)
