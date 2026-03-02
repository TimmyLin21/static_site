import re

from block_markdown import markdown_to_blocks, block_to_block_type, BlockType
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node, TextNode, TextType
from htmlnode import ParentNode


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for text_node in text_nodes:
        html_nodes.append(text_node_to_html_node(text_node))
    return html_nodes


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    div_children = []
    for block in blocks:
        block_type = block_to_block_type(block)

        match block_type:
            case BlockType.HEADING:
                sections = block.split(" ", 1)
                heading_num = len(sections[0])
                text = sections[1]
                children = text_to_children(text)
                heading = ParentNode(f"h{heading_num}", children)
                div_children.append(heading)
            case BlockType.CODE:
                text_nodes = TextNode(block[4:-3], TextType.TEXT)
                code = ParentNode("code", [text_node_to_html_node(text_nodes)])
                pre = ParentNode("pre", [code])
                div_children.append(pre)
            case BlockType.QUOTE:
                lines = block.split("\n")
                new_lines = []
                for line in lines:
                    if not line.startswith(">"):
                        raise ValueError("invalid quote block")
                    new_lines.append(line.lstrip(">").strip())
                content = " ".join(new_lines)
                children = text_to_children(content)
                quote_html = ParentNode("blockquote", children)
                div_children.append(quote_html)
            case BlockType.UNORDERED_LIST:
                items = block.split("\n")
                items_html = []
                for item in items:
                    sections = item.split(" ", 1)
                    text = sections[1]
                    children = text_to_children(text)
                    items_html.append(ParentNode("li", children))
                ul = ParentNode("ul", items_html)
                div_children.append(ul)
            case BlockType.ORDERED_LIST:
                items = block.split("\n")
                items_html = []
                for item in items:
                    sections = item.split(" ", 1)
                    text = sections[1]
                    children = text_to_children(text)
                    items_html.append(ParentNode("li", children))
                ol = ParentNode("ol", items_html)
                div_children.append(ol)
            case BlockType.PARAGRAPH:
                paragraphs = " ".join(block.split("\n"))
                children = text_to_children(paragraphs)
                p = ParentNode("p", children)
                div_children.append(p)

    div = ParentNode("div", div_children)
    return div


def extract_title(markdown):
    pattern = r"^# (.*)$"
    match = re.search(pattern, markdown, re.MULTILINE)
    if match is None:
        raise Exception("There is no h1 header")

    return match.group(1).strip()
