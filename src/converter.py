from textnode import TextNode, TextType
from htmlnode import ParentNode, LeafNode
from block import *
from inline import text_to_text_nodes
import re

def text_node_to_html_node(text_node: TextNode):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text.strip("```"))
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception("Invalid Type of TextNode")

def markdown_to_html_node(markdown: str):
    blocks = markdown_to_blocks(markdown)
    nodes = []

    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type == BlockType.CODE:
            text_node = TextNode(block, TextType.CODE)
            code_node = text_node_to_html_node(text_node)
            html_node = ParentNode("pre", [code_node])
            nodes.append(html_node)
        if block_type == BlockType.HEADING:
            sub_nodes = []

            pounds = block.count("#")
            tag = f"h{pounds}"

            text_nodes = text_to_text_nodes(block.strip("#").strip(" "))

            for node in text_nodes: 
                sub_nodes.append(text_node_to_html_node(node))
 
            nodes.append(ParentNode(tag, sub_nodes))
        if block_type == BlockType.QUOTE:
            sub_nodes = []
            text_nodes = text_to_text_nodes(block)

            quote_lines = [node.text.split("\n") for node in text_nodes]

            for line in quote_lines:
                for sub_line in line:
                    sub_nodes.append(text_node_to_html_node(TextNode(sub_line.strip("> "), TextType.TEXT)))
 
            nodes.append(ParentNode("blockquote", sub_nodes))
        if block_type == BlockType.UNORDERED_LIST:
            sub_nodes = []
            sub_blocks = block.split("\n")
            sub_blocks = [sb.strip("-").strip(" ") for sb in sub_blocks]

            for sb in sub_blocks:
                sub_nodes.append(LeafNode("li", sb))

            nodes.append(ParentNode("ul", sub_nodes))
        if block_type == BlockType.ORDERED_LIST:
            sub_nodes = []

            dot = block.find(".")
            sub_blocks = block.split("\n")

            for sb in sub_blocks:
                text = re.sub(r"^\d+\. ", "", sb)
                sub_nodes.append(LeafNode("li", text))

            nodes.append(
                ParentNode(
                    "ol",
                    sub_nodes, 
                    {"type": "1", "start": block[0:dot]}
                )
            )
        if block_type == BlockType.PARAGRAPH:
            sub_nodes = []
            text_nodes = text_to_text_nodes(block)

            for node in text_nodes: 
                sub_nodes.append(text_node_to_html_node(node))
 
            nodes.append(ParentNode("p", sub_nodes))

    return ParentNode("div", nodes)