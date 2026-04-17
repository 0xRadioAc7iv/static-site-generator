import unittest
from htmlnode import HTMLNode, ParentNode, LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_not_empty_when_set(self):
        node = HTMLNode("p", "this is some text", props={"id": "main", "lang": "en"})
        self.assertEqual(node.props_to_html(), " id=\"main\" lang=\"en\"")
    
    def test_props_to_html_empty_when_not_set(self):
        node = HTMLNode("p", "this is some text")
        self.assertEqual(node.props_to_html(), "")
    
    def test_children_is_not_empty_when_set(self):
        node = HTMLNode("p", "this is some text", [HTMLNode("a"), HTMLNode("p")])
        self.assertEqual(len(node.children), 2)

    def test_children_is_empty_when_not_set(self):
        node = HTMLNode("p", "this is some text", props={"id": "main", "lang": "en"})
        self.assertListEqual(node.children, [])
    
    def test_leaf_to_html_raises_when_value_none(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), "<a href=\"https://www.google.com\">Click me!</a>")
    
    def test_leaf_to_html_b(self):
        node = LeafNode("b", "BOLD TEXT")
        self.assertEqual(node.to_html(), "<b>BOLD TEXT</b>")

    def test_pre_code_block(self):
        node = ParentNode("pre", [LeafNode("code", "print('hello')")])
        self.assertEqual(node.to_html(), "<pre><code>print('hello')</code></pre>")

    def test_pre_code_block_multiline(self):
        node = ParentNode("pre", [LeafNode("code", "line one\nline two")])
        self.assertEqual(node.to_html(), "<pre><code>line one\nline two</code></pre>")

    def test_nested_parent_uses_child_props_not_outer(self):
        # inner <code> has its own class; outer <pre> props must NOT bleed into <code>
        inner = ParentNode("code", [LeafNode(None, "x")], {"class": "python"})
        outer = ParentNode("pre", [inner], {"class": "highlight"})
        self.assertEqual(
            outer.to_html(),
            '<pre class="highlight"><code class="python">x</code></pre>',
        )

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

class TestParentNode(unittest.TestCase):
    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    
    def test_parent_with_multiple_children(self):
        child1 = LeafNode("span", "one")
        child2 = LeafNode("span", "two")
        parent = ParentNode("div", [child1, child2])
        self.assertEqual(
            parent.to_html(),
            "<div><span>one</span><span>two</span></div>"
        )

    def test_parent_with_props(self):
        child = LeafNode("span", "content")
        parent = ParentNode("div", [child], {"class": "container"})
        self.assertEqual(
            parent.to_html(),
            "<div class=\"container\"><span>content</span></div>"
        )

    def test_parent_nested_multiple_levels(self):
        leaf = LeafNode("b", "deep")
        child = ParentNode("span", [leaf])
        parent = ParentNode("div", [child])
        self.assertEqual(
            parent.to_html(),
            "<div><span><b>deep</b></span></div>"
        )

    def test_parent_with_text_leaf_and_tagless_leaf(self):
        child1 = LeafNode("span", "text")
        child2 = LeafNode(None, "plain text")
        parent = ParentNode("div", [child1, child2])
        self.assertEqual(
            parent.to_html(),
            "<div><span>text</span>plain text</div>"
        )

    def test_parent_raises_error_when_tag_missing(self):
        child = LeafNode("span", "text")
        parent = ParentNode("", [child])
        with self.assertRaises(ValueError):
            parent.to_html()

    def test_parent_with_empty_children(self):
        parent = ParentNode("div", [])
        self.assertEqual(parent.to_html(), "<div></div>")

    def test_parent_with_deeply_nested_structure(self):
        node = ParentNode("div", [
            ParentNode("section", [
                ParentNode("article", [
                    LeafNode("p", "hello")
                ])
            ])
        ])
        self.assertEqual(
            node.to_html(),
            "<div><section><article><p>hello</p></article></section></div>"
        )

    def test_parent_with_multiple_nested_siblings(self):
        node = ParentNode("div", [
            ParentNode("span", [LeafNode("b", "bold")]),
            ParentNode("span", [LeafNode("i", "italic")])
        ])
        self.assertEqual(
            node.to_html(),
            "<div><span><b>bold</b></span><span><i>italic</i></span></div>"
        )

    def test_parent_child_without_value_raises(self):
        class DummyNode(HTMLNode):
            def to_html(self):
                return ""

        bad_child = DummyNode(tag="span")
        parent = ParentNode("div", [bad_child])
        with self.assertRaises(ValueError):
            parent.to_html()

if __name__ == "__main__":
    unittest.main()