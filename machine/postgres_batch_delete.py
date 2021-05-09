from typing import Dict, Generator

from utils.postgresql import Database
from workflow.consumer import Consumer


class PostgresBatchDelete(Consumer):
    def __init__(
        self,
        table_name: str,
        batch_size: int,
    ) -> None:
        self.table_name = table_name
        self.batch_size = batch_size
        self.bulk_delete: Generator = None  # type: ignore

    def setup(self, item: Dict) -> None:
        database = Database.load_default_database()
        table = database.load_table(self.table_name)
        self.bulk_delete = table.delete_each(self.batch_size)
        self.bulk_delete.send(None)

    def process(self, item: Dict) -> None:
        self.bulk_delete.send(item)

    def teardown(self, item: Dict) -> None:
        self.bulk_delete.send(None)
