import os
from file import list_tree
from markdown import extract_title, markdown_to_html_node


def generate_pages_recursive(
    dir_path_content: str, template_path: str, dest_dir_path: str, base_path: str
):
    dir_files, _ = list_tree(dir_path_content, dir_path_content)

    for dir_file in dir_files:
        if not dir_file.endswith(".md"):
            continue

        src_file_path = os.path.join(dir_path_content, dir_file)
        dest_file_path = os.path.join(dest_dir_path, dir_file[:-3] + ".html")

        generate_page(src_file_path, template_path, dest_file_path, base_path)


def generate_page(from_path: str, template_path: str, dest_path: str, base_path: str):
    print(
        f"Generating page from '{from_path}' to '{dest_path}' using '{template_path}'"
    )

    with open(from_path, "r") as f:
        markdown = f.read()

    with open(template_path, "r") as f:
        template = f.read()

    content = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    finished_html = (
        template.replace("{{ Title }}", title)
        .replace("{{ Content }}", content)
        .replace('href="/', f'href="{base_path}')
        .replace('src="/', f'src="{base_path}')
    )

    dir, _ = os.path.split(dest_path)
    os.makedirs(dir, exist_ok=True)

    with open(dest_path, "w") as dest_file:
        _ = dest_file.write(finished_html)
