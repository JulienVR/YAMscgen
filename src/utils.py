import xml.etree.ElementTree as ET
import random

# TODO generify usage of font
HELVETICA = {
    'capheight': 718,
    'xheight': 523,
    'ascender': 718,
    'descender': -207,
    'unicode_to_width': {
        32: 278, 33: 278, 34: 355, 35: 556, 36: 556, 37: 889, 38: 667, 39: 222, 40: 333, 41: 333, 42: 389, 43: 584,
        44: 278, 45: 333, 46: 278, 47: 278, 48: 556, 49: 556, 50: 556, 51: 556, 52: 556, 53: 556, 54: 556, 55: 556,
        56: 556, 57: 556, 58: 278, 59: 278, 60: 584, 61: 584, 62: 584, 63: 556, 64: 1015, 65: 667, 66: 667, 67: 722,
        68: 722, 69: 667, 70: 611, 71: 778, 72: 722, 73: 278, 74: 500, 75: 667, 76: 556, 77: 833, 78: 722, 79: 778,
        80: 667, 81: 778, 82: 722, 83: 667, 84: 611, 85: 722, 86: 667, 87: 944, 88: 667, 89: 667, 90: 611, 91: 278,
        92: 278, 93: 278, 94: 469, 95: 556, 96: 222, 97: 556, 98: 556, 99: 500, 100: 556, 101: 556, 102: 278, 103: 556,
        104: 556, 105: 222, 106: 222, 107: 500, 108: 222, 109: 833, 110: 556, 111: 556, 112: 556, 113: 556, 114: 333,
        115: 500, 116: 278, 117: 556, 118: 500, 119: 722, 120: 500, 121: 500, 122: 500, 123: 334, 124: 260, 125: 334,
        126: 584, 161: 333, 162: 556, 163: 556, 164: 167, 165: 556, 166: 556, 167: 556, 168: 556, 169: 191, 170: 333,
        171: 556, 172: 333, 173: 333, 174: 500, 175: 500, 177: 556, 178: 556, 179: 556, 180: 278, 182: 537, 183: 350,
        184: 222, 185: 333, 186: 333, 187: 556, 188: 1000, 189: 1000, 191: 611, 193: 333, 194: 333, 195: 333, 196: 333,
        197: 333, 198: 333, 199: 333, 200: 333, 202: 333, 203: 333, 205: 333, 206: 333, 207: 333, 208: 1000, 225: 1000,
        227: 370, 232: 556, 233: 778, 234: 1000, 235: 365, 241: 889, 245: 278, 248: 222, 249: 611, 250: 944, 251: 611,
    }
}


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


def get_offset_from_label_multiple_lines(label, font_size):
    """ A label may have multiple lines, hence needing the arcs to be shifted downwards. """
    offset = 0
    label_lines_count = len(label.split('\n'))
    if label_lines_count:
        offset = label_lines_count * font_size
    return offset


def get_text_width(text, font_size):
    """ Returns the text length in pixels. """
    return sum(HELVETICA['unicode_to_width'].get(ord(c), 0) for c in text) * font_size / 1000


def draw_label_v2(root, x1, x2, y, font_size, options):
    """
    Draw the label below the y coordinate, and in the middle of the x1, x2 coordinates.
    If there are multiple lines, expand the label downwards.
    """
    label = options.get('label')
    if not label:
        return
    MARGIN = 1  # upper, left and right margin
    g = ET.Element('g')
    scaled_ascender = HELVETICA['ascender'] * font_size / 1000
    y += scaled_ascender + MARGIN
    for idx, lab in enumerate(label.split('\n')):  # labels may contain newline character
        # Draw Boxes
        text_width = get_text_width(lab, font_size)
        if x1 == x2:
            x = x1
        else:
            x = min(x1, x2) + abs(x2 - x1) / 2 - text_width / 2
        text_height = (HELVETICA['ascender'] - HELVETICA['descender']) * font_size / 1000
        y += idx * text_height
        if lab == '':
            continue
        rect = ET.SubElement(g, 'rect', {
            'x': str(x - MARGIN),
            'y': str(y - scaled_ascender),
            'width': str(text_width + 2 * MARGIN),
            'height': str(text_height),
            'fill': options.get('textbgcolour') or options.get('textbgcolor') or 'white',
        })
        # Sometimes, the text goes beyond the SVG frame
        max_x = float(rect.attrib['x']) + float(rect.attrib['width'])
        if max_x > float(root.attrib['width']):
            root.attrib['width'] = str(max_x)
        # Draw text inside the box
        text = ET.SubElement(g, 'text', {
            'x': str(x - MARGIN),
            'y': str(y),
            'style': f"font-size: {font_size}",
            'font-family': 'Helvetica',
        })
        text.text = lab
    root.append(g)


def draw_label(root, x1, x2, y1, y2, font_size, options, y_offset_factor=1, arc_to_self=False):
    label = options.get('label')
    if not label:
        return
    MARGIN = 1  # margin before and after the label
    OFFSET = HELVETICA['ascender']/2 * font_size/1000  # offset above the arc
    g = ET.Element('g')
    lines_count = len(label.split('\n'))
    for idx, lab in enumerate(label.split('\n')):  # labels may contain newline character
        # Draw Boxes
        text_width = get_text_width(lab, font_size)
        if arc_to_self:
            x = x1 + OFFSET
            y = (y1 - OFFSET)
        else:
            x = min(x1, x2) + abs(x2 - x1) / 2 - text_width / 2
            y = ((y1 + y2) / 2 - y_offset_factor * OFFSET)
        text_height = (HELVETICA['ascender'] - HELVETICA['descender']) * font_size / 1000
        scaled_ascender = HELVETICA['ascender'] * font_size / 1000
        y -= (lines_count - idx - 1) * text_height
        box_x = x - MARGIN
        if lab == '':
            continue
        rect = ET.SubElement(g, 'rect', {
            'x': str(box_x),
            'y': str(y - scaled_ascender),
            'width': str(text_width + 2 * MARGIN),
            'height': str(text_height),
            'fill': options.get('textbgcolour') or options.get('textbgcolor') or 'white',
        })
        # Sometimes, the text goes beyond the SVG frame
        max_x = float(rect.attrib['x']) + float(rect.attrib['width'])
        if max_x > float(root.attrib['width']):
            root.attrib['width'] = str(max_x)
        # Draw text inside the box
        text = ET.SubElement(g, 'text', {
            'x': str(box_x),
            'y': str(y),
            'style': f"font-size: {font_size}",
            'font-family': 'Helvetica',
        })
        text.text = lab
    root.append(g)
