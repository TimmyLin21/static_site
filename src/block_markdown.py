from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown):
    blocks = []
    sections = markdown.split("\n\n")
    for section in sections:
        if section.strip() != "":
            blocks.append(section.strip())
    return blocks


def block_to_block_type(markdown):
    if markdown.startswith(("#", "##", "###", "####", "#####", "######")):
        return BlockType.HEADING
    if markdown.startswith((">", "> ")):
        return BlockType.QUOTE
    sections = markdown.split("\n")
    if all(section.startswith("- ") for section in sections):
        return BlockType.UNORDERED_LIST
    if all(sections[i].startswith(f"{i+1}. ") for i in range(len(sections))):
        return BlockType.ORDERED_LIST
    if len(sections) > 1 and sections[0].startswith("```") and sections[-1] == "```":
        return BlockType.CODE
    return BlockType.PARAGRAPH
