class HTMLNode:
    def __init__(self, tag: str = None, value: str = None, children: HTMLNode[] = None, props: dict = None):
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
        res = " "
        for k in self.props:
            res += f"{k}={self.props[k]} "
        return res


    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.__repr__(node) for node in self.children}, {self.props})"
