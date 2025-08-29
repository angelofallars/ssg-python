import os
from markdown import extract_title, markdown_to_html_node


def generate_page(from_path: str, template_path: str, dest_path: str):
    print(
        f"Generating page from '{from_path}' to '{dest_path}' using '{template_path}'"
    )

    with open(from_path, "r") as f:
        markdown = f.read()

    with open(template_path, "r") as f:
        template = f.read()

    content = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    finished_html = template.replace("{{ Title }}", title).replace(
        "{{ Content }}", content
    )

    dir, _ = os.path.split(dest_path)
    os.makedirs(dir, exist_ok=True)

    with open(dest_path, "w") as dest_file:
        _ = dest_file.write(finished_html)
