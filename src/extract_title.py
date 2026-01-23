from block_markdown import markdown_to_blocks,block_to_blocktype,BlockType

def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if block_to_blocktype(block) == BlockType.HEADING:
            if not block.startswith(("##","###","####","#####","######")) and block.startswith("#"):
                text = block.strip("#")
                return text.strip()
            pass
    raise Exception ("No H1 Header found.")
    
