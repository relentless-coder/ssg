import re
from htmlnode import ParentNode
from blocknode import block_to_html_node

def markdown_to_blocks(text: str) -> list[str]:
    res = []
    blocks = text.split("\n\n")
    for block in blocks:
        block = block.strip()
        if block != "":
            res.append(re.sub(r"(\n\s+)", "\n", block))
    return res

def markdown_to_html_node(markdown: str) -> ParentNode:
    html_nodes = [block_to_html_node(block) for block in markdown_to_blocks(markdown)]
    return ParentNode("div", html_nodes)
