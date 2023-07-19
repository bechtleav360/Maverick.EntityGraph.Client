from typing import List

from requests import Response

import entitygraph


class Transaction:
    def __init__(self):
        if entitygraph.base_client is None:
            raise Exception(
                "Not connected. Please connect using entitygraph.connect(api_key=..., host=...) before using Transaction()")

    def get_by_id(self, id: str) -> 'Transaction':
        endpoint = f"api/transactions/{id}"
        headers = {'Accept': "text/turtle"}
        response: Response = entitygraph.base_client.make_request('GET', endpoint, headers=headers)

        pass

    def get_all(self, limit: int = 100, offset: int = 0) -> List['Transaction']:
        endpoint = "api/transactions"
        params = {"limit": limit, "offset": offset}
        headers = {'Accept': "text/turtle"}
        response: Response = entitygraph.base_client.make_request('GET', endpoint, params=params, headers=headers)

        pass
