import xml.etree.ElementTree as ET

from . import utils


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

    def draw_arrow(self, root: ET.Element, x1, x2, y1, y2, arrow_id, color):
        # Params (:>)
        y_delta = 2
        if self.src == self.dst:
            # Special case: curved arc
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

    def draw(self, builder, root: ET.Element):
        # Arc color
        color = self.options.get('linecolour') or self.options.get('linecolor') or "black"
        arrow_id = self.get_arrow_tip_id(color)
        # Arc coordinates
        offset = utils.get_offset_from_label_multiple_lines(self.options.get('label', ''), builder.font_size)
        x1 = builder.participants_coordinates[self.src]
        y1 = builder.current_height + builder.margin + offset
        x2 = builder.participants_coordinates[self.dst]
        y2 = y1 + builder.parser.context['arcgradient']
        if self.src == self.dst and builder.parser.context['arcgradient'] < 10:
            # avoid having a squashed arc to self
            y2 += 10

        # Arrow (see https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/marker-end)
        self.draw_arrow(root, x1, x2, y1, y2, arrow_id, color)
        self.draw_arrow_tip(root, arrow_id, color)
        # Lifelines of participants
        utils.expand_lifelines(builder, root, y1=builder.current_height, y2=y2, extra_options=self.options)
        builder.current_height = y2
        # Label (last element drawn since the rendering order is based on the document order)
        utils.draw_label(root, x1, x2, y1, y2, builder.font_size, self.options, arc_to_self=self.src == self.dst)


class Box(Arity2):
    def __init__(self, src, dst, element, options):
        assert element in ('box', 'rbox', 'abox', 'note')
        super().__init__(src, dst, element, options)

    def __repr__(self):
        return f"<Box> {self.src}{self.element}{self.dst} {self.options}"

    def draw(self, builder, root: ET.Element, extra_options: dict = False):
        # TODO
        pass
