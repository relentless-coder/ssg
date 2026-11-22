import os
import sys
from utils import cleanup_dir, traverse_dir_and_copy_content, create_dir
from process_markdown import generate_pages_recursive


def main(arg):
    basepath = arg[1] if arg[1] else "/"
    DEST_DIR = os.environ.get("dest", default="docs")
    SRC_DIR = os.environ.get("src", default="static")
    if not DEST_DIR or not SRC_DIR:
        raise ValueError("DEST_DIR and SRC_DIR are requried")
    try:
        cleanup_dir(DEST_DIR)
    except Exception:
        print("Cleanup failed")
        return
    create_dir(DEST_DIR)
    try:
        traverse_dir_and_copy_content(dest=DEST_DIR, src=SRC_DIR, curr_path=[])
    except Exception:
        print(f"Copy failed {Exception.__bases__}")
        return
    try:
        generate_pages_recursive(dir_path_content="content", template_path="template.html", dest_dir_path=DEST_DIR, base_path=basepath)
    except (ValueError, FileNotFoundError) as e:
        print(f"Error generating page {e}")
        return


if __name__ == "__main__":
    main(sys.argv)
