from typing import List, Optional, Union

from slack.web.classes.blocks import (BlockElement, ContextBlock, DividerBlock,
                                      HeaderBlock, ImageBlock, SectionBlock)
from slack.web.classes.messages import Message
from slack.web.classes.objects import TextObject


class SlackMessage:
    def __init__(
        self,
        title: str
    ):
        self.title = title
        self.blocks: List = []

    def add_section(
        self,
        text: Union[str, TextObject] = None,
        block_id: str = None,
        fields: List[str] = None,
        accessory: Optional[BlockElement] = None,
        section: Optional[SectionBlock] = None,
    ) -> 'SlackMessage':
        if any([text, block_id, fields, accessory]):
            self.blocks.append(
                SectionBlock(text=text, block_id=block_id, fields=fields,
                             accessory=accessory)
            )
        if section:
            self.blocks.append(section)
        return self

    def add_divider(self) -> 'SlackMessage':
        self.blocks.append(DividerBlock())
        return self

    def add_header(
        self,
        text: str,
    ) -> 'SlackMessage':
        self.blocks.append(
            HeaderBlock(text=TextObject(text=text, subtype='plain_text'))
        )
        return self

    def add_image(
        self,
        image_url: str,
        title: str,
        alt_text: Optional[str] = None,
        block_id: Optional[str] = None,
        image: Optional[ImageBlock] = None,
    ) -> 'SlackMessage':
        alt_text = alt_text or title
        if any([image_url, alt_text, title, block_id]):
            self.blocks.append(
                ImageBlock(image_url=image_url, alt_text=alt_text, title=title,
                           block_id=block_id)
            )
        if image:
            self.blocks.append(image)
        return self

    def add_context(
        self,
        elements: List[Union[ImageBlock, TextObject]],
        block_id: Optional[str] = None,
        context: Optional[ContextBlock] = None,
    ) -> 'SlackMessage':
        if any([elements, block_id]):
            self.blocks.append(
                ContextBlock(elements=elements, block_id=block_id))
        if context:
            self.blocks.append(context)
        return self

    def to_message(self) -> Message:
        return Message(text=self.title, blocks=self.blocks)
