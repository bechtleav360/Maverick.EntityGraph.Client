from typing import List

import entitygraph
from entitygraph import TransactionsAPI


class Transaction:
    def __init__(self):
        if entitygraph.client is not None:
            self.__api: TransactionsAPI = entitygraph.client.transactions_api
        else:
            raise Exception(
                "Not connected. Please connect using entitygraph.connect(api_key=..., host=...) before using Transaction()")

    def get_by_id(self, id: str) -> 'Transaction':
        pass

    def get_all(self) -> List['Transaction']:
        pass
