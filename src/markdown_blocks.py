def markdown_to_blocks(markdown: str) -> list[str]:
    lines = markdown.split("\n\n")
    lines = map(lambda line: line.strip(), lines)
    lines = filter(lambda line: line != "", lines)
    lines = list(lines)

    return lines
