from textnode import TextNode, TextType
from htmlnode import LeafNode
import re

md_link_regex_pattern = r"(?<!!)\[(.*?)\]\((.*?)\)"
md_image_regex_pattern = r"!\[(.*?)\]\((.*?)\)"

def main():
    pass

def text_to_text_nodes(text: str):
    node = TextNode(text, TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_links(new_nodes)
    return new_nodes

def text_node_to_html_node(text_node: TextNode):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, { "href": text_node.url })
        case TextType.IMAGE:
            return LeafNode("img", "", { "src": text_node.url, "alt": text_node.text })
        case _:
            raise Exception("Invalid Type of TextNode")

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType):
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        split_nodes = []
        sections = old_node.text.split(delimiter)

        if len(sections) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")
        
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
            
        new_nodes.extend(split_nodes)
    
    return new_nodes

def split_nodes_image(old_nodes: list[TextNode]):
    new_nodes = []

    for old_node in old_nodes:
        images = extract_markdown_images(old_node.text)

        if len(images) == 0:
            new_nodes.append(old_node)
            continue

        nodes_new = []
        remaining = old_node.text
        for i in images:
            sections = remaining.split(f"![{i[0]}]({i[1]})", 1)
            remaining = sections[1]
            nodes_new.append(TextNode(sections[0], TextType.TEXT))
            nodes_new.append(TextNode(i[0], TextType.IMAGE, i[1]))

        if remaining:
            nodes_new.append(TextNode(remaining, TextType.TEXT))

        new_nodes.extend(nodes_new)

    return new_nodes

def split_nodes_links(old_nodes):
    new_nodes = []

    for old_node in old_nodes:
        links = extract_markdown_links(old_node.text)

        if len(links) == 0:
            new_nodes.append(old_node)
            continue

        nodes_new = []
        remaining = old_node.text
        for i in links:
            sections = remaining.split(f"[{i[0]}]({i[1]})", 1)
            remaining = sections[1]
            nodes_new.append(TextNode(sections[0], TextType.TEXT))
            nodes_new.append(TextNode(i[0], TextType.LINK, i[1]))

        if remaining:
            nodes_new.append(TextNode(remaining, TextType.TEXT))

        new_nodes.extend(nodes_new)

    return new_nodes

def extract_markdown_images(text: str):
    matches = re.findall(md_image_regex_pattern, text)
    return matches

def extract_markdown_links(text: str):
    matches = re.findall(md_link_regex_pattern, text)
    return matches

if __name__ == "__main__":
    main()