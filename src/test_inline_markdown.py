import unittest
from inline_markdown import (
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    extract_markdown_links,
    extract_markdown_images,
    text_to_textnodes
)

from textnode import TextNode, TextType

class TestInlineMarkdown(unittest.TestCase):
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded word", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

        
    def test_extract_markdown_images_one_image(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_mul_image(self):
        matches = extract_markdown_images(
            "This is text with a two ![image](https://i.imgur.com/zjjcJKZ.png) & ![image](https://i.imgur.com/cO51xkv.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png"),("image", "https://i.imgur.com/cO51xkv.png")], matches)

    def test_extract_markdown_images_no_image(self):
        matches = extract_markdown_images(
            "This is text with no images"
        )
        self.assertListEqual([], matches)

    def test_extract_markdown_images_on_link(self):
        matches = extract_markdown_images(
            "This is text with a link [to boot dev](https://www.boot.dev)"
        )
        self.assertListEqual([], matches)


    def test_extract_markdown_links_one_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev")], matches)

    def test_extract_markdown_links_mul_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)

    def test_extract_markdown_links_no_links(self):
        matches = extract_markdown_links(
            "This is text with no link"
        )
        self.assertListEqual([], matches)

    def test_extract_markdown_links_on_image(self):
        matches = extract_markdown_links(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([], matches)


    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.COM/IMAGE.PNG)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://www.example.COM/IMAGE.PNG"),
            ],
            new_nodes,
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev) with text that follows",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("another link", TextType.LINK, "https://blog.boot.dev"),
                TextNode(" with text that follows", TextType.TEXT),
            ],
            new_nodes,
        )
    

    def test_text_to_textnodes_just_text(self):
        text = "This is a plain set of text."
        test_nodes = text_to_textnodes(text)
        ex_nodes = [TextNode(text,TextType.TEXT)
        ]
        self.assertListEqual(test_nodes,ex_nodes)

    def test_text_to_textnodes_delims_seq(self):
        text = "This is a set of text with **bold**, _italic_, and `code` in it."
        test_nodes = text_to_textnodes(text)
        ex_nodes = [TextNode("This is a set of text with ",TextType.TEXT),
                    TextNode("bold",TextType.BOLD),
                    TextNode(", ",TextType.TEXT),
                    TextNode("italic",TextType.ITALIC),
                    TextNode(", and ",TextType.TEXT),
                    TextNode("code",TextType.CODE),
                    TextNode(" in it.",TextType.TEXT)
        ]
        self.assertListEqual(test_nodes,ex_nodes)

    def test_text_to_textnodes_image_and_link(self):
        text = "This is a set of text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev) in it."
        test_nodes = text_to_textnodes(text)
        ex_nodes = [TextNode("This is a set of text with an ",TextType.TEXT),
                    TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                    TextNode(" and a ",TextType.TEXT),
                    TextNode("link", TextType.LINK, "https://boot.dev"),
                    TextNode(" in it.",TextType.TEXT)
        ]
        self.assertListEqual(test_nodes,ex_nodes)

    def test_text_to_textnodes_delims_image_and_link(self):
        text = "This is a set of text with **bold**, _italic_, and `code` in it, as well as an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev) in it."
        test_nodes = text_to_textnodes(text)
        ex_nodes = [TextNode("This is a set of text with ",TextType.TEXT),
                    TextNode("bold",TextType.BOLD),
                    TextNode(", ",TextType.TEXT),
                    TextNode("italic",TextType.ITALIC),
                    TextNode(", and ",TextType.TEXT),
                    TextNode("code",TextType.CODE),
                    TextNode(" in it, as well as an ",TextType.TEXT),
                    TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                    TextNode(" and a ",TextType.TEXT),
                    TextNode("link", TextType.LINK, "https://boot.dev"),
                    TextNode(" in it.",TextType.TEXT)
        ]
        self.assertListEqual(test_nodes,ex_nodes)

    def test_text_to_textnodes_mul_delims(self):
        text = "This is a set of text with **bold**, **more bold**, _italic_, _more italic_, `code`, and `more code` in it."
        test_nodes = text_to_textnodes(text)
        ex_nodes = [TextNode("This is a set of text with ",TextType.TEXT),
                    TextNode("bold",TextType.BOLD),
                    TextNode(", ",TextType.TEXT),
                    TextNode("more bold",TextType.BOLD),
                    TextNode(", ",TextType.TEXT),
                    TextNode("italic",TextType.ITALIC),
                    TextNode(", ",TextType.TEXT),
                    TextNode("more italic",TextType.ITALIC),
                    TextNode(", ",TextType.TEXT),
                    TextNode("code",TextType.CODE),
                    TextNode(", and ",TextType.TEXT),
                    TextNode("more code",TextType.CODE),
                    TextNode(" in it.",TextType.TEXT)
        ]
        self.assertListEqual(test_nodes,ex_nodes)

    def test_text_to_textnodes_edge_delims(self):
        text = "**This** is a set of text that is _important._"
        test_nodes = text_to_textnodes(text)
        ex_nodes = [TextNode("This",TextType.BOLD),
                    TextNode(" is a set of text that is ",TextType.TEXT),
                    TextNode("important.",TextType.ITALIC),
        ]
        self.assertListEqual(test_nodes,ex_nodes)

    def test_text_to_textnodes_images_links_no_spaces(self):
        text = "Hot Tests![image](https://i.imgur.com/zjjcJKZ.png)click now[link](https://boot.dev)you want to"
        test_nodes = text_to_textnodes(text)
        ex_nodes = [TextNode("Hot Tests",TextType.TEXT),
                    TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                    TextNode("click now",TextType.TEXT),
                    TextNode("link", TextType.LINK, "https://boot.dev"),
                    TextNode("you want to",TextType.TEXT)
        ]
        self.assertListEqual(test_nodes,ex_nodes)

    def test_text_to_textnodes_images_links_broken(self):
        text = "Hot Tests![deadimage] (broken link)click now[deadlink] (dead)you want to"
        test_nodes = text_to_textnodes(text)
        ex_nodes = [TextNode("Hot Tests![deadimage] (broken link)click now[deadlink] (dead)you want to",TextType.TEXT),
        ]
        self.assertListEqual(test_nodes,ex_nodes)

    def test_text_to_textnodes_delims_code_protect(self):
        text = "This is a set of text with `code that has **stars** and _underscores_.`"
        test_nodes = text_to_textnodes(text)
        ex_nodes = [TextNode("This is a set of text with ",TextType.TEXT),
                    TextNode("code that has **stars** and _underscores_.",TextType.CODE),
        ]
        self.assertListEqual(test_nodes,ex_nodes)

if __name__ == "__main__":
    unittest.main()