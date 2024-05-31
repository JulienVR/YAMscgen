import xml.etree.ElementTree as ET
import random


def random_color():
    """ Generates a random hex color """
    hex_val = list(str(i) for i in range(10)) + ['a', 'b', 'c', 'd', 'e', 'f']
    return "#" + "".join(random.choices(hex_val, k=6))


def expand_lifelines(builder, root: ET.Element, y1, y2, extra_options: dict):
    """ Increases each participant's lifeline using the vertical_step """
    for coord in builder.participants_coordinates.values():
        ET.SubElement(root, 'line', {
            #'stroke': random_color(),
            'stroke': 'black',
            'x1': str(coord),
            'y1': str(y1),
            'x2': str(coord),
            'y2': str(y2),
            **extra_options,
        })
