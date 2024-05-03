import unittest

from src.builder import Builder, Parser


class Test(unittest.TestCase):

    def test1(self):
        builder = Builder("""msc {
          hscale = "2";
        
          a,b,c;
        
          a -> b [ label = "ab()" ] ;
          b-> c [ label = "bc(TRUE)"];
          c =>c [ label = "process(1)" ];
          c=>c [ label = "process(2)" ];
          ...;
          c=>c [ label = "process(n)" ];
          c=>c [ label = "process(END)" ];
          a<<=c [ label = "callback()"];
          ---  [ label = "If more to run", ID="*" ];
          a->a [ label = "next()"];
          a->c [ label = "ac1()\nac2()"];
          b<-c [ label = "cb(TRUE)"];
          b->b [ label = "stalled(...)"];
          a<-b [ label = "ab() = FALSE"];
        }""")
        print(builder.parser)
        image = builder.generate()

    def test2(self):
        """
        Vertical step = 28 (arbitrary value) + arcgradient = 36
        """
        builder = Builder("""msc {
        
         # Comment
         arcgradient = "8";
        
         a [label="Client"],b [label="Server"];
        
         a=>b [label="data1"];
         a-xb [label="data2"];
         a=>b [label="data3"];
         a<=b [label="ack1, nack2"];
         a=>b [label="data2", arcskip="1"];
         |||;
         a<=b [label="ack3"];
         |||;
        }""")
        print(builder.parser)
        image = builder.generate()

    def test3(self):
        builder = Builder("""msc {
        
           # The entities
           A, B, C, D;
        
           # Small gap before the boxes
           |||;
        
           # Next four on same line due to ','
           A box A [label="box"],
           B rbox B [label="rbox"], C abox C [label="abox"] ,
           D note D [label="note"];
        
           # Example of the boxes with filled backgrounds
           A abox B [label="abox", textbgcolour="#ff7f7f"];
           B rbox C [label="rbox", textbgcolour="#7fff7f"];
           C note D [label="note", textbgcolour="#7f7fff"];
        }""")
        print(builder.parser)
        image = builder.generate()
        
    def test4(self):
        line = ' ... [label = "this is ...", ID="1"], --- [label = "2nd", ID="2"];'
        lines = Parser.split_elements_on_line(line)
        self.assertEqual(lines, ['... [label = "this is ...", ID="1"]', '--- [label = "2nd", ID="2"]'])

    def test5(self):
        line = ' ...  , --- ;'
        lines = Parser.split_elements_on_line(line)
        self.assertEqual(lines, ['...', '---'])


if __name__ == "__main__":
    unittest.main()
