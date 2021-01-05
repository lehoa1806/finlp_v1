from copy import deepcopy
from typing import Dict, Iterator, List

from workflow.stage import Stage


class KeyTransformStage(Stage):
    def __init__(
        self,
        original_columns: List[str],
        new_columns: List[str],
    ) -> None:
        super().__init__()
        self.original_columns = original_columns
        self.new_columns = new_columns

    def process(self, item: Dict) -> Iterator:
        if len(self.original_columns) != len(self.new_columns):
            raise ValueError(f'Length mismatch: {self.original_columns} vs '
                             f'{self.new_columns}')
        item = deepcopy(item)
        for in_key, out_key in zip(self.input_columns, self.output_columns):
            item[out_key] = item.pop(in_key, None)
        yield item
