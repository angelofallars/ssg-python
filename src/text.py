import re

# ![<alt text>](<URL>)
_image_re = re.compile(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)")

# [<alt text>](<URL>)
_link_re = re.compile(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)")

def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    images: list[tuple[str, str]] = _image_re.findall(text)
    return images

def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    links: list[tuple[str, str]] = _link_re.findall(text)
    return links
