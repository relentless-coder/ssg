import shutil
import os
from pathlib import Path


def cleanup_dir(dest: str):
    if not os.path.exists(dest) or not os.path.isdir(dest):
        return
    shutil.rmtree(dest)
    return


def create_dir(dest: str):
    print(f"creating directory {dest}")
    os.mkdir(dest)
    return


def copy_file(src: str, dest: str):
    if not os.path.exists(src) or not os.path.isfile(src):
        print(f"skipping copy_file\n invalid parameter\n src: {src}")
        return
    if not os.path.exists(dest) or not os.path.isdir(dest):
        print(f"skipping copy_file\n invalid parameter\n src: {dest}")
        return
    shutil.copy(src, dest)
    print(f"copied src_path:{src} to dest_path:{dest}\n")
    return


def traverse_dir_and_copy_content(src: str, dest: str, curr_path: list[str]):
    src_path = Path(os.path.join(src, "/".join(curr_path)))
    if not src_path.exists() or not src_path.is_dir():
        raise Exception("src, and dest are required")
    for item in src_path.iterdir():
        if item.is_dir() and not item.is_symlink():
            curr_path.append(item.name)
            create_dir(dest=os.path.join(dest, "/".join(curr_path)))
            traverse_dir_and_copy_content(src, dest, curr_path)
            curr_path.pop()
        else:
            copy_file(os.path.join(src, "/".join(curr_path), item.name), os.path.join(dest,"/".join(curr_path)))
    return

def read_file(file_path: str) -> str:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"Invalid file_path: {file_path}")
    with open(file_path) as f:
        s = f.read()
    return s
