from enum import Enum
from htmlnode import LeafNode


class TextType(Enum):
    PLAIN = "plain"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str | None = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TextNode):
            return NotImplemented
        if self.text != other.text:
            return False
        if self.text_type != other.text_type:
            return False
        if self.url != other.url:
            return False
        return True

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    match text_node.text_type:
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.LINK:
            if text_node.url is None:
                raise ValueError("URL is required for a tag")
            return LeafNode(
                "a", text_node.text, {"href": text_node.url, "target": "_blank"}
            )
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.IMAGE:
            if text_node.url is None:
                raise ValueError("URL is required for img tag")
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            return LeafNode(None, text_node.text)
