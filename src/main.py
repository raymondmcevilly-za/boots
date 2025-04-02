import os
import shutil
from block_markdown import (
    markdown_to_html_node,
    extract_title,
)

dir_path_static = "./static"
dir_path_public = "./public"
dir_path_content = "./content"
templat_path = "./template.html"


def main():

    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    print("Copying static files to public directory...")
    copy(dir_path_static, dir_path_public)

    generate_pages_recursive(dir_path_content, templat_path, dir_path_public)

    # generate_page(
    #     os.path.join(dir_path_content, "index.md"),
    #     templat_path,
    #     os.path.join(dir_path_public, "index.html"),
    # )


def copy(src, dst):
    if not os.path.exists(dst):
        os.mkdir(dst)

    for path in os.listdir(src):
        src_path = os.path.join(src, path)
        dst_path = os.path.join(dst, path)

        print(f" * {src_path} -> {dst_path}")
        if os.path.isfile(src_path):
            shutil.copy(src_path, dst)
        else:
            copy(src_path, dst_path)

# /content/


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for path in os.listdir(dir_path_content):
        src_path = os.path.join(dir_path_content, path)
        dst_path = os.path.join(dest_dir_path, path.replace(".md", ".html"))

        if os.path.isfile(src_path):
            # print(f"{src_path} {templat_path} -> {dst_path}")
            generate_page(src_path, templat_path, dst_path)
        else:
            generate_pages_recursive(src_path, templat_path, dst_path)


def generate_page(from_path, template_path, dest_path):
    print(f" * {from_path} {template_path} -> {dest_path}")

    with open(from_path, "r") as file:
        markdown = file.read()

    with open(template_path, "r") as file:
        template = file.read()

    content = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", content)

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)

    with open(dest_path, "w") as file:
        file.write(template)


main()
