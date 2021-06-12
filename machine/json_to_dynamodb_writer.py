import json
import logging
from typing import Dict, List, Set

from aws_wrappers.dynamodb.database import Database
from workflow.consumer import Consumer


class JSONToDynamoWriter(Consumer):
    def __init__(
        self,
        table: str,
        database: Database = None,
    ) -> None:
        database = database or Database()
        self.table = database.tables.get(table)
        self.batch_size = 25
        self.current_batch: List[Dict] = []

    @property
    def required_columns(self) -> Set:
        return {'json'}

    def process(self, item: Dict) -> None:
        try:
            row = json.loads(item.get('json'))
            self.current_batch.append(row)
            if len(self.current_batch) >= self.batch_size:
                self.write_batch()
        except (json.decoder.JSONDecodeError, TypeError) as err:
            logging.exception(str(err))

    def write_batch(self):
        self.table.write_batch_items(self.current_batch)
        self.current_batch = []

    def teardown(self, item: Dict) -> None:
        if len(self.current_batch) > 0:
            self.write_batch()
