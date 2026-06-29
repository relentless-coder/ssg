from collections.abc import Sequence

class HTMLNode:
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        props: dict[str, str] | None = None,
        children: list["HTMLNode"] | None = None,
    ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if not self.props:
            return ""
        res = ""
        for k in self.props:
            res += " "
            res += f"{k}={self.props[k]}"
        return res

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {[node.__repr__() for node in self.children] if self.children else None}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(
        self, tag: str | None, value: str | None, props: dict[str, str] | None = None
    ):
        super().__init__(tag, value, props)

    def to_html(self):
        if not self.tag:
            return self.value
        res = f"<{self.tag}"
        if self.props:
            for prop in self.props:
                res += f" {prop}='{self.props[prop]}'"
        if self.value:
            res += f">{self.value}</{self.tag}>"
        else:
            res += "/>"
        return res


class ParentNode(HTMLNode):
    def __init__(
        self, tag: str, children: Sequence[HTMLNode] | None, props: dict[str, str] | None = None
    ):
        super().__init__(tag, None, props, list(children) if children is not None else None)

    def to_html(self):
        if not self.tag:
            raise ValueError("Tag is required for ParentNode")
        children_html = ""
        if self.children:
            for child in self.children:
                children_html += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"
