import unittest
from textnode import TextNode, TextType
from split_nodes import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_links,
)


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
            "Hello **world** test me **again please**, it's great to see **you**",
            TextType.PLAIN,
        )
        node2 = TextNode("Another world come time again", TextType.PLAIN)
        node3 = TextNode("Hello **world** test", TextType.PLAIN)
        res: list[TextNode] = split_nodes_delimiter(
            [node, node2, node3], "**", TextType.BOLD
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


class ExtractMarkdown(unittest.TestCase):
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("link", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def text_extract_markdown_links_from_mixed_context(self):
        matches = extract_markdown_links(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) ![link](https://google.com)"
        )
        self.assertListEqual([("link", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def text_extract_markdown_images_from_mixed_content(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) [link](https://google.com)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)


class SplitNodesImages(unittest.TestCase):
    def test_split_nodes_images(self):
        node = TextNode(
            "Hello this is an ![image](https://google.com)", TextType.PLAIN, None
        )
        node2 = TextNode("And another one with nothing", TextType.PLAIN, None)
        node3 = TextNode("an image already", TextType.IMAGE, "https://google.com")
        res = split_nodes_image([node, node2, node3])
        self.assertEqual(res[0].text, "Hello this is an ")
        self.assertEqual(res[0].text_type.value, TextType.PLAIN.value)
        self.assertEqual(res[1].text, "image")
        self.assertEqual(res[1].url, "https://google.com")
        self.assertEqual(res[3].text, "an image already")
        self.assertEqual(res[3].text_type.value, TextType.IMAGE.value)

    def test_split_nodes_images_not_links(self):
        node = TextNode(
            "Hello this is an ![image](https://google.com)", TextType.PLAIN, None
        )
        node2 = TextNode("And another one with nothing", TextType.PLAIN, None)
        node3 = TextNode("this is a [link](https://google.com)", TextType.PLAIN, None)
        res = split_nodes_image([node, node2, node3])
        self.assertEqual(res[0].text, "Hello this is an ")
        self.assertEqual(res[0].text_type.value, TextType.PLAIN.value)
        self.assertEqual(res[1].text, "image")
        self.assertEqual(res[1].url, "https://google.com")
        self.assertEqual(res[3].text, "this is a [link](https://google.com)")
        self.assertEqual(res[3].text_type.value, TextType.PLAIN.value)


class SplitNodesLinks(unittest.TestCase):
    def test_split_nodes_links(self):
        node = TextNode(
            "Hello this is an [link](https://google.com)", TextType.PLAIN, None
        )
        node2 = TextNode("And another one with nothing", TextType.PLAIN, None)
        node3 = TextNode("a link already", TextType.LINK, "https://google.com")
        res = split_nodes_links([node, node2, node3])
        self.assertEqual(res[0].text, "Hello this is an ")
        self.assertEqual(res[0].text_type.value, TextType.PLAIN.value)
        self.assertEqual(res[1].text, "link")
        self.assertEqual(res[1].url, "https://google.com")
        self.assertEqual(res[3].text, "a link already")
        self.assertEqual(res[3].text_type.value, TextType.LINK.value)

    def test_split_nodes_links_not_images(self):
        node = TextNode(
            "Hello this is an [link](https://google.com)", TextType.PLAIN, None
        )
        node2 = TextNode("And another one with nothing", TextType.PLAIN, None)
        node3 = TextNode("this is a ![image](https://google.com)", TextType.PLAIN, None)
        res = split_nodes_links([node, node2, node3])
        self.assertEqual(res[0].text, "Hello this is an ")
        self.assertEqual(res[0].text_type.value, TextType.PLAIN.value)
        self.assertEqual(res[1].text, "link")
        self.assertEqual(res[1].url, "https://google.com")
        self.assertEqual(res[3].text, "this is a ![image](https://google.com)")
        self.assertEqual(res[3].text_type.value, TextType.PLAIN.value)
