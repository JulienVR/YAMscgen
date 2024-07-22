import unittest

from src.parser import Parser


class TestParser(unittest.TestCase):

    def test_parse_options(self):
        line = r'a->b [label="test label,\non several; lines", arcskip="1", fill="red"]'
        options = Parser.parse_options(line)
        self.assertEqual(
            options,
            {
                "label": r"test label,\non several; lines",
                "arcskip": "1",
                "fill": "red",
            },
        )

    def test_split_elements_on_line_1(self):
        line = " ...  , --- ;"
        lines = Parser.split_elements_on_line(line)
        self.assertEqual(lines, ["...", "---"])

    def test_split_elements_on_lines_2(self):
        line = ' ... [label = "this is ...", ID="1"], --- [label = "2nd", ID="2"];'
        lines = Parser.split_elements_on_line(line)
        self.assertEqual(
            lines,
            ['... [label = "this is ...", ID="1"]', '--- [label = "2nd", ID="2"]'],
        )
