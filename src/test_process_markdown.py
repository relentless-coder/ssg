import unittest
from textnode import TextType
from process_markdown import text_to_text_nodes


class TestTextToTextNodes(unittest.TestCase):
    def test_text_to_text_nodes(self):
        res = text_to_text_nodes(
            "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        )
        self.assertEqual(len(res), 10)
        self.assertEqual(res[0].text, "This is ")
        self.assertEqual(res[0].text_type, TextType.PLAIN)
        self.assertEqual(res[1].text, "text")
        self.assertEqual(res[1].text_type, TextType.BOLD)
        self.assertEqual(res[3].text, "italic")
        self.assertEqual(res[3].text_type, TextType.ITALIC)
        self.assertEqual(res[5].text, "code block")
        self.assertEqual(res[5].text_type, TextType.CODE)
        self.assertEqual(res[7].text, "obi wan image")
        self.assertEqual(res[7].text_type, TextType.IMAGE)
        self.assertEqual(res[7].url, "https://i.imgur.com/fJRm4Vk.jpeg")

    def test_empty_text_to_text_nodes(self):
        res = text_to_text_nodes("")
        self.assertEqual(len(res), 0)
