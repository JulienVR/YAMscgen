import unittest

from src.builder import Builder
from src.parser import Parser


def generate_img(input_txt):
    builder = Builder(Parser(input_txt))
    images = builder.generate()
    if len(images) > 1:
        for i, image in enumerate(images):
            with open(f"/home/odoo/Downloads/out-{i}.svg", "wb+") as f:
                f.write(image)
    else:
        with open(f"/home/odoo/Downloads/out.svg", "wb+") as f:
            f.write(images[0])


class TestScenarios(unittest.TestCase):

    def test1(self):
        generate_img(
            r"""msc {
            hscale = "2", width="500";
            arcgradient = "20", max-height="1500", font="courier", font-size="15";
                    
            a,b,c [linecolour="red"];
            
            # This is a comment;
            # a -> b [label="another comment"];
            # a -> b [label = "another comment containing \n tmp \n"];
            a->c [ label = "First Line\nCode:\nfont-family='helvetica-bold', font-weight='bold'", textbgcolor = "yellow", font-family="helvetica-bold"];
            a -> b [ label = "this should be on line X", textbgcolor = "yellow"],
            b-> c [ label = "this should be on line X as well", textbgcolor = "yellow", font-family="times-italic", font-style="italic"];
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

    def test_arcs_alignment(self):
        generate_img(
            r"""msc {
            a,b,c [linecolour="red"];

            a => b [label="oneliner label"],
            a note a [label="Several arcs on\nthe same line"],
            c => c [ label = "oneliner label", textbgcolor = "yellow"],
            c => b [label = "twoliner\nlabel"];
            a => b [label = "another label"],
            c => b [label = "this time, it's aligned"];
            }"""
        )

    def test_arcs_alignment_arcgradient(self):
        """ A small alignment problem (also for mscgen and mscgen_js)
        Conclusion: alignment is not guaranteed for labels having different number of lines
        """
        generate_img(
            r"""msc {
            arcgradient="30";
            a,b,c [linecolour="red"];
            
            a => b [label="oneliner label"],
            a note a [label="Several arcs on\nthe same line"],
            c => c [ label = "oneliner label", textbgcolor = "yellow"],
            c => b [label = "twoliner\nlabel"];
            a => b [label = "another label"],
            c => b [label = "this time, it's aligned"];
            }"""
        )

    def test2_low_arcgradient(self):
        generate_img(
            r"""msc {
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
            r"""msc {
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
            r"""msc {
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
            r"""msc {
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
            r"""msc {
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
            r"""msc {
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
            r"""msc {
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
            r"""msc {
            arcgradient = "10";
            a, b;
            a->b [label="this is a line\nand a new line"];
            }"""
        )

    def test_broadcast_arc(self):
        generate_img(
            r"""msc {
            arcgradient = "30";
            a, b, c;
            a->* [label = "broadcast"];
            *<-a [label = "broadcast"];
            a note c [label = "Broadcast arc"];
            }"""
        )

    def test_broadcast_arc_bis(self):
        generate_img(
            r"""msc {
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

    def test_omitted_signal(self):
        generate_img(
            r"""msc {
            font-size="20", font="courier", max-height="500";
            # entity D can be customized
            a, b, c, d [linecolour="red"];
            d note d [label = "a random\ncomment", bordercolor="green", textbgcolour="yellow"];
            ... [label="Omitted Signal\nbut with several\nlines", textbgcolour="yellow"];
            a->b;
            ... [label="Omitted Signal", textbgcolour="yellow"];
            a->b;
            --- [label="General Comment"];
            a->b;
            ||| [label = "extra space"];
            a -> b;
            # Example of the boxes with filled backgrounds
            a abox b [label="abox", textbgcolour="#ff7f7f"];
            b rbox c [label="rbox", textbgcolour="#7fff7f"];
            c note d [label="note", textbgcolour="#7f7fff"];
            }"""
        )

    def test_arity0_elements(self):
        generate_img(
            r"""msc {
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

    def test_aligned_elements(self):
        """ Check that the comments and arcs are aligned """
        generate_img(
            r"""msc {
            a [label="A\ntmp", linecolour="green", textbgcolor="yellow"], b [label="B"], c [label="Instructions"], d;
            
            a->b, c abox c [label="turlupff\ntest again"];
            a => b [label = "place for a label"],
            b => c [label = "1\n2\n3\n4"],
            c -> d,
            c note c [label="a => b\nsecond line\nthird line", textbgcolor="yellow"];
            a => b [label="line 1\nline 2\nline 3", textbgcolor="yellow"],
            c note c [label="a => b"];
            ||| [stroke="red"],
            c note c [label="|||", textbgcolour="#7CC1D7"];
            a => b, c note c [label="a => b"];
            ... [stroke="red"], 
            c note c [label="...", textbgcolour="#7CC1D7"];
            a => b, c note c [label="a => b"];
            --- [stroke="red"],
            c note c [label="---", textbgcolour="#7CC1D7"];
            a => b, c note c [label="a => b\nsecond line"];
            a=>b;
            b=>c;
            }"""
        )

    def test_aligned_elements_high_arcgradient(self):
        generate_img(
            r"""msc {
            arcgradient="50";
            a [label="A"], b [label="B"], c [label="Instructions"], d;
            
            a => b[label = "1\n2\n3"],
            c -> d [label = "1\n2"],
            c note c [label="a => b\nsecond line\nthird line", textbgcolor="yellow"];
            a => b [label="line 1\nline 2\nline3\nline4", textbgcolor="yellow"],
            c note c [label="a => b"];
            |||, c note c [label="|||", textbgcolour="#7CC1D7"];
            a => b, c note c [label="a => b"];
            ..., c note c [label="...", textbgcolour="#7CC1D7"];
            a => b, c note c [label="a => b"];
            ---, c note c [label="---", textbgcolour="#7CC1D7"];
            a => b, c note c [label="a => b"];
            }"""
        )

    def test_fig_arcs(self):
        generate_img(
            r"""msc {
            a [label="A"], b [label="B"];
            
            a -> b [label="a -> b"];
            a => b [label="a => b"];
            a >> b [label="a >> b"];
            a =>> b [label="a =>> b"];
            a :> b [label="a :> b"];
            a -x b [label="a -x b"];
            }"""
        )

    def test_fig_0air(self):
        generate_img(
            r"""msc {
            a [label="A"], b [label="B"], c [label="Instructions"];
            
            a => b, c note c [label="a => b"];
            a => b, c note c [label="a => b"];
            |||, c note c [label="|||", textbgcolour="#7CC1D7"];
            a => b, c note c [label="a => b"];
            ..., c note c [label="...", textbgcolour="#7CC1D7"];
            a => b, c note c [label="a => b"];
            ---, c note c [label="---", textbgcolour="#7CC1D7"];
            a => b, c note c [label="a => b"];
            }"""
        )

    def test_different_fonts(self):
        generate_img(
            r"""msc {
            a [label="Times"], b [label="Courier"], c [label="Helvetica"];
            
            a note a [label="Times-Roman", font-family="Times-Roman", textbgcolor="#dae8fc"],
            b note b [label="Courier", font-family="Courier", textbgcolor="#dae8fc"],
            c note c [label="Helvetica", textbgcolor="#dae8fc"];
            
            a note a [label="Times-Bold", font-family="Times-Bold", font-weight="bold", textbgcolor="#dae8fc"],
            b note b [label="Courier-Bold", font-family="Courier-Bold", font-weight="bold", textbgcolor="#dae8fc"],
            c note c [label="Helvetica-Bold", font-family="Helvetica-Bold", font-weight="bold", textbgcolor="#dae8fc"];
            
            a note a [label="Times-Italic", font-family="Times-Italic", font-style="italic", textbgcolor="#dae8fc"],
            b note b [label="Courier-Oblique", font-family="Courier-Oblique", font-style="italic", textbgcolor="#dae8fc"],
            c note c [label="Helvetica-Oblique", font-family="Helvetica-Oblique", font-style="italic", textbgcolor="#dae8fc"];
            }"""
        )

    def test_show_splitting_lines(self):
        generate_img(
            r"""msc {
            arcgradient="20";
            a [textbgcolor="#dae8fc"], b [textbgcolor="#dae8fc"];
            a -> b [label="This is a label\nspanning multiple lines", textbgcolor="#dae8fc"];
            b -> a [label="This is a oneliner", textbgcolor="#dae8fc"];
            b -> b [label="Arc to self\nbut multiline", textbgcolor="#dae8fc"];
            a note a [label="It also works\nwith notes", textbgcolor="#dae8fc"],
            b note b [label="Notice the alignment\nof another element\nhaving a longer label\non the same line", textbgcolor="#dae8fc"];
            }"""
        )
