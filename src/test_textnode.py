import unittest
from textnode import TextNode, TextType
from inline import *
from converter import *

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_noteq_text(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node 2", TextType.BOLD)
        self.assertNotEqual(node, node2)
    
    def test_noteq_text_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_noteq_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "url")
        node2 = TextNode("This is a text node", TextType.BOLD, "url2")
        self.assertNotEqual(node, node2)
   
    def test_url_is_none_when_not_set(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertIsNone(node.url)
   
    def test_url_is_not_none_when_set(self):
        node = TextNode("This is a text node", TextType.BOLD, "this is a url")
        self.assertIsNotNone(node.url)

    def test_repr(self):
        node = TextNode("hello", TextType.BOLD, "https://example.com")
        self.assertEqual(repr(node), "TextNode(hello, **Bold text**, https://example.com)")
    
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_split_nodes_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)
    
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://google.com/)"
        )
        self.assertListEqual([("link", "https://google.com/")], matches)
    
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    
    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://google.com/) and another [link two](https://boot.dev/)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_links([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://google.com/"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "link two", TextType.LINK, "https://boot.dev/"
                ),
            ],
            new_nodes,
        )

    # text_node_to_html_node
    def test_bold(self):
        node = TextNode("bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "bold text")

    def test_italic(self):
        node = TextNode("italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "italic text")

    def test_code(self):
        node = TextNode("code text", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "code text")

    def test_link(self):
        node = TextNode("click here", TextType.LINK, "https://example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "click here")
        self.assertEqual(html_node.props["href"], "https://example.com")

    def test_image(self):
        node = TextNode("alt text", TextType.IMAGE, "https://example.com/img.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props["src"], "https://example.com/img.png")
        self.assertEqual(html_node.props["alt"], "alt text")

    def test_invalid_type_raises(self):
        node = TextNode("text", None)
        self.assertRaises(Exception, text_node_to_html_node, node)

    # split_nodes_delimiter
    def test_split_nodes_delimiter_bold(self):
        node = TextNode("This is **bold** text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[1].text, "bold")

    def test_split_nodes_delimiter_italic(self):
        node = TextNode("This is _italic_ text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[1].text_type, TextType.ITALIC)
        self.assertEqual(new_nodes[1].text, "italic")

    def test_split_nodes_delimiter_passthrough_non_text(self):
        node = TextNode("already bold", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0], node)

    def test_split_nodes_delimiter_unclosed_raises(self):
        node = TextNode("unclosed `code", TextType.TEXT)
        self.assertRaises(ValueError, split_nodes_delimiter, [node], "`", TextType.CODE)

    # extract_markdown_images / links
    def test_extract_markdown_images_multiple(self):
        matches = extract_markdown_images(
            "![one](https://a.com/1.png) and ![two](https://b.com/2.png)"
        )
        self.assertEqual(len(matches), 2)
        self.assertEqual(matches[0], ("one", "https://a.com/1.png"))
        self.assertEqual(matches[1], ("two", "https://b.com/2.png"))

    def test_extract_markdown_images_none(self):
        matches = extract_markdown_images("no images here")
        self.assertListEqual([], matches)

    def test_extract_markdown_links_ignores_images(self):
        matches = extract_markdown_links("![img](https://a.com/1.png)")
        self.assertListEqual([], matches)

    def test_extract_markdown_links_multiple(self):
        matches = extract_markdown_links(
            "[a](https://a.com) and [b](https://b.com)"
        )
        self.assertEqual(len(matches), 2)

    # split_nodes_image / links — edge cases
    def test_split_images_trailing_text(self):
        node = TextNode(
            "![img](https://a.com/1.png) trailing text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertEqual(new_nodes[-1], TextNode(" trailing text", TextType.TEXT))

    def test_split_images_no_images_passthrough(self):
        node = TextNode("plain text", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    def test_split_links_trailing_text(self):
        node = TextNode(
            "[link](https://a.com) trailing text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_links([node])
        self.assertEqual(new_nodes[-1], TextNode(" trailing text", TextType.TEXT))

    def test_split_links_no_links_passthrough(self):
        node = TextNode("plain text", TextType.TEXT)
        new_nodes = split_nodes_links([node])
        self.assertListEqual([node], new_nodes)

    def test_text_to_text_nodes(self):
        nodes = text_to_text_nodes(
            "Hello **bold** and _italic_ and `code` and [link](https://a.com) and ![img](https://b.com/i.png)"
        )
        types = [n.text_type for n in nodes]
        self.assertIn(TextType.BOLD, types)
        self.assertIn(TextType.ITALIC, types)
        self.assertIn(TextType.CODE, types)
        self.assertIn(TextType.LINK, types)
        self.assertIn(TextType.IMAGE, types)

    def test_text_to_text_nodes_plain(self):
        nodes = text_to_text_nodes("just plain text")
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
        self.assertEqual(nodes[0].text, "just plain text")

if __name__ == "__main__":
    unittest.main()