import unittest
from htmlnode import HTMLNode


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
