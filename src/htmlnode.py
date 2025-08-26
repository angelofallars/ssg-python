from dataclasses import dataclass
from typing import Literal, override


@dataclass(slots=True)
class HTMLNode:
    tag: "TagType | None" = None
    value: str | None = None
    children: "list[HTMLNode] | None" = None
    props: dict[str, str] | None = None

    def to_html(self) -> str:
        raise NotImplementedError

    def props_to_html(self) -> str:
        if self.props is None:
            return ""

        sorted_props = sorted(self.props.items())

        return "".join(f' {k}="{v}"' for k, v in sorted_props)

    @override
    def __repr__(self) -> str:
        fields = dict[str, str]()
        if self.tag is not None:
            fields["tag"] = f"'{self.tag}'"
        if self.value is not None:
            fields["value"] = f"'{self.value}'"
        if self.children is not None:
            fields["children"] = str(self.children)
        if self.props is not None:
            fields["props"] = str(self.props)

        fields_str = (f"{k}={v}" for k, v in fields.items())
        return f"{self.__class__.__name__}({', '.join(fields_str)})"


type TagType = Literal[
    "a",
    "abbr",
    "address",
    "area",
    "article",
    "aside",
    "audio",
    "b",
    "base",
    "bdi",
    "bdo",
    "blockquote",
    "body",
    "br",
    "button",
    "canvas",
    "caption",
    "cite",
    "code",
    "col",
    "colgroup",
    "command",
    "datalist",
    "dd",
    "del",
    "details",
    "dfn",
    "div",
    "dl",
    "dt",
    "em",
    "embed",
    "fieldset",
    "figcaption",
    "figure",
    "footer",
    "form",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "head",
    "header",
    "hgroup",
    "hr",
    "html",
    "i",
    "iframe",
    "img",
    "input",
    "ins",
    "kbd",
    "keygen",
    "label",
    "legend",
    "li",
    "link",
    "map",
    "mark",
    "menu",
    "meta",
    "meter",
    "nav",
    "noscript",
    "object",
    "ol",
    "optgroup",
    "option",
    "output",
    "p",
    "param",
    "pre",
    "progress",
    "q",
    "rp",
    "rt",
    "ruby",
    "s",
    "samp",
    "script",
    "section",
    "select",
    "small",
    "source",
    "span",
    "strong",
    "style",
    "sub",
    "summary",
    "sup",
    "table",
    "tbody",
    "td",
    "textarea",
    "tfoot",
    "th",
    "thead",
    "time",
    "title",
    "tr",
    "track",
    "u",
    "ul",
    "var",
    "video",
    "wbr",
]
