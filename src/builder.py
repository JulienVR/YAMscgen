import xml.etree.ElementTree as ET

from src.parser import Parser


class Builder:
    def __init__(self, input):
        self.parser = Parser(input)
        self.participants_coordinates = {}
        self.vertical_step = 28 + self.parser.context['arcgradient']
        self.stylesheets = []
        self.current_height = 16

    def draw_participants(self, root, height):
        """ Draw participants (on top of the image) """
        relative_position = float(root.attrib['width']) / (2 * len(self.parser.participants))
        x = relative_position
        for entity in self.parser.participants:
            label = entity['options'].pop('label', None)
            self.participants_coordinates[entity['name']] = x
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

    def generate(self):
        root = ET.Element('svg', {
            'version': '1.1',
            'width': str(self.parser.context['width'] * self.parser.context['hscale']),
            'xmlns': "http://www.w3.org/2000/svg",
        })

        self.draw_participants(root, self.current_height)
        self.current_height += 4
        for elements in self.parser.elements:
            for element in elements:
                element.draw(builder=self, root=root)

        # set height
        root.attrib['height'] = str(self.current_height)
        # indent
        tree = ET.ElementTree(root)
        ET.indent(tree, space="\t", level=0)
        tree.write("/home/odoo/Downloads/tmp.svg", encoding="utf-8")
        return ET.tostring(root, encoding="UTF-8")
