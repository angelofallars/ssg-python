from typing import Literal


def markdown_to_blocks(markdown: str) -> list[str]:
    lines = markdown.split("\n\n")
    lines = map(lambda line: line.strip(), lines)
    lines = filter(lambda line: line != "", lines)
    lines = list(lines)

    return lines


type BlockType = Literal[
    "Paragraph", "Heading", "Code", "Quote", "UnorderedList", "OrderedList"
]


def block_to_block_type(block: str) -> BlockType:
    lines = block.split("\n")

    # Heading
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return "Heading"

    # Code
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return "Code"

    # Quote
    is_quote = True
    for line in lines:
        words = line.split(" ")
        if len(words) == 0 or words[0] != ">":
            is_quote = False
            break

    if is_quote:
        return "Quote"

    # Unordered list
    is_unordered_list = all(map(lambda line: line.startswith("- "), lines))
    if is_unordered_list:
        return "UnorderedList"

    # Ordered list
    is_ordered_list = True
    for i, line in enumerate(lines):
        number = i + 1
        if not line.startswith(f"{number}. "):
            is_ordered_list = False
            break

    if is_ordered_list:
        return "OrderedList"

    # Paragraph
    return "Paragraph"
