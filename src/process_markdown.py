from pathlib import Path
import os
import re
from htmlnode import ParentNode
from blocknode import block_to_html_node
from utils import read_file, create_dir


def markdown_to_blocks(text: str) -> list[str]:
    res = []
    blocks = text.split("\n\n")
    for block in blocks:
        block = block.strip()
        if block != "":
            res.append(re.sub(r"(\n\s+)", "\n", block))
    return res


def markdown_to_html_node(markdown: str) -> ParentNode:
    html_nodes = [block_to_html_node(block) for block in markdown_to_blocks(markdown)]
    return ParentNode("div", html_nodes)

def extract_title(markdown: str) -> str:
    blocks = markdown_to_blocks(markdown)
    if not blocks:
        raise ValueError("No markdown")
    mtch = re.match(r"^# ", blocks[0])
    if not mtch:
        raise ValueError('No h1 heading in markdown')
    return blocks[0][2:]

def generate_page(from_path: str, template_path: str, dest_path: str):
    md = ""
    html = ""
    try:
        md = read_file(from_path)
    except FileNotFoundError:
        print(f"from_path {from_path} file not found")
        return
    try:
        html = read_file(template_path)
    except FileNotFoundError:
        print(f"template_path {template_path} file not found")
        return

    title = ""
    try:
        title = extract_title(md)
    except ValueError as e:
        print(f"Error extracting title {e}\n")
        return
    content = markdown_to_html_node(md)
    html = html.replace("{{ Title }}", title)
    html = html.replace("{{ Content }}", content.to_html())
    from_file_name = Path(from_path)
    with open(os.path.join(dest_path, from_file_name.name.split(".")[0] + ".html"), "w") as f:
        f.write(html)
    print(f"Generate html page at {dest_path}")

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    src_path = Path(dir_path_content)
    if not src_path.exists():
        raise ValueError(f"Invalid source path {src_path}")
    for item in src_path.iterdir():
        if item.is_dir() and not item.is_symlink():
            create_dir(os.path.join(dest_dir_path, item.name))
            generate_pages_recursive(os.path.join(dir_path_content, item.name), template_path, os.path.join(dest_dir_path, item.name))
        elif item.is_file():
            generate_page(os.path.join(dir_path_content, item.name), template_path, dest_path=dest_dir_path)
    return


