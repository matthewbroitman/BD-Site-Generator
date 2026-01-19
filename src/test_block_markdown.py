import unittest

from block_markdown import(
BlockType,
markdown_to_blocks,
block_to_blocktype
)

class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks_BD(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_all_headers(self):
        md = """
#This is a header

#This is another header

#This is a header with **bold text** in it

#This is a header with `code` in it

#This is a header with _italics_ in it
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "#This is a header",
                "#This is another header",
                "#This is a header with **bold text** in it",
                "#This is a header with `code` in it",
                "#This is a header with _italics_ in it",
            ],
        )

    def test_markdown_to_blocks_all_para(self):
        md = """
This is a paragraph

This is yet another paragraph
but with two lines

And another with ** bolded text**

Or perhaps one with `code`

And one last one with _italics_
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is a paragraph",
                "This is yet another paragraph\nbut with two lines",
                "And another with ** bolded text**",
                "Or perhaps one with `code`",
                "And one last one with _italics_",
            ],
        )

    def test_markdown_to_blocks_all_lists(self):
        md = """
-a list
-of some things

-and another
-with some **bold** things
-and even _italic_ things

-and yet one more with only one `code` thing
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "-a list\n-of some things",
                "-and another\n-with some **bold** things\n-and even _italic_ things",
                "-and yet one more with only one `code` thing",
            ],
        )

class TestBlockToBlocktype(unittest.TestCase):
    def test_paragraph_block(self):
        block = """This is a paragraph of text."""
        result = block_to_blocktype(block)
        self.assertEqual(result,BlockType.PARAGRAPH)

    def test_header_block(self):
        block = """###This is a piece of header text."""
        result = block_to_blocktype(block)
        self.assertEqual(result,BlockType.HEADING)

    def test_code_block(self):
        block = """```\nThis is a piece of code,\nspanning two lines.```"""
        result = block_to_blocktype(block)
        self.assertEqual(result,BlockType.CODE)

    def test_quote_block(self):
        block = """> This is a quote\n> of multiples lines"""
        result = block_to_blocktype(block)
        self.assertEqual(result,BlockType.QUOTE)

    def test_unordered_list_block(self):
        block = """- This is a list\n- of multiples items"""
        result = block_to_blocktype(block)
        self.assertEqual(result,BlockType.UNORDERED_LIST)

    def test_ordered_list_block(self):
        block = """1. This is a list\n2. of multiples items"""
        result = block_to_blocktype(block)
        self.assertEqual(result,BlockType.ORDERED_LIST)

    def test_code_block_no_newline(self):
        block = """```This is a piece of code,\nspanning two lines.```"""
        result = block_to_blocktype(block)
        self.assertEqual(result,BlockType.PARAGRAPH)
        
    def test_quote_block_bad_line(self):
        block = """> This is a quote\nof multiples lines"""
        result = block_to_blocktype(block)
        self.assertEqual(result,BlockType.PARAGRAPH)

    def test_unord_list_block_missing_space(self):
        block = """-This is a list\n-without spaces"""
        result = block_to_blocktype(block)
        self.assertEqual(result,BlockType.PARAGRAPH)

    def test_ord_list_block_misnumber(self):
        block = """1. This is\n4. a poorly ordered\n3. list"""
        result = block_to_blocktype(block)
        self.assertEqual(result,BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()