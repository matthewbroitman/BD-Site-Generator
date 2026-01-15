import unittest

from textnode import TextNode, TextType,text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_false(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("This is a text node", TextType.ITALIC, "https://www.boot.dev")
        node2 = TextNode("This is a text node", TextType.ITALIC, "https://www.boot.dev")
        self.assertEqual(node, node2)

    def test_eq_url_node(self):
        node = TextNode("This is a text node", TextType.ITALIC, None)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.TEXT, "https://www.boot.dev")
        self.assertEqual(
            "TextNode(This is a text node, text, https://www.boot.dev)", repr(node)
        )

class TestText_to_HTML(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold text node")

    def test_italics(self):
        node = TextNode("This is an italicized text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italicized text node")

    def test_code(self):
        node = TextNode("This is a code text node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code text node")

    def test_link(self):
        node = TextNode("This is a hyperlinked text node", TextType.LINK,"https://www.google.com")
        html_node = text_node_to_html_node(node)
        prop = html_node.props_to_html()
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a hyperlinked text node")
        self.assertEqual(prop,' href="https://www.google.com"')

    def test_image(self):
        node = TextNode("This is an image text node", TextType.IMAGE,"https://www.google.com")
        html_node = text_node_to_html_node(node)
        props = html_node.props_to_html()
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, None)
        self.assertEqual(props,' src="https://www.google.com" alt="This is an image text node"')

if __name__ == "__main__":
    unittest.main()