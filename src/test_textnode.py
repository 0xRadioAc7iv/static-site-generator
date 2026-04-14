import unittest
from textnode import TextNode, TextType
from main import text_node_to_html_node

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
    
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

if __name__ == "__main__":
    unittest.main()