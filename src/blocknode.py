import re
from enum import Enum


class BlockType(Enum):
    HEADING = "heading"
    PARAGRAPH = "paragraph"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(text: str) -> BlockType:
    if re.search(r"^#{1,6}\s", text):
        return BlockType.HEADING
    if re.search(r"^`{3}([\s\S]*?)`{3}", text):
        return BlockType.CODE
    if re.search(r"^>", text):
        return BlockType.QUOTE
    if re.search(r"^-\s", text):
        return BlockType.UNORDERED_LIST
    if re.search(r"^\d+\.\s", text):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH
