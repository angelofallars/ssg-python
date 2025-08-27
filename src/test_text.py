import unittest

from text import extract_markdown_images, extract_markdown_links


class TestText(unittest.TestCase):
    def test_extract_markdown_images(self):
        test_cases: list[tuple[str, list[tuple[str, str]]]] = [
            (
                "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
                [("image", "https://i.imgur.com/zjjcJKZ.png")],
            ),
            (
                "No alt text ![](https://www.boot.dev/img/bootdev-logo-full-small.webp)",
                [("", "https://www.boot.dev/img/bootdev-logo-full-small.webp")],
            ),
            (
                "Two images ![Python](https://i.imgur.com/zjjcJKZ.png) ![Boot.dev](https://www.boot.dev/img/bootdev-logo-full-small.webp)",
                [
                    ("Python", "https://i.imgur.com/zjjcJKZ.png"),
                    (
                        "Boot.dev",
                        "https://www.boot.dev/img/bootdev-logo-full-small.webp",
                    ),
                ],
            ),
        ]

        for input, expected in test_cases:
            actual = extract_markdown_images(input)
            self.assertEqual(actual, expected)

    def test_extract_markdown_links(self):
        test_cases: list[tuple[str, list[tuple[str, str]]]] = [
            (
                "This is text with a [link](https://i.imgur.com/zjjcJKZ.png)",
                [("link", "https://i.imgur.com/zjjcJKZ.png")],
            ),
            (
                "No alt text [](https://www.boot.dev/img/bootdev-logo-full-small.webp)",
                [("", "https://www.boot.dev/img/bootdev-logo-full-small.webp")],
            ),
            (
                "Two links [Python](https://i.imgur.com/zjjcJKZ.png) [Boot.dev](https://www.boot.dev/img/bootdev-logo-full-small.webp)",
                [
                    ("Python", "https://i.imgur.com/zjjcJKZ.png"),
                    (
                        "Boot.dev",
                        "https://www.boot.dev/img/bootdev-logo-full-small.webp",
                    ),
                ],
            ),
        ]

        for input, expected in test_cases:
            actual = extract_markdown_links(input)
            self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
