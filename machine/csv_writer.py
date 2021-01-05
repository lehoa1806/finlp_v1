import csv
from typing import Dict, List, TextIO

from workflow.consumer import Consumer


class CsvWriter(Consumer):
    def __init__(
        self,
        text: TextIO,
        fieldnames: List[str],
        with_header: bool = False,
    ) -> None:
        self.fieldnames = fieldnames
        self.writer = csv.DictWriter(
            text,
            fieldnames=fieldnames,
            delimiter='\t',
            quotechar='',
            quoting=csv.QUOTE_NONE,
            escapechar='\\',
        )
        if with_header:
            self.writer.writeheader()

    def process(self, item: Dict) -> None:
        if not set(self.fieldnames).issubset(set(item.keys())):
            raise ValueError(f'Invalid data fields: {item.keys()}. '
                             f'Required columns: {self.fieldnames}.')
        self.writer.writerow({
            k: item[k] for k in self.fieldnames
        })
