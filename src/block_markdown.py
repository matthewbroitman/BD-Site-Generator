from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    clean_blocks =[]
    for block in blocks:
        clean_blocks.append(block.strip())
    return clean_blocks

def block_to_blocktype(block):
    if block.startswith("#"):
        return BlockType.HEADING
    if block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE
    lines = block.split("\n")
    if all(line.startswith("> ") for line in lines):
        return BlockType.QUOTE
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST
    count = 1
    for line in lines:
        if line.startswith(f"{count}. "):
            count += 1
        else:
            return BlockType.PARAGRAPH
    return BlockType.ORDERED_LIST