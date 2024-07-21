import logging
import os
import random
import re
import xml.etree.ElementTree as ET

logger = logging.getLogger(__name__)


def parse_afm_files():
    """ Returns a dict mapping the font_name to the ascender, descender and width of each Unicode code point """
    fonts = {}
    fonts_directory = os.path.dirname(__file__) + "/../pdfcorefonts"
    for filename in os.listdir(fonts_directory):
        path = os.path.join(fonts_directory, filename)
        if not os.path.isfile(path) or not filename.endswith('.afm'):
            continue
        with open(path, 'r') as f:
            content = f.read()
        font_name_match = re.findall(r"FontName (.*)\n", content)
        ascender_match = re.findall(r"Ascender (\d*)", content)
        descender_match = re.findall(r"Descender (-?\d*)", content)
        if not (font_name_match and ascender_match and descender_match):
            continue
        unicode_to_width = {float(k): float(v) for k, v in re.findall(r"C (\d*) ; WX (\d*) ", content)}
        fonts[font_name_match[0].lower()] = {
            'ascender': float(ascender_match[0]),
            'descender': float(descender_match[0]),
            'unicode_to_width': unicode_to_width,
        }
    return fonts


def random_color():
    """Generates a random hex color"""
    hex_val = list(str(i) for i in range(10)) + ["a", "b", "c", "d", "e", "f"]
    return "#" + "".join(random.choices(hex_val, k=6))


def expand_lifelines(builder, root: ET.Element, y1, y2, extra_options: dict):
    """Increases each participant's lifeline using the vertical_step"""
    for participant in builder.parser.participants:
        coord = builder.participants_coordinates[participant['name']]
        options = participant['options']
        ET.SubElement(
            root,
            "line",
            {
                "stroke": options.get("linecolor") or options.get("linecolour") or "black",
                "x1": str(coord),
                "y1": str(y1),
                "x2": str(coord),
                "y2": str(y2),
                **extra_options,
                **options,
            },
        )


def get_offset_from_label_multiple_lines(label, font_size):
    """A label may have multiple lines, hence needing the arcs to be shifted downwards."""
    offset = 0
    label_lines_count = len(label.split(r"\n"))
    if label_lines_count:
        offset = label_lines_count * font_size
    return offset


def get_text_width(text, afm, font_size):
    """Returns the text length in pixels."""
    return sum(afm["unicode_to_width"][ord(c)] for c in text) * font_size / 1000


def get_text_ascender(afm, font_size):
    try:
        afm['ascender']
    except KeyError:
        pass
    return afm["ascender"] * font_size / 1000


def get_text_descender(afm, font_size):
    return abs(afm["descender"]) * font_size / 1000


def get_text_height(afm, font_size):
    return get_text_ascender(afm, font_size) + get_text_descender(afm, font_size)


def get_afm(font_afm, font):
    """ from all the AFM available, retrieve the one matching the font """
    try:
        afm = font_afm[font.lower()]
    except KeyError:
        logger.warning(f"No Adobe Font Metrics file available for font '{font}', impossible to measure the width of the labels using this font")
        afm = font_afm['helvetica']
    return afm


def draw_label(root, x1, x2, y, font, font_size, font_afm, options):
    """
    Draw the label right below the y coordinate, and in the middle of the x1, x2 coordinates.
    If there are multiple lines, expand the label downwards.
    :returns the lower vertical coordinate of the label drawn
    """
    label = options.get("label")
    if not label:
        return y
    afm = get_afm(font_afm, font)
    MARGIN_DOWN = font_size
    MARGIN_LEFT_RIGHT = 2
    scaled_ascender = get_text_ascender(afm, font_size)
    text_height = get_text_height(afm, font_size)
    g = ET.Element("g")
    # for a label right below y, need to put the cursor at y + scaled_ascender (if y grows downwards)
    y += scaled_ascender
    # shift label upward if multiline
    if x1 == x2:
        y -= text_height * len(label.split(r"\n"))
    for idx, lab in enumerate(label.split(r"\n")):  # labels may contain newline character
        # Draw Boxes
        text_width = get_text_width(lab, afm, font_size)
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
                "fill": options.get("textbgcolour") or options.get("textbgcolor") or "white",
            },
        )
        # Sometimes, the text goes beyond the SVG frame
        #max_x = float(rect.attrib["x"]) + float(rect.attrib["width"])
        #if max_x > float(root.attrib["width"]):
        #    root.attrib["width"] = str(max_x)
        # Custom font passed in the element
        if 'font-family' in options:
            # e.g. 'helvetica-bold' -> should use the 'helvetica-bold' AFM, but set the font-family of text element to 'helvetica'
            font = options['font-family'].split('-')[0]
        # Draw text inside the box
        text = ET.SubElement(
            g,
            "text",
            {
                "x": str(x),
                "y": str(y),
                "font-size": str(font_size),
                **options,
                "fill": options.get("textcolour") or options.get("textcolor") or "black",
                "font-family": font,
            },
        )
        text.text = lab
    root.append(g)
    # add the scaled descender to get the lowest vertical coordinate of the label
    y += get_text_descender(afm, font_size)
    # add the margin
    y += MARGIN_DOWN
    return y
