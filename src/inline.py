from textnode import TextNode, TextType
import re

md_link_regex_pattern = r"(?<!!)\[(.*?)\]\((.*?)\)"
md_image_regex_pattern = r"!\[(.*?)\]\((.*?)\)"

def extract_markdown_images(text: str):
    return re.findall(md_image_regex_pattern, text)

def extract_markdown_links(text: str):
    return re.findall(md_link_regex_pattern, text)

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType):
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        sections = old_node.text.split(delimiter)

        if len(sections) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")

        for i, section in enumerate(sections):
            if section == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(section, TextType.TEXT))
            else:
                new_nodes.append(TextNode(section, text_type))

    return new_nodes

def split_nodes_image(old_nodes: list[TextNode]):
    new_nodes = []

    for old_node in old_nodes:
        images = extract_markdown_images(old_node.text)

        if len(images) == 0:
            new_nodes.append(old_node)
            continue

        remaining = old_node.text
        for alt, url in images:
            sections = remaining.split(f"![{alt}]({url})", 1)
            remaining = sections[1]
            new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(alt, TextType.IMAGE, url))

        if remaining:
            new_nodes.append(TextNode(remaining, TextType.TEXT))

    return new_nodes

def split_nodes_links(old_nodes: list[TextNode]):
    new_nodes = []

    for old_node in old_nodes:
        links = extract_markdown_links(old_node.text)

        if len(links) == 0:
            new_nodes.append(old_node)
            continue

        remaining = old_node.text
        for anchor, url in links:
            sections = remaining.split(f"[{anchor}]({url})", 1)
            remaining = sections[1]
            new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(anchor, TextType.LINK, url))

        if remaining:
            new_nodes.append(TextNode(remaining, TextType.TEXT))

    return new_nodes

def text_to_text_nodes(text: str) -> list[TextNode]:
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_links(nodes)
    return nodes
