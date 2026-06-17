import re
from textnode import TextNode, TextType


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    res = []

    def add_to_res(text: str, text_type: TextType):
        res.append(TextNode(text, text_type))

    for node in old_nodes:
        accumulator = ""
        inside = False
        for char in node.text:
            if char != delimiter:
                accumulator += char
            elif char == delimiter:
                if accumulator != "":
                    add_to_res(accumulator, node.text_type if not inside else text_type)
                inside = True if not inside else False
                accumulator = ""
        if accumulator != "":
            if not inside:
                add_to_res(accumulator, node.text_type)
                accumulator = ""
            else:
                raise ValueError("Invalid Markdown syntax")

    return res


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    return re.findall(r"\!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    return re.findall(r"(?<!\!)\[(.*?)\]\((.*?)\)", text)
