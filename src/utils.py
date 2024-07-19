import xml.etree.ElementTree as ET
import random

# TODO generify usage of font
HELVETICA = {
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
    """Generates a random hex color"""
    hex_val = list(str(i) for i in range(10)) + ["a", "b", "c", "d", "e", "f"]
    return "#" + "".join(random.choices(hex_val, k=6))


def expand_lifelines(builder, root: ET.Element, y1, y2, extra_options: dict):
    """Increases each participant's lifeline using the vertical_step"""
    for coord in builder.participants_coordinates.values():
        ET.SubElement(
            root,
            "line",
            {
                #'stroke': random_color(),
                "stroke": "black",
                "x1": str(coord),
                "y1": str(y1),
                "x2": str(coord),
                "y2": str(y2),
                **extra_options,
            },
        )


def get_offset_from_label_multiple_lines(label, font_size):
    """A label may have multiple lines, hence needing the arcs to be shifted downwards."""
    offset = 0
    label_lines_count = len(label.split("\n"))
    if label_lines_count:
        offset = label_lines_count * font_size
    return offset


def get_text_width(text, font, font_size):
    """Returns the text length in pixels."""
    return (
        sum(HELVETICA["unicode_to_width"].get(ord(c), 0) for c in text)
        * font_size
        / 1000
    )


def get_text_ascender(font, font_size):
    return HELVETICA["ascender"] * font_size / 1000


def get_text_descender(font, font_size):
    return abs(HELVETICA["descender"]) * font_size / 1000


def get_text_height(font, font_size):
    return get_text_ascender(font, font_size) + get_text_descender(font, font_size)


def draw_label(root, x1, x2, y, font, font_size, options):
    """
    Draw the label right below the y coordinate, and in the middle of the x1, x2 coordinates.
    If there are multiple lines, expand the label downwards.
    :returns the lower vertical coordinate of the label drawn
    """
    label = options.get("label")
    if not label:
        return y
    MARGIN_DOWN = font_size
    MARGIN_LEFT_RIGHT = 2
    scaled_ascender = get_text_ascender(font, font_size)
    text_height = get_text_height(font, font_size)
    g = ET.Element("g")
    # for a label right below y, need to put the cursor at y + scaled_ascender (if y grows downwards)
    y += scaled_ascender
    # shift label upward if multiline
    if x1 == x2:
        y -= text_height * len(label.split("\n"))
    for idx, lab in enumerate(
        label.split("\n")
    ):  # labels may contain newline character
        # Draw Boxes
        text_width = get_text_width(lab, font, font_size)
        if x1 == x2:
            x = x1 + 3 * MARGIN_LEFT_RIGHT
        else:
            x = min(x1, x2) + abs(x2 - x1) / 2 - text_width / 2
        y += text_height if idx != 0 else 0
        rect = ET.SubElement(
            g,
            "rect",
            {
                "x": str(x - MARGIN_LEFT_RIGHT),
                "y": str(y - scaled_ascender),
                "width": str(text_width + 2 * MARGIN_LEFT_RIGHT),
                "height": str(text_height),
                "fill": options.get("textbgcolour")
                or options.get("textbgcolor")
                or "white",
            },
        )
        # Sometimes, the text goes beyond the SVG frame
        max_x = float(rect.attrib["x"]) + float(rect.attrib["width"])
        if max_x > float(root.attrib["width"]):
            root.attrib["width"] = str(max_x)
        # Draw text inside the box
        text = ET.SubElement(
            g,
            "text",
            {
                "x": str(x),
                "y": str(y),
                "font-size": str(font_size),
                "font-family": font,
                "fill": options.get("textcolour")
                or options.get("textcolor")
                or "black",
                **options,
            },
        )
        text.text = lab
    root.append(g)
    # add the scaled descender to get the lowest vertical coordinate of the label
    y += get_text_descender(font, font_size)
    # add the margin
    y += MARGIN_DOWN
    return y
