import unittest
from textnode import TextType
from process_markdown import text_to_text_nodes, markdown_to_blocks


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


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_block(self):
        md = """
            This is **bolded** paragraph

            This is another paragraph with _italic_ text and `code` here
            This is the same paragraph on a new line

            - This is a list
            - with items
            """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_single_paragraph(self):
        md = "This is a single paragraph."
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["This is a single paragraph."])

    def test_multiple_blank_lines_between_blocks(self):
        md = "Block one\n\n\n\nBlock two"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Block one", "Block two"])

    def test_leading_and_trailing_whitespace(self):
        md = """
    Leading paragraph

    Trailing paragraph
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            ["Leading paragraph", "Trailing paragraph"],
        )

    def test_indented_lines_get_collapsed(self):
        md = """
Line one

Line two
    still part of line two
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            ["Line one", "Line two\nstill part of line two"],
        )

    def test_heading_and_paragraph(self):
        md = "# Heading\n\nThis is a paragraph."
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["# Heading", "This is a paragraph."])

    def test_unordered_list_single_block(self):
        md = "- item one\n- item two\n- item three"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["- item one\n- item two\n- item three"])

    def test_ordered_list_single_block(self):
        md = "1. first\n2. second\n3. third"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["1. first\n2. second\n3. third"])

    def test_code_block_preserves_internal_newlines(self):
        md = "```\ncode line one\n    code line two\ncode line three\n```"
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            ["```\ncode line one\ncode line two\ncode line three\n```"],
        )

    def test_empty_string(self):
        blocks = markdown_to_blocks("")
        self.assertEqual(blocks, [])

    def test_only_whitespace(self):
        blocks = markdown_to_blocks("   \n\n  \n\n  ")
        self.assertEqual(blocks, [])

    def test_blockquote(self):
        md = "> Quote line one\nQuote line two"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["> Quote line one\nQuote line two"])

    def test_mixed_block_types(self):
        md = """
# Heading

This is a paragraph with `code`.

- list item one
- list item two

> a quote
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# Heading",
                "This is a paragraph with `code`.",
                "- list item one\n- list item two",
                "> a quote",
            ],
        )

    def test_unicode_content(self):
        md = "Привет, мир\n\nこんにちは"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Привет, мир", "こんにちは"])
