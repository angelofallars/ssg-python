import unittest

from textnode import TextNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "Bold")
        node2 = TextNode("This is a text node", "Bold")
        self.assertEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("This is a text node", "Image", "public/cat.png")
        node2 = TextNode("This is a text node", "Image", "public/cat.png")
        self.assertEqual(node, node2)

    def test_not_eq_url(self):
        node = TextNode("This is a text node", "Image", "public/cat2.png")
        node2 = TextNode("This is a text node", "Image", "public/cat.png")
        self.assertNotEqual(node, node2)

    def test_not_eq_text(self):
        node = TextNode("This is a text node", "Plain")
        node2 = TextNode("This is a text node!", "Plain")
        self.assertNotEqual(node, node2)

    def test_not_eq_type(self):
        node = TextNode("This is a text node", "Italic")
        node2 = TextNode("This is a text node", "Code")
        self.assertNotEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a text node", "Italic")
        node2 = TextNode("This is also a text node", "Code")
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()
