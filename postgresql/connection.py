from typing import Any, Dict, Iterable, Iterator, Tuple
from uuid import uuid1


class Connection:
    def __init__(self, psycopg2_client) -> None:
        self.psycopg2_client = psycopg2_client

    def execute(
        self,
        command: str,
        params: Iterable[Any] = None,
    ) -> None:
        with self.psycopg2_client:
            with self.psycopg2_client.cursor() as cursor:
                cursor.execute(command, params)

    def query(
        self,
        query: str,
        keys: Tuple,
    ) -> Iterator[Dict[str, str]]:
        with self.psycopg2_client:
            with self.psycopg2_client.cursor(name=str(uuid1())) as cursor:
                cursor.execute(query)
                for row in cursor:
                    if len(row) != len(keys):
                        continue
                    yield dict(zip(keys, row))
