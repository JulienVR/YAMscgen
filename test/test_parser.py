from src.parser import Parser, InvalidInputException
from .common import YAMscgenTestCommon


class TestParser(YAMscgenTestCommon):

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

    def test_undeclared_entity(self):
        with self.assertRaisesRegex(InvalidInputException, "The participant 'b' was not declared."):
            self.generate_img(
                r"""msc {
                a;
                a -> b;
                }"""
            )

    def test_undeclared_entities(self):
        with self.assertRaisesRegex(InvalidInputException, "'a -> b' is not a valid participant name."):
            self.generate_img(
                r"""msc {
                a -> b;
                }"""
            )

    def test_malformed_attributes_1(self):
        with self.assertRaisesRegex(InvalidInputException, "Options should start with '\[' and end with '\]' on line 'a -> b \[turlututu'."):
            self.generate_img(
                r"""msc {
                a, b;
                a -> b [turlututu;
                }"""
            )

    def test_malformed_attributes_2(self):
        with self.assertRaisesRegex(InvalidInputException, "Invalid attribute 'turlututu' on line 'a -> b \[turlututu\]'."):
            self.generate_img(
                r"""msc {
                a, b [label="B!"];
                a -> b [turlututu];
                }"""
            )

    def test_malformed_attributes_3(self):
        with self.assertRaisesRegex(InvalidInputException, "Invalid attribute 'turlututu' on line 'a -> b \[label=\"yup\", turlututu\]'."):
            self.generate_img(
                r"""msc {
                a [label="A", textbgcolor="red"], b [label="B!"];
                a -> b [label="one", textbgcolor="red"];
                a -> b [label="yup", turlututu];
                }"""
            )
