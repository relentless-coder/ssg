import re
from htmlnode import ParentNode
from enum import Enum
from process_markdown import text_to_text_nodes
from textnode import text_node_to_html_node, TextNode, TextType


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


def paragraph_to_html_node(text: str) -> ParentNode:
    text_nodes = text_to_text_nodes(text)
    html_nodes = []
    for node in text_nodes:
        html_nodes.append(text_node_to_html_node(node))
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
        if char == '#':
            heading_level += 1
        else:
            break
    text_nodes = text_to_text_nodes(text[heading_level + 1:])
    html_nodes = []
    for node in text_nodes:
        html_nodes.append(text_node_to_html_node(node))
    return ParentNode(f"h{heading_level}", html_nodes)

def quote_to_html_node(text: str) -> ParentNode:
    lines = text.split("\n")
    new_lines = []
    for line in lines:
        if line.startswith("> "):
            new_lines.append(line.lstrip('> '))
        elif line.startswith(">"):
            new_lines.append(line.lstrip('>'))
        else:
            new_lines.append(line)
    text_nodes = text_to_text_nodes("\n".join(new_lines))
    html_nodes = []
    for node in text_nodes:
        html_nodes.append(text_node_to_html_node(node))
    return ParentNode("blockquote", html_nodes)
