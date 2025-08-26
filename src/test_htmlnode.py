import unittest

from htmlnode import HTMLNode


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

if __name__ == "__main__":
    unittest.main()
