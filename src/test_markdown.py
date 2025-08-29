from typing import Literal
import unittest

from markdown import extract_title, markdown_to_html_node


class TestMarkdown(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_long_text(self):
        md = """
Write [triggers](#triggers) for client-side events effectively without dealing with JSON serialization. With this approach, **event-driven** applications are easier to develop.

Use [Swap Strategy](#swap-strategy) methods to fine-tune `hx-swap` behavior.

Uses standard `net/http` types.
Has basic [integration](#templ-integration) with [templ](https://templ.guide/) components.
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            """<div><p>Write <a href="#triggers">triggers</a> for client-side events effectively without dealing with JSON serialization. With this approach, <b>event-driven</b> applications are easier to develop.</p><p>Use <a href="#swap-strategy">Swap Strategy</a> methods to fine-tune <code>hx-swap</code> behavior.</p><p>Uses standard <code>net/http</code> types. Has basic <a href="#templ-integration">integration</a> with <a href="https://templ.guide/">templ</a> components.</p></div>""",
        )

    def test_headers_simple(self):
        md = """
# H1

## H2

### H3
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.maxDiff = None
        self.assertEqual(html, "<div><h1>H1</h1><h2>H2</h2><h3>H3</h3></div>")

    def test_headers(self):
        md = """
## Additional resources

- [HTMX - HTTP Header Reference](https://htmx.org/reference/#headers)

### Contributing

Pull requests are welcome!

#### License

[MIT](./LICENSE)
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.maxDiff = None
        self.assertEqual(
            html,
            '<div><h2>Additional resources</h2><ul><li><a href="https://htmx.org/reference/#headers">HTMX - HTTP Header Reference</a></li></ul><h3>Contributing</h3><p>Pull requests are welcome!</p><h4>License</h4><p><a href="./LICENSE">MIT</a></p></div>',
        )

    def test_quote(self):
        md = """
> One
> Two
> Three
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><blockquote>One Two Three</blockquote></div>")

    def test_quote_with_child_nodes(self):
        md = """
> **One**
> _Two_
> Three `Three`
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote><b>One</b> <i>Two</i> Three <code>Three</code></blockquote></div>",
        )

    def test_ordered_list(self):
        md = """
1. One
2. Two
3. Three
4. Four
5. Five
6. Six
7. Seven
8. Eight
9. Nine
10. Ten
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>One</li><li>Two</li><li>Three</li><li>Four</li><li>Five</li><li>Six</li><li>Seven</li><li>Eight</li><li>Nine</li><li>Ten</li></ol></div>",
        )

    def test_extract_title(self):
        test_cases: list[tuple[str, str | None]] = [
            ("# Hello", "Hello"),
            ("## H2\n# H1", "H1"),
            ("## H2\n#       Lots of whitespace    ", "Lots of whitespace"),
            ("# ", ""),
            ("## No H1", None),
            ("", None),
            ("### H3\n#### H4", None),
        ]

        for markdown, expected in test_cases:
            should_raise_exception = expected is None

            try:
                actual = extract_title(markdown)
            except Exception as e:
                if not should_raise_exception:
                    e.add_note("Unexpected exception")
                    raise e
            else:
                if should_raise_exception:
                    msg = f"Exception expected with input: '{markdown}'"
                    raise AssertionError(msg)

                self.assertEqual(actual, expected)



if __name__ == "__main__":
    unittest.main()
