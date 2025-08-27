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
    if len(lines) == 1:
        first_line = lines[0]
        first_words = first_line.split(" ")

        is_header = True
        char_count = 0
        for char in first_words[0]:
            char_count += 1
            if char != "#" or char_count > 6:
                is_header = False
                break

        if char_count == 0:
            is_header = False

        if is_header:
            return "Heading"

    # Code
    if block.startswith("```") and block.endswith("```"):
        return "Code"

    # Quote
    is_quote = all(map(lambda line: line.startswith("> "), lines))
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
