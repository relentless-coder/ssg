class HTMLNode:
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        props: dict[str, str] | None = None,
        children: list["HTMLNode"] | None = None,
    ):
        if not value and not children:
            raise ValueError("value and children both cannot be none")
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
        if not self.value:
            raise ValueError
        res = f"<{self.tag}"
        if self.props:
            for prop in self.props:
                res += f" {prop}='{self.props[prop]}'"
        res += f">{self.value}</{self.tag}>"
        return res


class ParentNode(HTMLNode):
    def __init__(
        self, tag: str, children: list[HTMLNode], props: dict[str, str] | None = None
    ):
        super().__init__(tag, None, props, children)

    def to_html(self):
        if not self.tag:
            raise ValueError("Tag is required for ParentNode")
        if not self.children:
            raise ValueError("Children are required for ParentNode")
        children_html = ""
        for child in self.children:
            children_html += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"
