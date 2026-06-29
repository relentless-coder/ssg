import unittest
from blocknode import (
    block_to_block_type,
    BlockType,
    paragraph_to_html_node,
    heading_to_html_node,
    code_to_html_node,
    quote_to_html_node,
    unordered_list_to_html_node,
    ordered_list_to_html_node,
)


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


class TestBlockToHtmlNode(unittest.TestCase):
    def test_paragraph(self):
        node = paragraph_to_html_node("This is a paragraph")
        self.assertEqual(node.to_html(), "<p>This is a paragraph</p>")

    def test_paragraph_with_inline_formatting(self):
        node = paragraph_to_html_node("This is **bold** and _italic_")
        self.assertEqual(
            node.to_html(),
            "<p>This is <b>bold</b> and <i>italic</i></p>",
        )

    def test_heading_h1(self):
        node = heading_to_html_node("# Heading")
        self.assertEqual(node.to_html(), "<h1>Heading</h1>")

    def test_heading_h6(self):
        node = heading_to_html_node("###### Heading")
        self.assertEqual(node.to_html(), "<h6>Heading</h6>")

    def test_code_block(self):
        node = code_to_html_node("```\ncode line\n```")
        self.assertEqual(node.to_html(), "<pre><code>code line</code></pre>")

    def test_code_block_with_language(self):
        node = code_to_html_node("```python\nprint('hi')\n```")
        self.assertEqual(node.to_html(), "<pre><code>print('hi')</code></pre>")

    def test_quote_single_line(self):
        node = quote_to_html_node("> A quote")
        self.assertEqual(node.to_html(), "<blockquote>A quote</blockquote>")

    def test_quote_multi_line(self):
        node = quote_to_html_node("> Line one\n> Line two")
        self.assertEqual(
            node.to_html(),
            "<blockquote>Line one\nLine two</blockquote>",
        )

    def test_quote_with_inline_formatting(self):
        node = quote_to_html_node("> **bold** quote")
        self.assertEqual(
            node.to_html(),
            "<blockquote><b>bold</b> quote</blockquote>",
        )

    def test_unordered_list_simple(self):
        node = unordered_list_to_html_node("- one\n- two\n- three")
        self.assertEqual(
            node.to_html(),
            "<ul><li>one</li><li>two</li><li>three</li></ul>",
        )

    def test_unordered_list_with_inline_formatting(self):
        node = unordered_list_to_html_node("- **bold** item\n- _italic_ item")
        self.assertEqual(
            node.to_html(),
            "<ul><li><b>bold</b> item</li><li><i>italic</i> item</li></ul>",
        )

    def test_unordered_list_with_continuation(self):
        node = unordered_list_to_html_node("- item one\n  continuation\n- item two")
        self.assertEqual(
            node.to_html(),
            "<ul><li>item one\n  continuation</li><li>item two</li></ul>",
        )

    def test_ordered_list_simple(self):
        node = ordered_list_to_html_node("1. one\n2. two\n3. three")
        self.assertEqual(
            node.to_html(),
            "<ol><li>one</li><li>two</li><li>three</li></ol>",
        )

    def test_ordered_list_double_digit(self):
        node = ordered_list_to_html_node("10. ten\n11. eleven")
        self.assertEqual(
            node.to_html(),
            "<ol><li>ten</li><li>eleven</li></ol>",
        )

    def test_ordered_list_with_inline_formatting(self):
        node = ordered_list_to_html_node("1. `code` item\n2. [link](https://boot.dev)")
        self.assertEqual(
            node.to_html(),
            "<ol><li><code>code</code> item</li><li><a href='https://boot.dev' target='_blank'>link</a></li></ol>",
        )

    def test_ordered_list_with_continuation(self):
        node = ordered_list_to_html_node("1. item one\n   continuation\n2. item two")
        self.assertEqual(
            node.to_html(),
            "<ol><li>item one\n   continuation</li><li>item two</li></ol>",
        )
