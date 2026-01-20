import unittest

from htmlnode import HTMLNode,LeafNode,ParentNode


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

class TestLeafNode(unittest.TestCase):
    def test_to_HTML_TEXT(self):
        node = LeafNode(None,"This is Raw Text")
        ex_text = "This is Raw Text"
        self.assertEqual(node.to_html(),ex_text)

    def test_to_HTML_BOLD(self):
        node = LeafNode("b","This is Bold Text.")
        ex_text = "<b>This is Bold Text.</b>"
        self.assertEqual(node.to_html(),ex_text)

    def test_to_HTML_ITALIC(self):
        node = LeafNode("i","This is Italic Text.")
        ex_text = "<i>This is Italic Text.</i>"
        self.assertEqual(node.to_html(),ex_text)

    def test_to_HTML_PARA(self):
        node = LeafNode("p","This is a Paragraph.")
        ex_text = "<p>This is a Paragraph.</p>"
        self.assertEqual(node.to_html(),ex_text)

    def test_to_HTML_LINK(self):
        node = LeafNode("a","This is a Link",{"href":"https://example.com"})
        ex_text = '<a href="https://example.com"> This is a Link</a>'
        self.assertEqual(node.to_html(),ex_text)

    def test_to_HTML_IMAGE(self):
        node = LeafNode("img","This is an Image",{"src":"https://example.com"})
        ex_text = '<img src="https://example.com" alt="This is an Image" />'
        self.assertEqual(node.to_html(),ex_text)
    
    def test_to_HTML_NOVAL(self):
        node = LeafNode("p",None)
        with self.assertRaises(ValueError):
            node.to_html()

class TestLeafNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    
    def test_to_html_notag(self):
        child_node = LeafNode("b","Bold Test Text")
        parent_node = ParentNode(None,[child_node])
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_novalchild(self):
        child_node = LeafNode("b",None)
        parent_node = ParentNode("p",[child_node])
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_no_children_raises(self):
        parent_node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_multiple_children(self):
        child1 = LeafNode("span", "one")
        child2 = LeafNode("b", "two")
        parent = ParentNode("div", [child1, child2])
        self.assertEqual(parent.to_html(), "<div><span>one</span><b>two</b></div>")

    def test_to_html_with_props(self):
        child = LeafNode("span", "child")
        parent = ParentNode("div", [child], {"class": "container"})
        self.assertEqual(
            parent.to_html(),
            '<div class="container"><span>child</span></div>',
        )
        
    def test_to_html_with_grandchildren_and_props(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node],{"href":"https://google.com"})
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            '<div><span href="https://google.com"><b>grandchild</b></span></div>',
        )


if __name__ == "__main__":
    unittest.main()