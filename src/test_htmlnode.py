import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


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
                    {"href": "https://www.google.com", "target": "blank"},
                ),
                '<a href="https://www.google.com" target="blank">A link!</a>',
            ),
            (
                LeafNode("code", 'print("hello world")', {"style": "code-block"}),
                '<code style="code-block">print("hello world")</code>',
            ),
        ]

        for node, expected in test_cases:
            actual = node.to_html()
            self.assertEqual(actual, expected)

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

    def test_to_html_with_many_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode(
            "span", [grandchild_node, grandchild_node, grandchild_node]
        )
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b><b>grandchild</b><b>grandchild</b></span></div>",
        )

    def test_to_html_with_many_grandchildren_2(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode(
            "span", [grandchild_node, grandchild_node, grandchild_node, grandchild_node]
        )
        parent_node = ParentNode("div", [child_node], {"hello": "world"})

        self.assertEqual(
            parent_node.to_html(),
            '<div hello="world"><span><b>grandchild</b><b>grandchild</b><b>grandchild</b><b>grandchild</b></span></div>',
        )


if __name__ == "__main__":
    unittest.main()
