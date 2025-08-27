from typing import Literal, override


class HTMLNode:
    def __init__(
        self,
        tag: "TagType | None" = None,
        value: str | None = None,
        children: "list[HTMLNode] | None" = None,
        props: dict[str, str] | None = None,
    ) -> None:
        self.tag: "TagType | None" = tag
        self.value: str | None = value
        self.children: "list[HTMLNode] | None" = children
        self.props: dict[str, str] | None = props

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


class LeafNode(HTMLNode):
    def __init__(
        self,
        tag: "TagType | None",
        value: str,
        props: dict[str, str] | None = None,
    ) -> None:
        super().__init__(tag, value, None, props)

    @override
    def to_html(self) -> str:
        if self.value is None:
            msg = f"Leaf node '{self}' has no value"
            raise ValueError(msg)

        start_tag = ""
        end_tag = ""
        if self.tag is not None:
            start_tag = f"<{self.tag}{self.props_to_html()}>"
            end_tag = f"</{self.tag}>"

        return f"{start_tag}{self.value}{end_tag}"


class ParentNode(HTMLNode):
    def __init__(
        self,
        tag: "TagType",
        children: list[HTMLNode],
        props: dict[str, str] | None = None,
    ) -> None:
        super().__init__(tag, None, children, props)

    @override
    def to_html(self) -> str:
        if self.tag is None:
            msg = f"Parent node '{self}' has no tag"
            raise ValueError(msg)

        if self.children is None:
            msg = f"Parent node '{self}' has no children"
            raise ValueError(msg)


        children = "".join(child.to_html() for child in self.children)

        return f"<{self.tag}{self.props_to_html()}>{children}</{self.tag}>"


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
