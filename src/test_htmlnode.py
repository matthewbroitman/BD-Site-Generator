import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_mulprops(self):
        node = HTMLNode(props={"href": "https://example.com", "target": "_blank"})
        result =  ' href="https://example.com" target="_blank"'
        self.assertEqual(node.props_to_html(), result)

    def test_props_to_html_noprops(self):
        node = HTMLNode()
        result = ""
        self.assertEqual(node.props_to_html(),result)

    def test_to_html(self):
        node = HTMLNode()
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_def_value_check(self):
        node = HTMLNode()
        ex_text = "HTMLNode(None, None, None, None)"
        self.assertEqual(repr(node),ex_text)

    def test_nondef_value_check(self):
        node = HTMLNode(tag="p",value="some text",props={"href": "https://example.com", "target": "_blank"})
        ex_text = "HTMLNode(None, None, None, None)"
        self.assertNotEqual(repr(node),ex_text)

if __name__ == "__main__":
    unittest.main()