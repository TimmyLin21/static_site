import unittest

from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    def test_repr(self):
        node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
        self.assertEqual(repr(node), "TextNode(This is some anchor text, link, https://www.boot.dev)")
    def test_url_none(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node.url, None)

if __name__ == "__main__":
    unittest.main()