from collections.abc import Sequence
from dataclasses import dataclass
from typing import Literal, override

from htmlnode import HTMLNode, LeafNode


type TextType = Literal["Plain", "Bold", "Italic", "Code", "Link", "Image"]


@dataclass(slots=True)
class TextNode:
    text: str
    text_type: TextType
    url: str | None = None

    @override
    def __eq__(self, value: object, /) -> bool:
        if not isinstance(value, TextNode):
            return False

        return (
            self.text == value.text
            and self.text_type == value.text_type
            and self.url == value.url
        )

    @override
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}('{self.text}', '{self.text_type}', '{self.url}')"


def text_node_to_html_node(text_node: TextNode) -> HTMLNode:
    match text_node.text_type:
        case "Plain":
            return LeafNode(tag=None, value=text_node.text)
        case "Bold":
            return LeafNode(tag="b", value=text_node.text)
        case "Italic":
            return LeafNode(tag="i", value=text_node.text)
        case "Code":
            return LeafNode(tag="code", value=text_node.text)
        case "Link":
            if text_node.url is None:
                msg = f"{text_node} has no url"
                raise ValueError(msg)

            return LeafNode(
                tag="a", value=text_node.text, props={"href": text_node.url}
            )
        case "Image":
            if text_node.url is None:
                msg = f"{text_node} has no url"
                raise ValueError(msg)

            return LeafNode(
                tag="img",
                value="",
                props={"href": text_node.url, "alt": text_node.text},
            )


def split_nodes_delimiter(
    old_nodes: Sequence[TextNode], text_type: Literal["Bold", "Italic", "Code"]
) -> list[TextNode]:
    delimiter: str
    match text_type:
        case "Bold":
            delimiter = "**"
        case "Italic":
            delimiter = "_"
        case "Code":
            delimiter = "`"

    new_nodes = list[TextNode]()
    for node in old_nodes:
        if node.text_type != "Plain":
            new_nodes.append(node)
            continue

        last = ""
        text_so_far = ""
        start_delimiter = False
        for char in node.text:
            is_delimiter = (last + char).endswith(delimiter)
            if is_delimiter:
                # Hacky hack hack for bold
                if len(delimiter) == 2:
                    text_so_far = text_so_far[:-1]

                if not start_delimiter:
                    start_delimiter = True
                    if len(text_so_far) != 0:
                        new_nodes.append(TextNode(text_so_far, "Plain"))
                        text_so_far = ""
                else:
                    start_delimiter = False
                    new_nodes.append(TextNode(text_so_far, text_type))
                    text_so_far = ""
            else:
                text_so_far += char

            last = char

        # Not raising an error on not finding a closing delimiter

        if len(text_so_far) != 0:
            new_nodes.append(TextNode(text_so_far, "Plain"))

    return new_nodes
