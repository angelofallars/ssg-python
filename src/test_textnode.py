from typing import Literal
import unittest

from textnode import TextNode, split_nodes_delimiter, text_node_to_html_node


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

    def test_text(self):
        node = TextNode("This is a text node", "Plain")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.children, None)
        self.assertEqual(html_node.props, None)

    def test_bold(self):
        node = TextNode("This is a bold node", "Bold")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")
        self.assertEqual(html_node.children, None)
        self.assertEqual(html_node.props, None)

    def test_italic(self):
        node = TextNode("This is an italic node", "Italic")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic node")
        self.assertEqual(html_node.children, None)
        self.assertEqual(html_node.props, None)

    def test_code(self):
        node = TextNode("This is a code node", "Code")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code node")
        self.assertEqual(html_node.children, None)
        self.assertEqual(html_node.props, None)

    def test_link(self):
        node = TextNode("This is a link node", "Link", "https://www.bing.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link node")
        self.assertEqual(html_node.children, None)
        self.assertEqual(html_node.props, {"href": "https://www.bing.com"})

    def test_image(self):
        node = TextNode("This is an image node", "Image", "public/cat.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.children, None)
        self.assertEqual(
            html_node.props, {"href": "public/cat.png", "alt": "This is an image node"}
        )

    def test_split_nodes_delimiter(self):
        test_cases: list[
            tuple[list[TextNode], Literal["Bold", "Italic", "Code"], list[TextNode]]
        ] = [
            (
                [TextNode("This is text with a `code block` word", "Plain")],
                "Code",
                [
                    TextNode("This is text with a ", "Plain"),
                    TextNode("code block", "Code"),
                    TextNode(" word", "Plain"),
                ],
            ),
            (
                [TextNode("Meow **meow** meow", "Plain"), TextNode("Purr ** purr ** purr", "Plain")],
                "Bold",
                [
                    TextNode("Meow ", "Plain"),
                    TextNode("meow", "Bold"),
                    TextNode(" meow", "Plain"),
                    TextNode("Purr ", "Plain"),
                    TextNode(" purr ", "Bold"),
                    TextNode(" purr", "Plain"),
                ],
            ),
            (
                [TextNode("_italic_ shenanigans", "Plain"), TextNode("this is also _ita_lic", "Plain")],
                "Italic",
                [
                    TextNode("italic", "Italic"),
                    TextNode(" shenanigans", "Plain"),
                    TextNode("this is also ", "Plain"),
                    TextNode("ita", "Italic"),
                    TextNode("lic", "Plain"),
                ],
            ),
        ]

        for input, text_type, expected in test_cases:
            actual = split_nodes_delimiter(input, text_type)
            self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
