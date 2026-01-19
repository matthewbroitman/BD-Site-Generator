import unittest

from block_markdown import (
markdown_to_blocks
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

if __name__ == "__main__":
    unittest.main()