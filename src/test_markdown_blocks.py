import unittest

from markdown_blocks import markdown_to_blocks


class TestTextNode(unittest.TestCase):
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
