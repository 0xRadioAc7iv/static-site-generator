import unittest
from converter import markdown_to_html_node


class TestMarkdownToHtmlNode(unittest.TestCase):

    # --- CODE ---

    def test_code_block(self):
        md = "```\ncode here\n```"
        result = markdown_to_html_node(md)
        self.assertEqual(result.to_html(), "<div><pre><code>\ncode here\n</code></pre></div>")

    def test_code_block_preserves_content(self):
        md = "```\ndef foo():\n    return 42\n```"
        result = markdown_to_html_node(md)
        self.assertIn("def foo():", result.to_html())
        self.assertIn("<pre>", result.to_html())
        self.assertIn("<code>", result.to_html())

    # --- PARAGRAPH ---

    def test_paragraph_plain(self):
        result = markdown_to_html_node("plain text")
        self.assertEqual(result.to_html(), "<div><p>plain text</p></div>")

    def test_paragraph_bold(self):
        result = markdown_to_html_node("text with **bold**")
        self.assertEqual(result.to_html(), "<div><p>text with <b>bold</b></p></div>")

    def test_paragraph_italic(self):
        result = markdown_to_html_node("text with _italic_")
        self.assertEqual(result.to_html(), "<div><p>text with <i>italic</i></p></div>")

    def test_paragraph_mixed_inline(self):
        result = markdown_to_html_node("**bold** and _italic_")
        html = result.to_html()
        self.assertIn("<b>bold</b>", html)
        self.assertIn("<i>italic</i>", html)

    # --- HEADING ---

    def test_heading_h1(self):
        result = markdown_to_html_node("# Hello")
        self.assertEqual(result.to_html(), "<div><h1>Hello</h1></div>")

    def test_heading_h2(self):
        result = markdown_to_html_node("## Hello")
        self.assertEqual(result.to_html(), "<div><h2>Hello</h2></div>")

    def test_heading_h6(self):
        result = markdown_to_html_node("###### Hello")
        self.assertEqual(result.to_html(), "<div><h6>Hello</h6></div>")

    # --- QUOTE ---

    def test_quote_single_line(self):
        result = markdown_to_html_node("> a quote")
        self.assertEqual(result.to_html(), "<div><blockquote>a quote</blockquote></div>")

    def test_quote_multi_line(self):
        # ">" prefix must be stripped from every line, not just the first
        result = markdown_to_html_node("> line one\n> line two")
        html = result.to_html()
        self.assertIn("<blockquote>", html)
        self.assertIn("line one", html)
        self.assertIn("line two", html)
        self.assertNotIn(">", html.replace("<blockquote>", "").replace("</blockquote>", "").replace("<div>", "").replace("</div>", ""))

    # --- UNORDERED LIST ---

    def test_unordered_list_single_item(self):
        result = markdown_to_html_node("- item one")
        self.assertEqual(result.to_html(), "<div><ul><li>item one</li></ul></div>")

    def test_unordered_list_item_with_hyphen_in_content(self):
        # strip("-") strips from both ends — "- well-being" must not lose the trailing hyphen
        result = markdown_to_html_node("- well-being")
        self.assertIn("<li>well-being</li>", result.to_html())

    def test_unordered_list_multi_item(self):
        result = markdown_to_html_node("- item one\n- item two\n- item three")
        html = result.to_html()
        self.assertIn("<ul>", html)
        self.assertIn("<li>item one</li>", html)
        self.assertIn("<li>item two</li>", html)
        self.assertIn("<li>item three</li>", html)

    # --- ORDERED LIST ---

    def test_ordered_list_single_item(self):
        result = markdown_to_html_node("1. first item")
        self.assertEqual(
            result.to_html(),
            '<div><ol type="1" start="1"><li>first item</li></ol></div>',
        )

    def test_ordered_list_multi_item(self):
        result = markdown_to_html_node("1. first\n2. second\n3. third")
        html = result.to_html()
        self.assertIn('<ol type="1" start="1">', html)
        self.assertIn("<li>first</li>", html)
        self.assertIn("<li>second</li>", html)
        self.assertIn("<li>third</li>", html)

    def test_ordered_list_non_one_start(self):
        result = markdown_to_html_node("3. third item\n4. fourth item")
        html = result.to_html()
        self.assertIn('<ol type="1" start="3">', html)
        self.assertIn("<li>third item</li>", html)
        self.assertIn("<li>fourth item</li>", html)

    # --- MULTIPLE BLOCKS ---

    def test_multiple_blocks(self):
        md = "# Heading\n\nA paragraph."
        result = markdown_to_html_node(md)
        html = result.to_html()
        self.assertIn("<h1>", html)
        self.assertIn("<p>", html)

    def test_returns_div_wrapper(self):
        result = markdown_to_html_node("some text")
        self.assertTrue(result.to_html().startswith("<div>"))
        self.assertTrue(result.to_html().endswith("</div>"))


if __name__ == "__main__":
    unittest.main()
