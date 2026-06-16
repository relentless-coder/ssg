import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_html_node_with_correct_values(self):
        test_props = {"href": "https://google.com"}
        node = HTMLNode("a", "A link", test_props)
        self.assertEqual(node.props, test_props)
        self.assertEqual(node.tag, "a")
        self.assertEqual(node.value, "A link")
        self.assertEqual(node.children, None)

    def test_html_node_with_no_value_and_children(self):
        self.assertRaises(ValueError, HTMLNode, "div")

    def test_props_to_html(self):
        node = HTMLNode(
            "a", "A link", {"href": "https://google.com", "target": "_blank"}
        )
        self.assertEqual(node.props_to_html(), " href=https://google.com target=_blank")


class TestLeafNode(unittest.TestCase):
    def test_leaf_node_to_html_p(self):
        leaf_node = LeafNode("p", "I am relentless")
        self.assertEqual(leaf_node.to_html(), "<p>I am relentless</p>")

    def test_leaf_node_to_html_a(self):
        leaf_node = LeafNode(
            "a", "A link", {"href": "https://google.com", "target": "_blank"}
        )
        self.assertEqual(
            leaf_node.to_html(),
            "<a href='https://google.com' target='_blank'>A link</a>",
        )

    def test_leaf_node_to_html_strong(self):
        leaf_node = LeafNode("strong", "Important")
        self.assertEqual(leaf_node.to_html(), "<strong>Important</strong>")


class TestParentNode(unittest.TestCase):
    def test_raises_valueerror_when_no_value(self):
        self.assertRaises(ValueError, ParentNode, "div", None)

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_props(self):
        grandchild_node = LeafNode(
            "a", "grandchild link", {"href": "https://google.com"}
        )
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><a href='https://google.com'>grandchild link</a></span></div>",
        )
