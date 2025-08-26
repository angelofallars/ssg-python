import unittest

from htmlnode import HTMLNode, LeafNode


class TestTextNode(unittest.TestCase):
    def test_props_to_html(self):
        test_cases: list[tuple[HTMLNode, str]] = [
            (
                HTMLNode(
                    "a",
                    "Here comes the Lash!",
                    props={"href": "https://www.google.com", "target": "blank"},
                ),
                ' href="https://www.google.com" target="blank"',
            ),
            (
                HTMLNode(
                    "a",
                    "Deadlock is a good game",
                    props={"target": "blank", "href": "https://www.google.com"},
                ),
                ' href="https://www.google.com" target="blank"',
            ),
            (
                HTMLNode(
                    "th",
                    "Paige mains rise up",
                    props={"style": "margin-top: 0;", "class": "sidebar", "lang": "en"},
                ),
                ' class="sidebar" lang="en" style="margin-top: 0;"',
            ),
        ]

        for node, expected in test_cases:
            actual = node.props_to_html()
            self.assertEqual(actual, expected)

    def test_leaf_to_html_p(self):
        test_cases: list[tuple[HTMLNode, str]] = [
            (
                LeafNode(
                    "b",
                    "Hello, world!",
                ),
                 "<b>Hello, world!</b>",
            ),
            (
                LeafNode(
                    "a",
                    "A link!",
                    {"href": "https://www.google.com", "target":"blank"}
                ),
                '<a href="https://www.google.com" target="blank">A link!</a>',
            ),
            (
                LeafNode(
                    "code",
                    'print("hello world")',
                    {"style": "code-block"}
                ),
                '<code style="code-block">print("hello world")</code>',
            ),
        ]

        for node, expected in test_cases:
            actual = node.to_html()
            self.assertEqual(actual, expected)

if __name__ == "__main__":
    unittest.main()
