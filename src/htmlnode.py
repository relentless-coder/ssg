class HTMLNode:
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        props: dict[str, str] | None = None,
        children: list[HTMLNode] | None = None,
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
