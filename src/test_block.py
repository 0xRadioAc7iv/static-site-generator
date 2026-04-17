import unittest
from block import *

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
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

    def test_markdown_to_blocks_single_block(self):
        blocks = markdown_to_blocks("Just one block")
        self.assertEqual(blocks, ["Just one block"])

    def test_markdown_to_blocks_extra_blank_lines(self):
        md = "First block\n\n\n\nSecond block"
        blocks = markdown_to_blocks(md)
        self.assertEqual(len(blocks), 2)
        self.assertEqual(blocks[0], "First block")
        self.assertEqual(blocks[1], "Second block")

    def test_markdown_to_blocks_strips_outer_whitespace(self):
        blocks = markdown_to_blocks("  \n\nFirst block\n\nSecond block\n\n  ")
        self.assertEqual(blocks[0], "First block")
        self.assertEqual(blocks[-1], "Second block")

class TestBlockToBlockType(unittest.TestCase):

    # --- HEADING ---

    def test_heading_h1(self):
        self.assertEqual(block_to_block_type("# Heading"), BlockType.HEADING)

    def test_heading_h3(self):
        self.assertEqual(block_to_block_type("### Heading"), BlockType.HEADING)

    def test_heading_h6(self):
        self.assertEqual(block_to_block_type("###### Heading"), BlockType.HEADING)

    def test_heading_missing_space(self):
        # No space after # — should fall through to paragraph
        self.assertEqual(block_to_block_type("#Heading"), BlockType.PARAGRAPH)

    def test_heading_too_many_hashes(self):
        # 7 hashes is not a valid heading
        self.assertEqual(block_to_block_type("####### Heading"), BlockType.PARAGRAPH)

    # --- CODE ---

    def test_code_single_line(self):
        self.assertEqual(block_to_block_type("```\nprint('hello')\n```"), BlockType.CODE)

    def test_code_multi_line(self):
        block = "```\ndef foo():\n    return 42\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_code_unclosed_backticks(self):
        self.assertEqual(block_to_block_type("```\nsome code"), BlockType.PARAGRAPH)

    # --- QUOTE ---

    def test_quote_single_line(self):
        self.assertEqual(block_to_block_type("> A quote"), BlockType.QUOTE)

    def test_quote_multi_line_all_prefixed(self):
        block = "> Line one\n> Line two\n> Line three"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_quote_mixed_lines_not_quote(self):
        # One line missing the > prefix — should NOT be a quote
        block = "> Line one\nLine two without prefix"
        self.assertNotEqual(block_to_block_type(block), BlockType.QUOTE)

    # --- UNORDERED LIST ---

    def test_unordered_list_single_item(self):
        self.assertEqual(block_to_block_type("- item one"), BlockType.UNORDERED_LIST)

    def test_unordered_list_multi_item(self):
        block = "- item one\n- item two\n- item three"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_unordered_list_mixed_lines_not_list(self):
        # One line missing the - prefix — should NOT be an unordered list
        block = "- item one\nitem two without prefix"
        self.assertNotEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_unordered_list_missing_space(self):
        # No space after - — should not match
        self.assertNotEqual(block_to_block_type("-item"), BlockType.UNORDERED_LIST)

    # --- ORDERED LIST ---

    def test_ordered_list_single_item(self):
        self.assertEqual(block_to_block_type("1. first item"), BlockType.ORDERED_LIST)

    def test_ordered_list_multi_item(self):
        block = "1. first\n2. second\n3. third"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_ordered_list_non_sequential(self):
        # Numbers must be sequential
        block = "1. first\n3. skipped two"
        self.assertNotEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_ordered_list_missing_period(self):
        self.assertNotEqual(block_to_block_type("1 no period"), BlockType.ORDERED_LIST)

    # --- PARAGRAPH ---

    def test_paragraph_plain_text(self):
        self.assertEqual(block_to_block_type("Just a plain paragraph."), BlockType.PARAGRAPH)

    def test_paragraph_multi_line(self):
        block = "First line of paragraph\nSecond line of paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_empty_block_is_paragraph(self):
        self.assertEqual(block_to_block_type(""), BlockType.PARAGRAPH)

if __name__ == "__main__":
    unittest.main()
