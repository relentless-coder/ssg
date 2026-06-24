import re
from textnode import TextNode, TextType
from split_nodes import split_nodes_delimiter, split_nodes_image, split_nodes_links


def text_to_text_nodes(text: str) -> list[TextNode]:
    nodes = [TextNode(text, TextType.PLAIN, None)]
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_links(nodes)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    return nodes


def markdown_to_blocks(text: str) -> list[str]:
    res = []
    blocks = text.split("\n\n")
    for block in blocks:
        block = block.strip()
        if block != "":
            res.append(re.sub(r"(\n\s+)", "\n", block))
    return res
