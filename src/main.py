import shutil
import os
from markdown_to_html import markdown_to_html_node, extract_title
import sys


def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    template_content = ""
    markdown_content = ""
    with open(template_path, "r") as f:
        template_content = f.read()
    with open(from_path, "r") as f:
        markdown_content = f.read()
    div_node = markdown_to_html_node(markdown_content)
    html_string = div_node.to_html()
    title = extract_title(markdown_content)
    template_content = template_content.replace("{{ Title }}", title)
    template_content = template_content.replace("{{ Content }}", html_string)
    template_content = template_content.replace('href="/', 'href=f"{basepath}')
    template_content = template_content.replace('src="/', 'src=f"{basepath}')
    dirname = os.path.dirname(dest_path)
    os.makedirs(dirname, exist_ok=True)

    dest_path = dest_path.replace("md", "html")
    with open(dest_path, "w") as f:
        f.write(template_content)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    content_items = os.listdir(dir_path_content)
    for content_item in content_items:
        content_path = os.path.join(dir_path_content, content_item)
        dest_path = os.path.join(dest_dir_path, content_item)
        if os.path.isfile(content_path):
            generate_page(content_path, template_path, dest_path, basepath)
        else:
            os.mkdir(dest_path)
            generate_pages_recursive(content_path, template_path, dest_path, basepath)


def copy_to(soucre, dest, basepath):
    items = os.listdir(soucre)
    for item in items:
        source_path = os.path.join(soucre, item)
        dest_path = os.path.join(dest, item)
        if os.path.isfile(source_path):
            shutil.copy(source_path, dest_path)
            print(f"Successfully created {item}")
        else:
            os.mkdir(dest_path)
            print(f"Successfully created {item}")
            copy_to(source_path, dest_path, basepath)
            generate_pages_recursive("content", "template.html", "docs", basepath)


def main():
    basepath = sys.argv[1] or "/"
    SOURCE_DIR = "static"
    DES_DIR = "docs"
    try:
        if os.path.exists(DES_DIR):
            shutil.rmtree(DES_DIR)
            print(f"Successfully deleted {DES_DIR}")
        os.mkdir(DES_DIR)
        print(f"Successfully created {DES_DIR}")

        copy_to(SOURCE_DIR, DES_DIR, basepath)

    except FileNotFoundError:
        print("The directory does not exist.")
    except PermissionError:
        print("You do not have permission to delete this folder.")
    except OSError as e:
        print(f"Error: {e.strerror}")


if __name__ == "__main__":
    main()
