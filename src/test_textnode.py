import unittest
from textnode import TextNode, TextType

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



if __name__ == "__main__":
    unittest.main()
