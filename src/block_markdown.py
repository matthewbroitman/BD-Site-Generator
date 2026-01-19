def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    clean_blocks =[]
    for block in blocks:
        clean_blocks.append(block.strip())
    return clean_blocks