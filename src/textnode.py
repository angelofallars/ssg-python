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
