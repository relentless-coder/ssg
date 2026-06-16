import unittest
from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq_bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_italic(self):
        node = TextNode("This is an italic node", TextType.ITALIC)
        node2 = TextNode("This is an italic node", TextType.ITALIC)
        node3 = TextNode("This is bold node", TextType.BOLD)
        self.assertEqual(node, node2)
        self.assertNotEqual(node, node3)
        self.assertNotEqual(node2, node3)

    def test_eq_link(self):
        node = TextNode("This is a link node", TextType.LINK, "https://google.com")
        node2 = TextNode("This is a link node", TextType.LINK, "https://google.com")
        node3 = TextNode("This is a text node", TextType.LINK, "https://foogle.com")
        self.assertEqual(node, node2)
        self.assertNotEqual(node2, node3)

    def test_not_eq_text_type(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        node2 = TextNode("This is a bold node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_not_eq_link(self):
        node = TextNode("This is a link node", TextType.LINK, "https://google.com")
        node2 = TextNode("This is a link node", TextType.LINK)
        self.assertNotEqual(node, node2)


class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text_node_to_html_node(self):
        node = TextNode("This is a text node", TextType.PLAIN)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_code_node_to_html_node(self):
        node = TextNode("This is code", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is code")

    def test_link_node_to_html_node(self):
        node = TextNode("This is link", TextType.LINK, "https://google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is link")
        self.assertEqual(
            html_node.props, {"href": "https://google.com", "target": "_blank"}
        )


if __name__ == "__main__":
    unittest.main()
