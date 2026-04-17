import os
import re
from converter import markdown_to_html_node

PUBLIC_DIR = "./public/"

def main():
    copy_files()
    generate_pages_recursive("./content", "./template.html", "./public")

def generate_page(from_path: str, template_path: str, dest_path: str):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    md_file = os.open(from_path, os.O_RDONLY)
    md_content = os.read(md_file, os.path.getsize(md_file)).decode()

    template_file = os.open(template_path, os.O_RDONLY)
    template_content = os.read(template_file, os.path.getsize(template_file)).decode()

    title = extract_title(md_content)
    html = markdown_to_html_node(md_content).to_html()

    final_html = template_content.replace("{{ Title }}", title).replace("{{ Content }}", html)
    final_html_path = os.path.join(os.path.split(dest_path)[0], "index.html")

    os.makedirs(os.path.dirname(final_html_path), exist_ok=True)
    html_file = os.open(final_html_path, os.O_CREAT | os.O_WRONLY | os.O_TRUNC, 0o644)
    os.write(html_file, final_html.encode())

def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path: str):
    if os.path.isfile(dir_path_content):
        generate_page(dir_path_content, template_path, dest_dir_path)
        return

    items = os.listdir(dir_path_content)
    for i in items:
        generate_pages_recursive(
            os.path.join(dir_path_content, i),
            template_path,
            os.path.join(dest_dir_path, i)
        )

def copy_files():
    if os.path.exists(PUBLIC_DIR): remove_dir(PUBLIC_DIR)
    copy_dir("./static/", PUBLIC_DIR)

def extract_title(markdown: str):
    blocks = markdown.split("\n")
    blocks = [block for block in blocks if block != ""]
    
    match = re.match(r"^# [\s\S]+", blocks[0])
    if match is None:
        raise Exception("No Header found")
    
    return match.group(0).lstrip("# ")

def remove_dir(path: str):
    if os.path.isfile(path):
        os.remove(path)
        return

    items = os.listdir(path)
    for i in items: remove_dir(os.path.join(path, i))

    os.rmdir(path)

def copy_dir(src: str, dest: str):
    if os.path.isfile(src):
        f = os.open(src, os.O_RDONLY)
        file_contents = os.read(f, os.path.getsize(src))
        
        fnew = os.open(dest, os.O_CREAT | os.O_WRONLY, 0o644)
        os.write(fnew, file_contents)
        return
    
    os.mkdir(dest)
    
    items = os.listdir(src)
    for i in items: copy_dir(os.path.join(src, i), os.path.join(dest, i))

if __name__ == "__main__":
    main()