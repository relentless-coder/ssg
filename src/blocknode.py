import re
from enum import Enum

from htmlnode import HTMLNode, ParentNode
from split_nodes import text_to_text_nodes
from textnode import TextNode, TextType, text_node_to_html_node


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

def block_to_html_node(text: str) -> ParentNode:
    block_type = block_to_block_type(text)
    match block_type:
        case BlockType.HEADING:
            return heading_to_html_node(text)
        case BlockType.CODE:
            return code_to_html_node(text)
        case BlockType.QUOTE:
            return quote_to_html_node(text)
        case BlockType.UNORDERED_LIST:
            return unordered_list_to_html_node(text)
        case BlockType.ORDERED_LIST:
            return ordered_list_to_html_node(text)
        case _:
            return paragraph_to_html_node(text)


def text_to_children(text: str) -> list[HTMLNode]:
    text_nodes = text_to_text_nodes(text)
    return [text_node_to_html_node(node) for node in text_nodes]


def paragraph_to_html_node(text: str) -> ParentNode:
    html_nodes = text_to_children(text)
    return ParentNode("p", html_nodes)


def code_to_html_node(text: str) -> ParentNode:
    lines = text.strip().split("\n")
    return ParentNode(
        "pre",
        [text_node_to_html_node(TextNode("\n".join(lines[1:-1]), TextType.CODE, None))],
    )


def heading_to_html_node(text: str) -> ParentNode:
    heading_level = 0
    for char in text:
        if char == "#":
            heading_level += 1
        else:
            break
    html_nodes = text_to_children(text[heading_level + 1 :])
    return ParentNode(f"h{heading_level}", html_nodes)


def quote_to_html_node(text: str) -> ParentNode:
    lines = text.split("\n")
    new_lines = []
    for line in lines:
        if line.startswith("> "):
            new_lines.append(line.lstrip("> "))
        elif line.startswith(">"):
            new_lines.append(line.lstrip(">"))
        else:
            new_lines.append(line)
    html_nodes = text_to_children("\n".join(new_lines))
    return ParentNode("blockquote", html_nodes)


def unordered_list_to_html_node(text: str) -> ParentNode:
    lines = text.split("\n")
    list_nodes = []
    acc = []
    for line in lines:
        if re.match(r"- ", line):
            if len(acc) > 0:
                list_nodes.append(
                    ParentNode(
                        "li",
                        text_to_children("\n".join(acc)),
                    )
                )
            acc = [line[2:]]
        else:
            acc.append(line)
    if len(acc) > 0:
        list_nodes.append(ParentNode("li", text_to_children("\n".join(acc))))
    return ParentNode("ul", list_nodes)


def ordered_list_to_html_node(text: str) -> ParentNode:
    lines = text.split("\n")
    list_nodes = []
    acc = []
    for line in lines:
        match = re.match(r"\d+\.\s", line)
        if match:
            if len(acc) > 0:
                list_nodes.append(
                    ParentNode(
                        "li",
                        text_to_children("\n".join(acc)),
                    )
                )
            acc = [line[match.end() :]]
        else:
            acc.append(line)
    if len(acc) > 0:
        list_nodes.append(ParentNode("li", text_to_children("\n".join(acc))))
    return ParentNode("ol", list_nodes)
