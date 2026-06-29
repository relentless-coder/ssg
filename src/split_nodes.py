import re
from textnode import TextNode, TextType

def text_to_text_nodes(text: str) -> list[TextNode]:
    nodes = [TextNode(text, TextType.PLAIN, None)]
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_links(nodes)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    return nodes

def add_text_node_to_res(
    text: str, text_type: TextType, url: str | None, res: list[TextNode]
):
    res.append(TextNode(text, text_type, url))


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    res = []

    for node in old_nodes:
        items = node.text.split(delimiter)
        if len(items) % 2 == 0:
            raise ValueError("Invalid markdown syntax")
        for i in range(len(items)):
            if i % 2 == 0:
                if items[i] != "":
                    add_text_node_to_res(items[i], node.text_type, node.url, res)
            else:
                add_text_node_to_res(items[i], text_type, None, res)

    return res


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    res = []

    for node in old_nodes:
        matches = extract_markdown_images(node.text)
        if len(matches) > 0:
            curr_pos = 0
            for text, url in matches:
                link_index = node.text.find(f"![{text}]({url})")
                if curr_pos < link_index:
                    add_text_node_to_res(
                        node.text[curr_pos:link_index], node.text_type, node.url, res
                    )
                add_text_node_to_res(text, TextType.IMAGE, url, res)
                ln = len(f"![{text}]({url})")
                curr_pos += ln + link_index
            if curr_pos < len(node.text):
                add_text_node_to_res(
                    node.text[curr_pos : len(node.text)], node.text_type, node.url, res
                )
        else:
            add_text_node_to_res(node.text, node.text_type, node.url, res)

    return res


def split_nodes_links(old_nodes: list[TextNode]) -> list[TextNode]:
    res = []

    for node in old_nodes:
        matches = extract_markdown_links(node.text)
        if len(matches) > 0:
            curr_pos = 0
            for text, url in matches:
                link_index = node.text.find(f"[{text}]({url})")
                if curr_pos < link_index:
                    add_text_node_to_res(
                        node.text[curr_pos:link_index], node.text_type, node.url, res
                    )
                add_text_node_to_res(text, TextType.LINK, url, res)
                curr_pos += len(f"[{text}]({url})") + link_index

            if curr_pos < len(node.text):
                add_text_node_to_res(
                    node.text[curr_pos : len(node.text)], node.text_type, node.url, res
                )
        else:
            add_text_node_to_res(node.text, node.text_type, node.url, res)

    return res


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    return re.findall(r"\!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    return re.findall(r"(?<!\!)\[(.*?)\]\((.*?)\)", text)
