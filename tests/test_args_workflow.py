import logging

from utils.argument_parser import ArgumentParser
from workflow.consumer import Consumer
from workflow.job import Job
from workflow.pipeline import Pipeline
from workflow.serial_producer import SerialProducer
from workflow.stage import Stage


def get_stream(x: int = 10):
    for i in range(x):
        yield {
            'operand1': 2 * i,
            'operand2': 2 * i + 1,
            'operand3': 'unnecessary data',
        }


class SimpleStage(Stage):
    @property
    def input_columns(self):
        return ['operand1', 'operand2']

    def process(self, item):
        yield {'sum': item['operand1'] + item['operand2']}


class SimpleConsumer(Consumer):
    def process(self, item):
        logging.info(item.get('sum'))


class SimpleJob(Job):
    def parse_args(self):
        parser = ArgumentParser()
        parser.add_argument(
           'length',
           type=int,
           required=True,
           help='Length of the testing stream',
        )
        return parser.arguments

    @property
    def pipeline(self) -> Pipeline:
        return Pipeline(
            stage=SimpleStage(),
        )

    @property
    def consumer(self):
        return SimpleConsumer()

    @property
    def producer(self):
        return SerialProducer(get_stream(self.args.length))


if __name__ == "__main__":
    # Call the worker
    SimpleJob().main()
    # 1 5 9 13 17 21 25 29 33 37
