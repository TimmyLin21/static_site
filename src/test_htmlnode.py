import unittest

from htmlnode import HTMLNode

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

if __name__ == "__main__":
    unittest.main()