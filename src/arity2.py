import xml.etree.ElementTree as ET

from . import utils

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
    
    def get_arrow_tip_id(self, color):
        if self.element == '-x':
            form = 'lost'
        elif self.element == '=>>':
            form = 'light'
        elif self.element == '->':
            form = 'super-light'
        elif self.element == ':>':
            form = 'emphasized'
        else:
            form = 'standard'
        return f"arrow-{form}-{color}"

    def draw_arrow_tip(self, root, arrow_id, color):
        if not root.find(f'defs/marker[@id="{arrow_id}"]'):
            marker = ET.SubElement(root.find('defs'), 'marker', {
                'id': arrow_id,
                'viewBox': '0 0 10 10',  # x, y, width, height
                'refX': '10',
                'refY': '5',
                'markerWidth': '10',
                'markerHeight': '10',
                'orient': 'auto',
            })
            if self.element == '->':
                ET.SubElement(marker, 'path', {
                    'd': 'M 10 5 l -10 5',  # simple line (l: LineTo)
                    'style': f'stroke:{color}',
                })
            elif self.element == '=>>':
                ET.SubElement(marker, 'path', {
                    'd': 'M 0 0 L 10 5 L 0 10',  # same as the filled triangle, but we do not close the path at the end
                    'fill': 'none',
                    'stroke': color,
                })
            elif self.element == '-x':
                marker.attrib['refX'] = '5'
                ET.SubElement(marker, 'path', {
                    'd': 'M 0 0 L 10 10 M 0 10 L 10 0',
                    'fill': 'none',
                    'stroke': color,
                })
            else:
                ET.SubElement(marker, 'path', {
                    'd': 'M 0 0 L 10 5 L 0 10 z',  # simple triangle (M: MoveTo, L: LineTo, z: ClosePath)
                    'fill': color,
                })

    def draw_label(self, root, x1, x2, y1, y2, font_size):
        label = self.options.get('label')
        if not label:
            return
        MARGIN = 1  # margin before and after the label
        OFFSET = HELVETICA['ascender']/2 * font_size/1000  # offset above the arc
        g = ET.Element('g')
        lines_count = len(label.split('\n'))
        for idx, lab in enumerate(label.split('\n')):  # labels may contain newline character
            # Draw Boxes
            text_width = sum(HELVETICA['unicode_to_width'].get(ord(c), 0) for c in lab) * font_size / 1000
            if self.src == self.dst:
                x = x1 + OFFSET
                y = (y1 - OFFSET)
            else:
                x = min(x1, x2) + abs(x2 - x1) / 2 - text_width / 2
                y = ((y1 + y2) / 2 - OFFSET)
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
                'fill': self.options.get('textbgcolour') or self.options.get('textbgcolor') or 'white',
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

    def draw(self, builder, root: ET.Element):
        # Arc color
        color = self.options.get('linecolour') or self.options.get('linecolor') or "black"
        arrow_id = self.get_arrow_tip_id(color)
        # Arc coordinates
        x1 = builder.participants_coordinates[self.src]
        y1 = builder.current_height + builder.margin
        x2 = builder.participants_coordinates[self.dst]
        y2 = y1 + builder.parser.context['arcgradient']
        # Label may have multiple lines, hence needing the arcs to be shifted downwards
        label_lines_count = len(self.options.get('label', '').split('\n'))
        if label_lines_count:
            offset = label_lines_count * builder.font_size
            y1 += offset
            y2 += offset
        # Params (:>)
        y_delta = 2
        if self.src == self.dst:
            # Special case: curved arc
            if builder.parser.context['arcgradient'] < 10:
                y2 += 10
            arc_magnitude = 100
            ET.SubElement(root, 'path', {
                **self.options,
                'stroke': '' if self.element == ':>' else color,
                'd': f"M{x1},{y1} C{x1+arc_magnitude},{y1} {x1+arc_magnitude},{y2} {x2},{y2}",
                'fill': 'none',
                'stroke-dasharray': '5, 3' if self.element == '>>' else '',
                'marker-end': f"url(#{arrow_id})",
            })
            if self.element == ':>':
                # approach followed by mscgen: offset the 2 curves above and below the standard one
                ET.SubElement(root, 'path', {
                    **self.options,
                    'stroke': color,
                    'd': f"M{x1},{y1-y_delta} C{x1 + arc_magnitude},{y1-y_delta} {x1 + arc_magnitude},{y2-y_delta} {x2+15},{y2-y_delta}"
                         f"M{x1},{y1+y_delta} C{x1 + arc_magnitude},{y1+y_delta} {x1 + arc_magnitude},{y2+y_delta} {x2+15},{y2+y_delta}",
                    'fill': 'none',
                    'stroke-dasharray': '5, 3' if self.element == '>>' else '',
                })
        elif self.element == '-x':
            # Special case: half line arc
            ET.SubElement(root, 'line', {
                **self.options,
                'stroke': color,
                'x1': str(x1),
                'y1': str(y1),
                'x2': str(x2 + (x1-x2)*0.25),
                'y2': str(y2 + (y1-y2)*0.25),
                'marker-end': f"url(#{arrow_id})",
            })
        elif self.element == ':>':
            # Double line arc
            shorten_factor = 0.04  # both lines should be shortened, since the tip is in between
            ET.SubElement(root, 'path', {
                **self.options,
                'stroke': color,
                'd': f"M {x1} {y1+y_delta} L {x2 + (x1-x2)*shorten_factor} {y2+y_delta + (y1-y2)*shorten_factor} "
                     f"M {x1} {y1-y_delta} L {x2 + (x1-x2)*shorten_factor} {y2-y_delta + (y1-y2)*shorten_factor}",
            })
            # invisible vertex, on which the marker is drawn
            ET.SubElement(root, 'path', {
                **self.options,
                'stroke': '',
                'd': f"M {x1} {y1} L {x2} {y2}",
                'marker-end': f"url(#{arrow_id})",
            })
        else:
            # Standard line arc
            ET.SubElement(root, 'line', {
                **self.options,
                'stroke': color,
                'x1': str(x1),
                'y1': str(y1),
                'x2': str(x2),
                'y2': str(y2),
                'marker-end': f"url(#{arrow_id})",
                'stroke-dasharray': '5, 3' if self.element == '>>' else '',
            })
        # Arrow (see https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/marker-end)
        self.draw_arrow_tip(root, arrow_id, color)
        # Lifelines of participants
        utils.expand_lifelines(builder, root, y1=builder.current_height, y2=y2, extra_options=self.options)
        builder.current_height = y2
        # Label (last element drawn since the rendering order is based on the document order)
        self.draw_label(root, x1, x2, y1, y2, builder.font_size)


class Box(Arity2):
    def __init__(self, src, dst, element, options):
        assert element in ('box', 'rbox', 'abox', 'note')
        super().__init__(src, dst, element, options)

    def __repr__(self):
        return f"<Box> {self.src}{self.element}{self.dst} {self.options}"

    def draw(self, builder, root: ET.Element, extra_options: dict = False):
        # TODO
        pass
