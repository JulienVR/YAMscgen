import xml.etree.ElementTree as ET


def expand_lifelines(builder, root: ET.Element, extra_options: dict):
    """ Increases each participant's lifeline using the vertical_step """
    for coord in builder.participants_coordinates.values():
        ET.SubElement(root, 'line', {
            **extra_options,
            'stroke': 'black',
            'x1': str(coord),
            'y1': str(builder.current_height),
            'x2': str(coord),
            'y2': str(builder.current_height + builder.vertical_step),
        })
