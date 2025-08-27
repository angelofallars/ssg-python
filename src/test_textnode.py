from typing import Literal
import unittest

from textnode import (
    TextNode,
    markdown_to_blocks,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_node_to_html_node,
    text_to_textnodes,
)


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
                [
                    TextNode("Meow **meow** meow", "Plain"),
                    TextNode("Purr ** purr ** purr", "Plain"),
                ],
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
                [
                    TextNode("_italic_ shenanigans", "Plain"),
                    TextNode("this is also _ita_lic", "Plain"),
                ],
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

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            "Plain",
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", "Plain"),
                TextNode("image", "Image", "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", "Plain"),
                TextNode("second image", "Image", "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_images_2(self):
        new_nodes = split_nodes_image(
            [
                TextNode(
                    "![image](https://i.imgur.com/zjjcJKZ.png) ![second image](https://i.imgur.com/3elNhQu.png) ![second image](https://i.imgur.com/3elNhQu.png)",
                    "Plain",
                ),
                TextNode(
                    "![image](https://i.imgur.com/zjjcJKZ.png) ![second image](https://i.imgur.com/3elNhQu.png) ![second image](https://i.imgur.com/3elNhQu.png)",
                    "Plain",
                ),
                TextNode(
                    "![image](https://i.imgur.com/zjjcJKZ.png) ![second image](https://i.imgur.com/3elNhQu.png) ![second image](https://i.imgur.com/3elNhQu.png)",
                    "Plain",
                ),
            ]
        )
        self.assertListEqual(
            [
                TextNode("image", "Image", "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" ", "Plain"),
                TextNode("second image", "Image", "https://i.imgur.com/3elNhQu.png"),
                TextNode(" ", "Plain"),
                TextNode("second image", "Image", "https://i.imgur.com/3elNhQu.png"),
                TextNode("image", "Image", "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" ", "Plain"),
                TextNode("second image", "Image", "https://i.imgur.com/3elNhQu.png"),
                TextNode(" ", "Plain"),
                TextNode("second image", "Image", "https://i.imgur.com/3elNhQu.png"),
                TextNode("image", "Image", "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" ", "Plain"),
                TextNode("second image", "Image", "https://i.imgur.com/3elNhQu.png"),
                TextNode(" ", "Plain"),
                TextNode("second image", "Image", "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            "Plain",
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", "Plain"),
                TextNode("link", "Link", "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", "Plain"),
                TextNode("second link", "Link", "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_links_2(self):
        new_nodes = split_nodes_link(
            [
                TextNode(
                    "[link](https://i.imgur.com/zjjcJKZ.png) [second link](https://i.imgur.com/3elNhQu.png) [second link](https://i.imgur.com/3elNhQu.png)",
                    "Plain",
                ),
                TextNode(
                    "[link](https://i.imgur.com/zjjcJKZ.png) [second link](https://i.imgur.com/3elNhQu.png) [second link](https://i.imgur.com/3elNhQu.png)",
                    "Plain",
                ),
                TextNode(
                    "[link](https://i.imgur.com/zjjcJKZ.png) [second link](https://i.imgur.com/3elNhQu.png) [second link](https://i.imgur.com/3elNhQu.png)",
                    "Plain",
                ),
            ]
        )
        self.assertListEqual(
            [
                TextNode("link", "Link", "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" ", "Plain"),
                TextNode("second link", "Link", "https://i.imgur.com/3elNhQu.png"),
                TextNode(" ", "Plain"),
                TextNode("second link", "Link", "https://i.imgur.com/3elNhQu.png"),
                TextNode("link", "Link", "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" ", "Plain"),
                TextNode("second link", "Link", "https://i.imgur.com/3elNhQu.png"),
                TextNode(" ", "Plain"),
                TextNode("second link", "Link", "https://i.imgur.com/3elNhQu.png"),
                TextNode("link", "Link", "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" ", "Plain"),
                TextNode("second link", "Link", "https://i.imgur.com/3elNhQu.png"),
                TextNode(" ", "Plain"),
                TextNode("second link", "Link", "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_text_to_textnodes(self):
        test_cases: list[tuple[str, list[TextNode]]] = [
            (
                "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)",
                [
                    TextNode("This is ", "Plain"),
                    TextNode("text", "Bold"),
                    TextNode(" with an ", "Plain"),
                    TextNode("italic", "Italic"),
                    TextNode(" word and a ", "Plain"),
                    TextNode("code block", "Code"),
                    TextNode(" and an ", "Plain"),
                    TextNode(
                        "obi wan image", "Image", "https://i.imgur.com/fJRm4Vk.jpeg"
                    ),
                    TextNode(" and a ", "Plain"),
                    TextNode("link", "Link", "https://boot.dev"),
                ],
            ),
            (
                "Uses standard `net/http` types. Has basic [integration](#templ-integration) with [templ](https://templ.guide/) components.",
                [
                    TextNode("Uses standard ", "Plain"),
                    TextNode("net/http", "Code"),
                    TextNode(" types. Has basic ", "Plain"),
                    TextNode("integration", "Link", "#templ-integration"),
                    TextNode(" with ", "Plain"),
                    TextNode("templ", "Link", "https://templ.guide/"),
                    TextNode(" components.", "Plain"),
                ],
            ),
            (
                "If you have an element that is polling a URL and you want it to stop, use the `htmx.StatusStopPolling` 286 status code in a response to cancel the polling. [HTMX documentation reference](https://htmx.org/docs/#polling)",
                [
                    TextNode(
                        "If you have an element that is polling a URL and you want it to stop, use the ",
                        "Plain",
                    ),
                    TextNode("htmx.StatusStopPolling", "Code"),
                    TextNode(
                        " 286 status code in a response to cancel the polling. ",
                        "Plain",
                    ),
                    TextNode(
                        "HTMX documentation reference",
                        "Link",
                        "https://htmx.org/docs/#polling",
                    ),
                ],
            ),
            (
                "**S**imple **W**ayland **H**ot**K**ey **D**aemon",
                [
                    TextNode("S", "Bold"),
                    TextNode("imple ", "Plain"),
                    TextNode("W", "Bold"),
                    TextNode("ayland ", "Plain"),
                    TextNode("H", "Bold"),
                    TextNode("ot", "Plain"),
                    TextNode("K", "Bold"),
                    TextNode("ey ", "Plain"),
                    TextNode("D", "Bold"),
                    TextNode("aemon", "Plain"),
                ],
            ),
        ]

        for input, expected in test_cases:
            actual = text_to_textnodes(input)
            self.assertEqual(actual, expected)

    def test_markdown_to_blocks(self):
        test_cases: list[tuple[str, list[str]]] = [
            (
                """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
""",
                [
                    "This is **bolded** paragraph",
                    "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                    "- This is a list\n- with items",
                ],
            ),
            (
                """
A picture of you reminds me
How the years have gone so lonely
And why do you have to leave me
Without saying that you love me?

I'm saying "I love you" again
Are you listening?
Open your eyes once again
Look at me crying

If only you could hear me shout your name
If only you could feel my love again
The stars in the sky will never be the same
If only you were here
""",
                [
                    "A picture of you reminds me\nHow the years have gone so lonely\nAnd why do you have to leave me\nWithout saying that you love me?",
                    "I'm saying \"I love you\" again\nAre you listening?\nOpen your eyes once again\nLook at me crying",
                    "If only you could hear me shout your name\nIf only you could feel my love again\nThe stars in the sky will never be the same\nIf only you were here",
                ],
            ),
            (
                """
# Hypo


Hypo is a hyper-fast runtime for [HTML, the programming language](https://html-lang.org).




Run HTML, the programming language code outside of the browser.

## Installation
""",
                [
                    "# Hypo",
                    "Hypo is a hyper-fast runtime for [HTML, the programming language](https://html-lang.org).",
                    "Run HTML, the programming language code outside of the browser.",
                    "## Installation",
                ],
            ),
        ]

        for input, expected in test_cases:
            actual = markdown_to_blocks(input)
            self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
