from dataclasses import dataclass
from typing import Literal, override


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
        return (
            f"{self.__class__.__name__}('{self.text}', '{self.text_type}', '{self.url}')"
        )
