from src.utils import InvalidInputException
from .common import YAMscgenTestCommon


class TestScenarios(YAMscgenTestCommon):

    def test1(self):
        self.generate_img(
            r"""msc {
            hscale = "2", width="500";
            arcgradient = "20", max-height="1500", font="courier", font-size="15";
                    
            a,b,c [linecolour="red"];
            
            # This is a comment;
            # a -> b [label="another comment"];
            # a -> b [label = "another comment containing \n tmp \n"];
            a->c [ label = "First Line\nCode:\nfont-family='helvetica-bold', font-weight='bold'", textbgcolor = "yellow", font-family="helvetica-bold", font-weight="bold"];
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
        self.generate_img(
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
        self.generate_img(
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
        self.generate_img(
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
        self.generate_img(
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
        self.generate_img(
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
        self.generate_img(
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
        self.generate_img(
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
        self.generate_img(
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
        self.generate_img(
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
        self.generate_img(
            r"""msc {
            arcgradient = "10";
            a, b;
            a->b [label="this is a line\nand a new line"];
            }"""
        )

    def test_broadcast_arc(self):
        self.generate_img(
            r"""msc {
            arcgradient = "30";
            a, b, c;
            a->* [label = "broadcast"];
            *<-a [label = "broadcast"];
            a note c [label = "Broadcast arc"];
            }"""
        )

    def test_broadcast_arc_bis(self):
        self.generate_img(
            r"""msc {
            # This is a comment
            # another comment
            arcgradient = "30";
            font-size="16";
            font="Helvetica";
            a [textbgcolour = "turquoise", label = "A is very\nimportant"],
            b [label = "BBB", font-size="20", textbgcolour = "turquoise"], c, d;
            b->* [label = "broadcast with custom key"];
            b->* [label = "broadcast", textcolor="red"];
            *<-b [label = "broadcast\non several lines\nthis time\nreally!", textbgcolor="turquoise", linecolor="blue"];
            b note c [label = "Broadcast arc", textbgcolour="grey"];
            b abox c [label = "Broadcast arc", textbgcolour="yellow"];
            }"""
        )

    def test_omitted_signal(self):
        self.generate_img(
            r"""msc {
            font-size="20", font="courier", max-height="500";
            # entity D can be customized
            a, b, c, d [linecolour="red"];
            d note d [label = "a random\ncomment", bordercolor="green", textbgcolour="yellow"];
            ... [label="Omitted Signal\nbut with several\nlines", textbgcolour="yellow", font-size="15"];
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
        self.generate_img(
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
        self.generate_img(
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
        self.generate_img(
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
        self.generate_img(
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
        self.generate_img(
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
        self.generate_img(
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
        self.generate_img(
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

    def test_alignment(self):
        self.generate_img(
            r"""msc {
            arcgradient="10";
            a, b, c, d;
            a => b,
            b=>c [label="line 1"],
            c=>d [label="line 1\nline 2\nline 3"];
            a => a,
            b=>b [label="line 1"],
            c=>c [label="line 1\nline 2"],
            d=>d [label="line 1\nline 2\nline 3"];
            }"""
        )

    def test_alignment_2(self):
        self.generate_img(
            r"""msc {
            arcgradient="20";
            a, b, c, d;
            
            a=>b,
            b=>c [label="line 1\nline 2"],
            c=>d [label="line 1\nline 2\nline 3\nline 4\nline 5"];
        
            a=>a,
            b=>b [label="line 1\nline 2"],
            c=>c [label="line 1\nline 2\nline 3\nline 4\nline 5"],
            d note d [label = "Note should be\naligned too !"];
            }"""
        )

    def test_split_max_height_low(self):
        with self.assertRaisesRegex(InvalidInputException, "The max-height '50.0' is insufficient for the diagram to be drawn."):
            self.generate_img(
                r"""msc {
                max-height="50";
                a, b;
                a -> b [label="first"];
                a -> b [label="second"];
                b -> a [label="third"];
                }"""
            )

        # but this should work
        self.generate_img(
            r"""msc {
            max-height="100";
            a, b;
            a -> b [label="first"];
            a -> b [label="second"];
            b -> a [label="third"];
            }"""
        )

    def test_special_char(self):
        # '[' and ']' are sensitive chars
        self.generate_img(
            r"""msc {
            a, b;
            a -> b [label="hey [] hey [start\nend]"];
            }"""
        )

    def test_demo_example(self):
        self.generate_img(
            r"""msc {
            # Global options here
            arcgradient="10";
            
            # Entities here
            a [label="Entity A", textbgcolor="#82b366"],
            b [label="Entity B", textbgcolor="grey"],
            c [label="Entity C", textbgcolor="#d79b00"];
            
            # Arcs, boxes
            
            # A line finishes with ';'
            a=>b [label="First call"];
            
            # Several elements can be aligned
            b=>b [label="Processing...", textbgcolor="yellow"], 
            c note c [label="Several elements\ncan be on the\nsame line", textbgcolor="#dae8fc"];
            
            c -> b [label="Another arc type"];
            b >> a [label="A dashed arc\nis useful here"],
            c rbox c [label="This is another\ntype of comment", textbgcolor="#dae8fc"];
            
            ... [label="Time flies...", textcolor="blue"];
            
            a:>b [label="And this is an\nemphasized arc"];
            a->c [label="Last call", linecolor="red"];
            }"""
        )

    def test_arbitrary_attributes(self):
        self.generate_img(
            r"""msc {
            arcgradient="20";
            
            a [label="A", textbgcolor="coral"],
            b [label="Big B", linecolor="royalblue", font-size="20"],
            c [label="Instructions", textbgcolor="#dae8fc"];
            
            b => a [label="Arc 1", font-family="Times-Bold", font-weight="bold", font-size="20", textbgcolor="yellow"],
            c note c [label="font-family='Times-Bold',\nfont-weight='bold',\nfont-size='20'", textbgcolor="#dae8fc"];
            
            b => a [stroke-width="2", label="Arc 2", font-family="courier"],
            c note c [label="stroke-width='2',\nfont-family='courier'", textbgcolor="#dae8fc"];
            
            b => b [opacity="0.4", label="arc to self\nwith opacity", font-style="italic", font-family="Times-Italic"],
            c note c [label="opacity='0.4',\nfont-style='italic',\nfont-family='Times-Italic'", textbgcolor="#dae8fc"];
            }"""
        )

    def test_colors(self):
        self.generate_img(
            r"""msc {
            arcgradient="20";

            a [label="line line", textbgcolor="coral", font-family="courier"],
            b [label="B", linecolor="royalblue"],
            c [label="Instructions", textbgcolor="#dae8fc"];

            b => a [label="Arc 1", textbgcolor="goldenrod"];
            }"""
        )

    def test_example_split(self):
        self.generate_img(
            r"""msc {
            arcgradient="20", max-height="124";
            a [textbgcolor="#82b366"], b [textbgcolor="#82b366"], c [textbgcolor="#82b366"];
            
            a=>b [label="line 1\nline 2"],
            b=>c [label="line 1\nline 2\nline 3\nline 4\nline 5"];
        
            a=>a [label="line 1"],
            b=>b [label="line 1\nline 2\nline 3"],
            c=>c [label="line 1\nline 2\nline 3\nline 4\nline 5"];
            }"""
        )

    def test_tcp(self):
        self.generate_img(
            r"""msc {
            # global options
            arcgradient="20";
            
            # entities
            commentsA  [label=" ", linecolor="white"],
            a [label="Client", textbgcolour="#7CC1D7"],
            b [label="Server", textbgcolour="#568203"],
            commentsB  [label=" ", linecolor="white"];
            
            commentsA note commentsA  [label="closed", linecolor="black", textbgcolor="#FFFFCC", font-family="courier"], 
            commentsB note commentsB  [label="closed", linecolor="black", textbgcolor="#FFFFCC", font-family="courier"];
        
            a=>b [label="SYN=1, seq=client_ISN", textcolour="blue"];
            a<=b [label="SYN=1, seq=server_ISN\nack=client_ISN+1", textcolour="#568203"];
            a=>b [label="SYN=0, seq=client_ISN+1\nack=server_ISN+1", textcolour="blue"];
            
            commentsA note commentsA  [label="established", linecolor="black", textbgcolor="#FFFFCC", font-family="courier"], 
            commentsB note commentsB  [label="established", linecolor="black", textbgcolor="#FFFFCC", font-family="courier"];
            }"""
        )
