import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        a = HTMLNode(
            "a",
            "Google",
            props={
            "href": "https://www.google.com",
            "target": "_blank",
        })
        self.assertEqual(
            a.props_to_html(),
            ' href="https://www.google.com" target="_blank"'
        )
    def test_repr(self):
        div = HTMLNode("div","This is div",props={
            "class": "flex"
        })
        self.assertEqual(repr(div), "tag=div value=This is div children=None props={'class': 'flex'}")
    def test_tag_None(self):
        node = HTMLNode()
        self.assertEqual(node.tag, None)

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_repr(self):
        div = LeafNode("div","This is div",props={
            "class": "flex"
        })
        self.assertEqual(repr(div), "tag=div value=This is div props={'class': 'flex'}")

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_multichildren(self):
        child_node = LeafNode("span", "child")
        child_node2 = LeafNode("span", "child2")
        parent_node = ParentNode("div", [child_node, child_node2])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span>child</span><span>child2</span></div>",
        )
if __name__ == "__main__":
    unittest.main()