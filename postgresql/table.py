import logging
from typing import Dict, Generator, List

from .connection import Connection


class Table:
    def __init__(
        self,
        connection: Connection,
        table_name: str,
    ) -> None:
        self.connection = connection
        self.name = table_name

    def get_primary_key(self) -> List[str]:
        query = (
            f'SELECT pg_attribute.attname '
            f'FROM pg_index '
            f'JOIN pg_attribute ON pg_attribute.attrelid = pg_index.indrelid '
            f'AND pg_attribute.attnum = ANY ( pg_index.indkey ) '
            f'WHERE pg_index.indrelid = \'{self.name}\'::regclass '
            f'AND pg_index.indisprimary;'
        )
        primary_keys = [
            i['attname'] for i in self.connection.query(query, ('attname',))
        ]
        logging.info(f'Primary keys: {primary_keys}')
        return primary_keys

    def batch_insert(self, items: List[Dict]) -> None:
        """
        Insert a batch of data to the table
        :param items: A list of data
        :return: None
        """
        if len(items) <= 0:
            return
        columns = sorted(items[0].keys())
        value_tokens = ', '.join(['%s'] * len(columns))
        values = [[item[column] for column in columns] for item in items]
        columns_to_insert = ', '.join(columns)
        with self.connection.psycopg2_client.cursor() as cursor:
            values_to_insert = ', '.join(
                cursor.mogrify(f'({value_tokens})', record).decode('utf-8')
                for record in values
            )
        logging.info(f'Inserting {len(items)} records to {self.name}.')
        command = (
            f'INSERT INTO {self.name} ({columns_to_insert}) '
            f'VALUES {values_to_insert} ON CONFLICT DO NOTHING'
        )
        self.connection.execute(command)

    def batch_insert_generator(self, batch_size: int) -> Generator:
        """
        Receive data from self.insert_each, append it to a list then send to
         self.batch_insert
        :param batch_size:
        :return:
        """
        records_to_insert: List[Dict] = []
        while len(records_to_insert) < batch_size:
            record_to_insert = yield
            if record_to_insert is None:
                break
            records_to_insert.append(record_to_insert)
        self.batch_insert(records_to_insert)

    def insert_each(self, batch_size: int = 100) -> Generator:
        batch_generator = None
        while True:
            if batch_generator is None:
                batch_generator = self.batch_insert_generator(batch_size)
                batch_generator.send(None)
            record_to_delete = yield
            try:
                batch_generator.send(record_to_delete)
            except StopIteration:
                batch_generator = None

    def batch_delete(self, items: List[Dict]) -> None:
        """
        Delete a batch of data from the table
        :param items: A list of data
        :return: None
        """
        if len(items) <= 0:
            return
        columns = sorted(items[0].keys())
        primary_keys = sorted(self.get_primary_key())
        if columns != primary_keys:
            logging.error(
                f'Only support batch delete on Primary keys ({primary_keys}): '
                f'input {columns}')
            return
        value_tokens = ', '.join(['%s'] * len(columns))
        values = [[item[column] for column in columns] for item in items]
        columns_to_delete = ', '.join(columns)
        with self.connection.psycopg2_client.cursor() as cursor:
            values_to_delete = ', '.join(
                cursor.mogrify(f'({value_tokens})', record).decode('utf-8')
                for record in values
            )
        logging.info(f'Deleting {len(items)} records from {self.name}.')
        command = (
            f'DELETE FROM {self.name} WHERE ({columns_to_delete}) '
            f'IN (VALUES {values_to_delete})'
        )
        self.connection.execute(command)

    def batch_delete_generator(self, batch_size: int) -> Generator:
        """
        Receive data from self.delete_each, append it to a list then send to
         self.batch_delete
        :param batch_size:
        :return:
        """
        records_to_delete: List[Dict] = []
        while len(records_to_delete) < batch_size:
            record_to_delete = yield
            if record_to_delete is None:
                break
            records_to_delete.append(record_to_delete)
        self.batch_delete(records_to_delete)

    def delete_each(self, batch_size: int = 100) -> Generator:
        batch_generator = None
        while True:
            if batch_generator is None:
                batch_generator = self.batch_delete_generator(batch_size)
                batch_generator.send(None)
            record_to_delete = yield
            try:
                batch_generator.send(record_to_delete)
            except StopIteration:
                batch_generator = None
