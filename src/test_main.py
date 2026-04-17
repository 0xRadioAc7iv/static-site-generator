import unittest
from main import extract_title


class TestExtractTitle(unittest.TestCase):

    def test_simple_title(self):
        self.assertEqual(extract_title("# Hello"), "Hello")

    def test_title_with_multiple_words(self):
        self.assertEqual(extract_title("# My Great Title"), "My Great Title")

    def test_title_with_content_below(self):
        md = "# My Title\n\nSome paragraph text below."
        self.assertEqual(extract_title(md), "My Title")

    def test_no_heading_raises(self):
        with self.assertRaises(Exception):
            extract_title("just a paragraph")

    def test_h2_not_valid_title(self):
        with self.assertRaises(Exception):
            extract_title("## Not a title")

    def test_h1_not_on_first_line_raises(self):
        md = "Some paragraph\n\n# Title buried below"
        with self.assertRaises(Exception):
            extract_title(md)

    def test_empty_markdown_raises(self):
        with self.assertRaises(Exception):
            extract_title("")


if __name__ == "__main__":
    unittest.main()
