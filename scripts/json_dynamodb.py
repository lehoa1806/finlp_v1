import json
from argparse import Namespace
from typing import Any, Dict, Iterator, TextIO

from aws_wrappers.dynamodb.database import Database
from machine.json_to_dynamodb_writer import JSONToDynamoWriter
from machine.text_writer import TextWriter
from utils.argument_parser import ArgumentParser
from utils.json_encoder import CustomJSONEncoder
from workflow.consumer import Consumer
from workflow.job import Job
from workflow.pipeline import Pipeline
from workflow.single_item_producer import SingleItemProducer
from workflow.stage import Stage


class Worker(Job):
    def parse_args(self) -> Namespace:
        parser = ArgumentParser(
            description='Script to export/import DynamoDB table to/from JSON',
        )
        parser.add_argument(
            '--operator',
            choices=['export', 'import'],
            type=str,
            required=True,
            help='Action: Export data to JSON/Import data from JSON'
        )
        parser.add_argument(
            '--table',
            type=str,
            required=True,
            help='Table name'
        )
        parser.add_file_input(
            name='json-in',
            required=False,
            description='JSON file name'
        )
        parser.add_file_output(
            name='json-out',
            required=False,
            description='JSON file name'
        )

        args = parser.arguments
        if args.operator == 'export' and args.json_out is None:
            parser.error("--export requires --json-out.")
        elif args.operator == 'import' and args.json_in is None:
            parser.error("--import requires --json-in.")

        return args

    @property
    def database(self) -> Database:
        return Database()

    @property
    def consumer(self) -> Consumer:
        if self.args.operator == 'export':
            return TextWriter(text_out=self.args.json_out)
        elif self.args.operator == 'import':
            return JSONToDynamoWriter(
                table=self.args.table, database=self.database)
        else:
            raise ValueError(f'Invalid operator ({self.args.operator})')

    @property
    def pipeline(self) -> Pipeline:
        if self.args.operator == 'export':
            stage = DynamoDB2JsonStage(
                table=self.args.table, database=self.database)
        elif self.args.operator == 'import':
            stage = Json2DynamoDBStage(json_input=self.args.json_in)
        else:
            raise ValueError(f'Invalid operator ({self.args.operator})')

        return Pipeline(stage=stage)

    @property
    def producer(self):
        return SingleItemProducer({})


class DynamoDB2JsonStage(Stage):
    def __init__(
        self,
        table: str,
        database: Database = None,
    ) -> None:
        super().__init__('Export DynamoDB to JSON')
        database = database or Database()
        self.table = database.tables.get(table)

    def process(self, item: Dict) -> Iterator[Dict[str, Any]]:
        for item in self.table.scan():
            yield {'text': json.dumps(item, sort_keys=True, cls=CustomJSONEncoder)}


class Json2DynamoDBStage(Stage):
    def __init__(
        self,
        json_input: TextIO,
    ) -> None:
        super().__init__('Import JSON to DynamoDB')
        self.json_input = json_input

    def process(self, item: Dict) -> Iterator[Dict[str, Any]]:
        for item in self.json_input:
            yield {'json': item}


if __name__ == "__main__":
    Worker().main()
