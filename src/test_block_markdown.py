import unittest

from block_markdown import(
 markdown_to_html_node,
    markdown_to_blocks,
    block_to_blocktype,
    BlockType,
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
        block = """```\nThis is a piece of code,\nspanning two lines.\n```"""
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

    def test_paragraph(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_lists(self):
        md = """
- This is a list
- with items
- and _more_ items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )

    def test_code(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

if __name__ == "__main__":
    unittest.main()