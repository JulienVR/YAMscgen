from xml.etree import ElementTree as ET
import re

from src.parser import Parser


class Builder():
    def __init__(self, input):
        self.parser = Parser(input)
        self.entities_coordinate = {}
        self.vertical_step = 28 + self.parser.context['arcgradient']
        self.stylesheets = []  # TODO

    def parse_arc(self, arc_txt):
        # TODO: ... | --- | ||| | box | rbox | abox | note
        match = re.findall("(\S*?) ?(=>>|<<=|->|<-|=>|<=|<<|>>|:>|<:|-x|x-|->\*|\*<-) ?(\S*)", arc_txt)
        if not match:
            raise Exception(f"Invalid expression: '{arc_txt}'")
        return match[0]

    def draw_entities(self, root, height):
        relative_position = float(root.attrib['width']) / (2 * len(self.parser.entities))
        x = relative_position
        for entity in self.parser.entities:
            label = entity['options'].pop('label', None)
            self.entities_coordinate[entity['name']] = x
            node = ET.SubElement(root, 'text', {
                'font-size': '12',
                'font-family': 'Helvetica',
                'fill': 'black',
                'text-anchor': 'middle',
                **entity['options'],
                'x': str(x),
                'y': str(height),
            })
            node.text = label or entity['name']
            x += 2 * relative_position

    def expand_entities(self, root, height, extra_options):
        for coord in self.entities_coordinate.values():
            ET.SubElement(root, 'line', {
                **extra_options,
                'stroke': 'black',
                'x1': str(coord),
                'y1': str(height),
                'x2': str(coord),
                'y2': str(height + self.vertical_step),
            })

    def generate(self):
        root = ET.Element('svg', {
            'version': '1.1',
            'width': str(self.parser.context['width'] * self.parser.context['hscale']),
            'xmlns': "http://www.w3.org/2000/svg",
        })

        height = 16
        self.draw_entities(root, height)
        height += 4

        for arc_list in self.parser.arcs:
            for arc in arc_list:
                if arc['arc'].startswith('...') or arc['arc'].startswith('---'):
                    # ...
                    self.expand_entities(root, height, {'stroke-dasharray': str(2)})
                elif arc['arc'].startswith('|||'):
                    self.expand_entities(root, height, {})
                else:
                    # line from entities
                    self.expand_entities(root, height, {})
                    # Arc
                    entity_from, arc_type, entity_to = self.parse_arc(arc['arc'])
                    label = arc['options'].pop('label', None)  # TODO (new node ?)
                    y = height + self.vertical_step/2
                    x2 = self.entities_coordinate[entity_to]
                    y2 = y + self.parser.context['arcgradient']
                    ET.SubElement(root, 'line', {
                        **arc['options'],
                        'stroke': 'black',
                        'x1': str(self.entities_coordinate[entity_from]),
                        'y1': str(y),
                        'x2': str(x2),
                        'y2': str(y2),
                    })
                    # Triangle (example: <polygon fill="purple" points="450,215 440,221 440,209"/>)
                    y1, y3 = y2 + 6, y2 - 6
                    if '>' in arc_type:
                        x1 = x3 = x2 - 10
                    else:
                        x1 = x3 = x2 + 10
                    ET.SubElement(root, 'polygon', {
                        'fill': 'black',
                        'points': f"{x1},{y1} {x2},{y2} {x3},{y3}",
                    })
                height += self.vertical_step

        # set height
        root.attrib['height'] = str(height)
        # indent
        tree = ET.ElementTree(root)
        ET.indent(tree, space="\t", level=0)
        tree.write("/home/odoo/Downloads/tmp.svg", encoding="utf-8")
        return ET.tostring(root, encoding="UTF-8")
