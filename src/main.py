import os
import shutil
import sys

from file import copy_dir
from page import generate_pages_recursive


SRC_PATH = "static/"
CONTENT_PATH = "content/"
TEMPLATE_PATH = "template.html"
DEST_PATH = "docs/"

def main():
    basepath = "/"
    if len(sys.argv) != 1:
        basepath = sys.argv[1]

    # Delete all contents of dest
    if os.path.exists(DEST_PATH):
        shutil.rmtree(DEST_PATH)

    copy_dir(SRC_PATH, DEST_PATH)

    generate_pages_recursive(CONTENT_PATH, TEMPLATE_PATH, DEST_PATH, basepath)
    

if __name__ == "__main__":
    main()
