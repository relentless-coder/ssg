import os
from utils import cleanup_dir, traverse_dir_and_copy_content, create_dir


def main():
    DEST_DIR = os.environ.get("dest", default="public")
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


if __name__ == "__main__":
    main()
