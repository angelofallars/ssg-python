import typing
from htmlnode import HTMLNode, LeafNode, ParentNode, TagType
from markdown_blocks import block_to_block_type, markdown_to_blocks
from textnode import TextNode, text_node_to_html_node, text_to_textnodes

def markdown_to_html_node(markdown: str) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)

    top_children = list[HTMLNode]()

    for block in blocks:
        block_type = block_to_block_type(block)

        node: HTMLNode
        match block_type:
            case "Paragraph":
                block = block.replace("\n", " ")
                children = text_to_children(block)
                node = ParentNode("p", children)
            case "Heading":
                words = block.split(" ")
                header_level = len(words[0])
                children = text_to_children(" ".join(words[1:]))
                node = ParentNode(typing.cast(TagType, f"h{header_level}"), children)
            case "Code":
                block = block[3:-3]
                block = block.lstrip("\n")

                node = ParentNode("pre", [LeafNode("code", block)]) 
            case "Quote":
                block = " ".join(map(lambda line: line[2:], block.split("\n")))
                children = text_to_children(block)
                node = ParentNode("blockquote", children)
            case "UnorderedList":
                children = list[HTMLNode]()
                for line in block.split("\n"):
                    text_nodes = list(map(text_node_to_html_node, text_to_textnodes(line[2:])))
                    children.append(ParentNode("li", text_nodes))

                node = ParentNode("ul", children)
            case "OrderedList":
                children = list[HTMLNode]()
                for line in block.split("\n"):
                    line_without_num = "".join(line.split(". ")[1:])
                    text_nodes = list(map(text_node_to_html_node, text_to_textnodes(line_without_num)))
                    children.append(ParentNode("li", text_nodes))

                node = ParentNode("ol", children)

        top_children.append(node)

    parent = ParentNode("div", top_children)
    return parent


def text_to_children(text: str) -> list[HTMLNode]:
    text_nodes = text_to_textnodes(text)

    html_nodes = list[HTMLNode]()
    for text_node in text_nodes:
        html_nodes.append(text_node_to_html_node(text_node))

    return html_nodes


def extract_title(markdown: str) -> str:
    lines = markdown.split("\n")

    for line in lines:
        if line.startswith("# "):
            return line.lstrip("# ").strip()

    msg = "No 'h1' header found"
    raise Exception(msg)
