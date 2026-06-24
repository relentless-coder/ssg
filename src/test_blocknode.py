import unittest
from blocknode import block_to_block_type, BlockType


class TestBlockToBlockType(unittest.TestCase):
    def test_h1(self):
        self.assertEqual(block_to_block_type("# Heading"), BlockType.HEADING)

    def test_h6(self):
        self.assertEqual(block_to_block_type("###### Heading"), BlockType.HEADING)

    def test_h7_is_paragraph(self):
        self.assertEqual(block_to_block_type("####### Heading"), BlockType.PARAGRAPH)

    def test_heading_without_space(self):
        self.assertEqual(block_to_block_type("#Heading"), BlockType.PARAGRAPH)

    def test_code_block_simple(self):
        self.assertEqual(block_to_block_type("```\ncode\n```"), BlockType.CODE)

    def test_code_block_with_language(self):
        self.assertEqual(
            block_to_block_type("```python\nprint('hi')\n```"), BlockType.CODE
        )

    def test_inline_code_only(self):
        self.assertEqual(
            block_to_block_type("This has `inline` code"), BlockType.PARAGRAPH
        )

    def test_quote(self):
        self.assertEqual(block_to_block_type("> A quote"), BlockType.QUOTE)

    def test_paragraph_with_greater_than(self):
        self.assertEqual(block_to_block_type("5 > 3"), BlockType.PARAGRAPH)

    def test_unordered_list(self):
        self.assertEqual(
            block_to_block_type("- item one\n- item two"), BlockType.UNORDERED_LIST
        )

    def test_paragraph_with_dash(self):
        self.assertEqual(
            block_to_block_type("This - is not a list"), BlockType.PARAGRAPH
        )

    def test_ordered_list_single_digit(self):
        self.assertEqual(block_to_block_type("1. first"), BlockType.ORDERED_LIST)

    def test_ordered_list_double_digit(self):
        self.assertEqual(block_to_block_type("10. tenth"), BlockType.ORDERED_LIST)

    def test_plain_paragraph(self):
        self.assertEqual(block_to_block_type("Just a paragraph."), BlockType.PARAGRAPH)

    def test_empty_string(self):
        self.assertEqual(block_to_block_type(""), BlockType.PARAGRAPH)
