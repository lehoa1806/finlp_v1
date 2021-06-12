from typing import Dict, Set, TextIO

from workflow.consumer import Consumer


class TextWriter(Consumer):
    def __init__(
        self,
        text_out: TextIO,
    ) -> None:
        self.text_out = text_out

    @property
    def required_columns(self) -> Set:
        return {'text'}

    def process(self, item: Dict) -> None:
        self.text_out.write('{}\n'.format(item['text']))
