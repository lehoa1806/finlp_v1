from typing import Dict, Generator

from utils.postgresql import Database
from workflow.consumer import Consumer


class PostgresBatchInsert(Consumer):
    def __init__(
        self,
        table_name: str,
        batch_size: int,
    ) -> None:
        self.table_name = table_name
        self.batch_size = batch_size
        self.bulk_insert: Generator = None  # type: ignore

    def setup(self, item: Dict) -> None:
        database = Database.load_default_database()
        table = database.load_table(self.table_name)
        self.bulk_insert = table.insert_each(self.batch_size)
        self.bulk_insert.send(None)

    def process(self, item: Dict) -> None:
        self.bulk_insert.send(item)

    def teardown(self, item: Dict) -> None:
        self.bulk_insert.send(None)
