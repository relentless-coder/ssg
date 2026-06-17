import unittest
from textnode import TextNode, TextType
from split_nodes import split_nodes_delimiter


class SplitNodes(unittest.TestCase):
    def test_split_nodes_delimiter_code(self):
        node = TextNode(
            "Hello `world` test me `again please`, it's great", TextType.PLAIN
        )
        node2 = TextNode("Another world come time again", TextType.PLAIN)
        node3 = TextNode("Hello `world` test", TextType.PLAIN)
        res: list[TextNode] = split_nodes_delimiter(
            [node, node2, node3], "`", TextType.CODE
        )
        self.assertEqual(len(res), 9)
        self.assertEqual(res[0].text, "Hello ")
        self.assertEqual(res[0].text_type.value, TextType.PLAIN.value)
        self.assertEqual(res[7].text, "world")
        self.assertEqual(res[7].text_type.value, TextType.CODE.value)

    def test_split_nodes_delimiter_bold(self):
        node = TextNode(
            "Hello *world* test me *again please*, it's great to see *you*",
            TextType.PLAIN,
        )
        node2 = TextNode("Another world come time again", TextType.PLAIN)
        node3 = TextNode("Hello *world* test", TextType.PLAIN)
        res: list[TextNode] = split_nodes_delimiter(
            [node, node2, node3], "*", TextType.BOLD
        )
        self.assertEqual(len(res), 10)
        self.assertEqual(res[1].text, "world")
        self.assertEqual(res[1].text_type.value, TextType.BOLD.value)
        self.assertEqual(res[4].text, ", it's great to see ")
        self.assertEqual(res[4].text_type.value, TextType.PLAIN.value)

    def test_split_nodes_delimiter_italic(self):
        node = TextNode(
            "Hello _world_ test me _again please_, it's great to see _you_",
            TextType.PLAIN,
        )
        node2 = TextNode("_Another world come time again_", TextType.PLAIN)
        node3 = TextNode("Hello _world_ test", TextType.PLAIN)
        res: list[TextNode] = split_nodes_delimiter(
            [node, node2, node3], "_", TextType.ITALIC
        )
        self.assertEqual(len(res), 10)
        self.assertEqual(res[5].text, "you")
        self.assertEqual(res[5].text_type.value, TextType.ITALIC.value)
        self.assertEqual(res[6].text, "Another world come time again")
        self.assertEqual(res[6].text_type.value, TextType.ITALIC.value)
