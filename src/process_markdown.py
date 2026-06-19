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
