import unittest
from htmlnode import ParentNode
from process_markdown import markdown_to_blocks, markdown_to_html_node


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


class TestMarkdownToHtmlNode(unittest.TestCase):
    def test_empty_markdown(self):
        node = markdown_to_html_node("")
        self.assertEqual(node.to_html(), "<div></div>")

    def test_single_paragraph(self):
        node = markdown_to_html_node("This is a paragraph")
        self.assertEqual(node.to_html(), "<div><p>This is a paragraph</p></div>")

    def test_multiple_paragraphs(self):
        node = markdown_to_html_node("Para one\n\nPara two")
        self.assertEqual(
            node.to_html(),
            "<div><p>Para one</p><p>Para two</p></div>",
        )

    def test_heading(self):
        node = markdown_to_html_node("# Heading\n\nSome text")
        self.assertEqual(
            node.to_html(),
            "<div><h1>Heading</h1><p>Some text</p></div>",
        )

    def test_all_headings(self):
        md = "\n\n".join([f"{'#' * i} Heading {i}" for i in range(1, 7)])
        node = markdown_to_html_node(md)
        expected = "".join([f"<h{i}>Heading {i}</h{i}>" for i in range(1, 7)])
        self.assertEqual(node.to_html(), f"<div>{expected}</div>")

    def test_code_block(self):
        node = markdown_to_html_node("```\ncode line\n```")
        self.assertEqual(
            node.to_html(),
            "<div><pre><code>code line</code></pre></div>",
        )

    def test_quote(self):
        node = markdown_to_html_node("> A quote\n\nSome text")
        self.assertEqual(
            node.to_html(),
            "<div><blockquote>A quote</blockquote><p>Some text</p></div>",
        )

    def test_unordered_list(self):
        node = markdown_to_html_node("- one\n- two\n- three")
        self.assertEqual(
            node.to_html(),
            "<div><ul><li>one</li><li>two</li><li>three</li></ul></div>",
        )

    def test_ordered_list(self):
        node = markdown_to_html_node("1. one\n2. two\n3. three")
        self.assertEqual(
            node.to_html(),
            "<div><ol><li>one</li><li>two</li><li>three</li></ol></div>",
        )

    def test_inline_formatting(self):
        node = markdown_to_html_node("This is **bold** and _italic_ and `code`")
        self.assertEqual(
            node.to_html(),
            "<div><p>This is <b>bold</b> and <i>italic</i> and <code>code</code></p></div>",
        )

    def test_link_and_image(self):
        node = markdown_to_html_node(
            "An ![image](https://example.com/img.png) and a [link](https://example.com)"
        )
        self.assertEqual(
            node.to_html(),
            "<div><p>An <img src='https://example.com/img.png' alt='image'/> and a <a href='https://example.com' target='_blank'>link</a></p></div>",
        )

    def test_mixed_blocks(self):
        md = """# Heading

This is a paragraph with **bold**.

- item one
- item two

1. first
2. second

> a quote

```
code
```"""
        node = markdown_to_html_node(md)
        expected = (
            "<div>"
            "<h1>Heading</h1>"
            "<p>This is a paragraph with <b>bold</b>.</p>"
            "<ul><li>item one</li><li>item two</li></ul>"
            "<ol><li>first</li><li>second</li></ol>"
            "<blockquote>a quote</blockquote>"
            "<pre><code>code</code></pre>"
            "</div>"
        )
        self.assertEqual(node.to_html(), expected)

    def test_returns_parent_node(self):
        node = markdown_to_html_node("hello")
        self.assertIsInstance(node, ParentNode)
        self.assertEqual(node.tag, "div")
