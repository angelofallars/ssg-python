import os
import shutil


def copy_dir(src: str, dest: str):
    if not os.path.exists(src):
        msg = f"Path does not exist: {src}"
        raise Exception(msg)

    files, directories = _list_tree(src, src)

    # Copy all files and subdirs, nested files/subdirs
    os.mkdir(dest)
    for directory in directories:
        new_directory = os.path.join(dest, directory)
        os.mkdir(new_directory)

    for file in files:
        old_file = os.path.join(src, file)
        new_file = os.path.join(dest, file)
        _ = shutil.copy(old_file, new_file)


def _list_tree(src: str, prefix: str) -> tuple[list[str], list[str]]:
    files: list[str] = []
    directories: list[str] = []

    for content in sorted(os.listdir(src)):
        full_path = os.path.join(src, content)
        rel_path = os.path.relpath(full_path, prefix)

        if os.path.isfile(full_path):
            files.append(rel_path)
        else:
            directories.append(rel_path)
            child_files, child_directories = _list_tree(full_path, prefix)
            files.extend(child_files)
            files.extend(child_directories)

    return files, directories
