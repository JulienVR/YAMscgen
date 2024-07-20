import unittest

from src.builder import Builder
from src.parser import Parser


def generate_img(input_txt, **kwargs):
    builder = Builder(Parser(input_txt), **kwargs)
    image = builder.generate()
    with open("/home/odoo/Downloads/out.svg", "wb+") as f:
        f.write(image)


class Test(unittest.TestCase):

    def test1(self):
        generate_img(
            """msc {
            hscale = "2", arcgradient = "20", max-height="500";
                    
            a,b,c;
            
            a->c [ label = "ac1()\nac2()\nanother new long line\nand yet another one", textbgcolor = "yellow", font-family="courier", font-weight="bold"];
            a -> b [ label = "this should be on line X", textbgcolor = "yellow"],
            b-> c [ label = "this should be on line X as well", textbgcolor = "yellow"];
            c =>c [ label = "process(1)", textbgcolor = "yellow"];
            c=>c [ label = "process(2)", textbgcolor="yellow" ];
            ...;
            c=>c [ label = "ac1()\nac2()\nanother new long line", linecolor="blue", textbgcolor = "yellow" ];
            c=>c [ label = "process(END)", textbgcolor="yellow"];
            a<<=c [ label = "callback()", textbgcolor="yellow"];
            ---  [ label = "If more to run", font-family="courier", textbgcolor="yellow"];
            a->a [ label = "next()", textbgcolor="yellow"];
            b<-c [ label = "cb(TRUE)", textbgcolor="yellow"];
            b->b [ label = "stalled(...)", textbgcolor="yellow"];
            a<-b [ label = "ab() = FALSE", textbgcolor="yellow"];
        }"""
        )

    def test2_low_arcgradient(self):
        generate_img(
            """msc {
            arcgradient="10";
            a [label="Client"],b [label="Server"];
            
            a=>b [label="data1"];
            a-xb [label="data2"];
            a=>b [label="data3\nanother line\nagain another one"];
            a<=b [label="ack1, nack2"];
            a=>b [arcskip="2"], a=>b [label="no arcskip VS arcskip"];
            |||;
            a<=b [label="ack3"];
            |||;
            }"""
        )

    def test2_avg_arcgradient(self):
        generate_img(
            """msc {
            arcgradient="30";
            a [label="Client"],b [label="Server"];
            
            a=>b [label="data1"];
            a-xb [label="data2"];
            a=>b [label="data3\nanother line\nagain another one"];
            a<=b [label="ack1, nack2"];
            a=>b [label="data2", arcskip="1"];
            |||;
            a<=b [label="ack3"];
            |||;
            }"""
        )

    def test_drawing_boxes(self):
        generate_img(
            """msc {
            arcgradient = "20";
            font-size = "15";
            # The entities
            A, B, C, D;
            
            # Small gap before the boxes
            |||;
            
            # Next four on same line due to ','
            A box A [label="box", textbgcolour="turquoise"],
            B rbox B [label="rbox"], C abox C [label="abox"] ,
            D note D [label="note\nline1\nline2\nline3\nline4"];
            
            # Example of the boxes with filled backgrounds
            A abox B [label="abox\nabox", textbgcolour="#ff7f7f"];
            B rbox C [label="rbox", textbgcolour="#7fff7f"];
            C note D [label="note", textbgcolour="#7f7fff"];
            }"""
        )

    def test_drawing_boxes_hscale(self):
        generate_img(
            """msc {
            arcgradient = "10";
            hscale = "2";
            # The entities
            A, B, C, D;
            
            # Small gap before the boxes
            |||;
            
            # Next four on same line due to ','
            A box A [label="box\nturlututu", textbgcolour="turquoise"],
            B rbox B [label="rbox"], C abox C [label="abox"] ,
            D note D [label="note"];
            
            # Example of the boxes with filled backgrounds
            A abox B [label="abox", textbgcolour="#ff7f7f"];
            B rbox C [label="rbox", textbgcolour="#7fff7f"];
            C note D [label="note", textbgcolour="#7f7fff"];
            }"""
        )

    def test_arc_to_self(self):
        generate_img(
            """msc {
            arcgradient = "10";
            # The entities
            A, B;
            
            # Next four on same line due to ','
            A -> B [label = "this is label ppp", linecolor="red", textbgcolour = "turquoise"];
            B -> A [label = "this is label", linecolor="red"];
            B => B [label = "this is label 1", linecolour="blue", textbgcolor = "turquoise"];
            A => B [label = "this is label 1", linecolour="blue"];
            A >> A [label = "label >>"]; 
            A << B [label = "label >>"]; 
            A =>> B [label = "label =>>", textbgcolour = "turquoise"];
            A :> B [label = "label :>"];
            A <: B [label = "label :> bla bla bla"];
            B <: B [label = "label :> bla bla bla"];
            B -x A [label = "label -x"];
            }
            """
        )

    def test_arc_to_self_avg_arcgradient(self):
        generate_img(
            """msc {
            arcgradient = "30";
            # The entities
            A, B;
            
            # Next four on same line due to ','
            A -> B [label = "this is label ppp", linecolor="red", textbgcolour = "turquoise"];
            B -> A [label = "this is label", linecolor="red"];
            B => B [label = "this is label 1", linecolour="blue", textbgcolor = "turquoise"];
            A => B [label = "this is label 1", linecolour="blue"];
            A >> A [label = "label >>"]; 
            A << B [label = "label >>"]; 
            A =>> B [label = "label =>>", textbgcolour = "turquoise"];
            A :> B [label = "label :>"];
            A <: B [label = "label :> bla bla bla"];
            B <: B [label = "label :> bla bla bla"];
            B -x A [label = "label -x"];
            }
            """
        )

    def test_arc_to_self_high_arcgradient(self):
        generate_img(
            """msc {
            arcgradient = "50";
            # The entities
            A, B;
            
            # Next four on same line due to ','
            A -> B [label = "this is label ppp", linecolor="red", textbgcolour = "turquoise"];
            B -> A [label = "this is label", linecolor="red"];
            B => B [label = "this is label 1", linecolour="blue", textbgcolor = "turquoise"];
            A => B [label = "this is label 1", linecolour="blue"];
            A >> A [label = "label >>"]; 
            A << B [label = "label >>"]; 
            A =>> B [label = "label =>>", textbgcolour = "turquoise"];
            A :> B [label = "label :>"];
            A <: B [label = "label :> bla bla bla"];
            B <: B [label = "label :> bla bla bla"];
            B -x A [label = "label -x"];
            }
            """
        )

    def test_newline_char(self):
        generate_img(
            """msc {
            arcgradient = "10";
            a, b;
            a->b [label="this is a line\nand a new line"];
            }"""
        )

    def test_broadcast_arc(self):
        generate_img(
            """msc {
            arcgradient = "30";
            a, b, c;
            a->* [label = "broadcast"];
            *<-a [label = "broadcast"];
            a note c [label = "Broadcast arc"];
            }"""
        )

    def test_broadcast_arc_bis(self):
        generate_img(
            """msc {
            # This is a comment
            # another comment
            arcgradient = "30";
            font-size="16";
            font="Helvetica";
            a [textbgcolour = "turquoise", label = "Participant 1\ntrès important"],
            b [label = "BBB", font-size="20", textbgcolour = "turquoise"], c, d;
            b->* [label = "broadcast with custom key"];
            b->* [label = "broadcast", textcolor="red"];
            *<-b [label = "broadcast\non several lines\nthis time\nreally!", textbgcolor="turquoise", linecolor="blue"];
            b note c [label = "Broadcast arc", textbgcolour="grey"];
            b abox c [label = "Broadcast arc", textbgcolour="yellow"];
            }"""
        )

    def test4(self):
        line = ' ... [label = "this is ...", ID="1"], --- [label = "2nd", ID="2"];'
        lines = Parser.split_elements_on_line(line)
        self.assertEqual(
            lines,
            ['... [label = "this is ...", ID="1"]', '--- [label = "2nd", ID="2"]'],
        )

    def test5(self):
        line = " ...  , --- ;"
        lines = Parser.split_elements_on_line(line)
        self.assertEqual(lines, ["...", "---"])

    def test_parse_options(self):
        line = 'a->b [label="test label,\non several; lines", arcskip="1", fill="red"]'
        options = Parser.parse_options(line)
        self.assertEqual(
            options,
            {
                "label": "test label,\non several; lines",
                "arcskip": "1",
                "fill": "red",
            },
        )

    def test_arity1_elements(self):
        generate_img(
            """msc {
            arcgradient = "30";
            font="Courier";
            a, b;
            a->b [label="arc"];
            --- [label="general comment\nwhich is on several lines\nand another one", textbgcolor="turquoise"];
            a->b [label="fourth arc"];
            --- [label="general comment", textbgcolor="turquoise"];
            a->b;
            ||| [label="extra space", textbgcolor="turquoise"];
            a->b [label="arc"];
            ... [label="omitted signal", textbgcolor="turquoise"];
            a->b [label="arc"];
            }"""
        )


if __name__ == "__main__":
    unittest.main()
