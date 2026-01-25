import os
from block_markdown import markdown_to_html_node
from extract_title import extract_title
from htmlnode import HTMLNode

def generate_page(from_path,template_path,dest_path):
    print (f"Reticulating Splines: {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r", encoding="utf-8") as f:
        from_string = f.read()
    with open(template_path, "r", encoding="utf-8") as f:
        template_string = f.read()
    node = markdown_to_html_node(from_string)
    HTMLString = node.to_html()
    title = extract_title(from_string)
    template_string = template_string.replace("{{ Title }}", title)
    template_string = template_string.replace("{{ Content }}",HTMLString)
    dirpath = os.path.dirname(dest_path)
    if dirpath and not os.path.exists(dirpath):
        os.makedirs(dirpath, exist_ok=True)
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(template_string)
    
def generate_page_recursively(dir_path_content,template_path,dest_dir_path):
    items = os.listdir(dir_path_content)
    for item in items:
        item_path = os.path.join(dir_path_content,item)
        dest_item_path = os.path.join(dest_dir_path,item.replace(".md",".html"))
        if os.path.isfile(item_path) and item_path.endswith(".md"):
            generate_page(item_path,template_path,dest_item_path)
        if os.path.isdir(item_path):
            generate_page_recursively(item_path,template_path,dest_item_path)
    