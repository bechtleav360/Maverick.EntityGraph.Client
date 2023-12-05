from typing import List

from requests import Response

import entitygraph


class Transaction:
    @classmethod
    def get_by_id(self, id: str) -> "Transaction":
        endpoint = f"api/transactions/{id}"
        headers = {'Accept': "text/turtle"}
        response: Response = entitygraph.base_api_client.make_request('GET', endpoint, headers=headers)

        pass

    def get_all(self, limit: int = 100, offset: int = 0) -> List['Transaction']:
        endpoint = "api/transactions"
        params = {"limit": limit, "offset": offset}
        headers = {'Accept': "text/turtle"}
        response: Response = entitygraph.base_api_client.make_request('GET', endpoint, params=params, headers=headers)

        pass
