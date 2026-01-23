import unittest

from extract_title import extract_title

class Test_Title_Extract(unittest.TestCase):
    def test_extract_normal_conditions(self):
        md="""
# This is a header

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        header = extract_title(md)
        self.assertEqual(header,"This is a header")

    def test_extract_multiple_headers(self):
        md="""
# This is a header

# This is another header

- This is a list
- with items
"""
        header = extract_title(md)
        self.assertEqual(header,"This is a header")

    def test_extract_header_more1st(self):
        md="""
## This is a header

# This is another header

- This is a list
- with items
"""
        header = extract_title(md)
        self.assertEqual(header,"This is another header")

    def test_extract_header_no_header(self):
        md="""
## This is a header

This is another header

- This is a list
- with items
"""
        with self.assertRaises(Exception):
              header = extract_title(md)

if __name__ == "__main__":
    unittest.main()