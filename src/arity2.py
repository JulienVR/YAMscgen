import xml.etree.ElementTree as ET

import src.utils as utils


class Arity2:
    def __init__(self, src, dst, element, options):
        self.src = src
        self.dst = dst
        self.element = element
        self.options = options


class Arc(Arity2):
    def __init__(self, src, dst, element, options):
        assert element in ('->', '=>', '>>', '=>>', ':>', '-x'), f"Unsupported type: {element}"
        super().__init__(src, dst, element, options)

    def __repr__(self):
        return f"<Arc> {self.src}{self.element}{self.dst} {self.options}"

    def draw(self, builder, root: ET.Element):
        # Participant's line
        utils.expand_lifelines(builder, root, self.options)
        # Arc
        y1 = builder.current_height + builder.vertical_step / 2
        x1 = builder.participants_coordinates[self.src]
        x2 = builder.participants_coordinates[self.dst]
        y2 = y1 + builder.parser.context['arcgradient']
        ET.SubElement(root, 'line', {
            **self.options,
            'stroke': 'black',
            'x1': str(x1),
            'y1': str(y1),
            'x2': str(x2),
            'y2': str(y2),
        })
        # Triangle (example: <polygon fill="purple" points="450,215 440,221 440,209"/>)
        y1, y3 = y2 + 6, y2 - 6
        if x1 < x2:
            x1 = x3 = x2 - 10
        else:
            x1 = x3 = x2 + 10
        ET.SubElement(root, 'polygon', {
            'fill': 'black',
            'points': f"{x1},{y1} {x2},{y2} {x3},{y3}",
        })
        # Increase height pointer
        builder.current_height += builder.vertical_step


class Box(Arity2):
    def __init__(self, src, dst, element, options):
        assert element in ('box', 'rbox', 'abox', 'note')
        super().__init__(src, dst, element, options)

    def __repr__(self):
        return f"<Box> {self.src}{self.element}{self.dst} {self.options}"

    def draw(self, builder, root: ET.Element, extra_options: dict = False):
        pass
