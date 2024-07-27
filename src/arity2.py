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
        assert element in (
            "->",
            "=>",
            ">>",
            "=>>",
            ":>",
            "-x",
            "->*",
        ), f"Unsupported type: {element}"
        super().__init__(src, dst, element, options)

    def __repr__(self):
        return f"<Arc> {self.src}{self.element}{self.dst} {self.options}"

    def get_arrow_tip_id(self, color):
        if self.element == "-x":
            form = "lost"
        elif self.element == "=>>":
            form = "light"
        elif self.element == "->":
            form = "super-light"
        elif self.element == ":>":
            form = "emphasized"
        else:
            form = "standard"
        return f"arrow-{form}-{color}"

    def draw_arrow_tip(self, builder, arrow_id, color):
        if not builder.defs.find(f'marker[@id="{arrow_id}"]'):
            # TODO: pass the defs elements
            marker = ET.SubElement(
                builder.defs,
                "marker",
                {
                    "id": arrow_id,
                    "viewBox": "0 0 10 10",  # x, y, width, height
                    "refX": "10",
                    "refY": "5",
                    "markerWidth": "10",
                    "markerHeight": "10",
                    "orient": "auto",
                },
            )
            if self.element == "->":
                ET.SubElement(
                    marker,
                    "path",
                    {
                        "d": "M 10 5 l -10 5",  # simple line (l: LineTo)
                        "stroke": color,
                    },
                )
            elif self.element == "=>>":
                ET.SubElement(
                    marker,
                    "path",
                    {
                        "d": "M 0 0 L 10 5 L 0 10",  # same as the filled triangle, but we do not close the path at the end
                        "fill": "none",
                        "stroke": color,
                    },
                )
            elif self.element == "-x":
                marker.attrib["refX"] = "5"
                ET.SubElement(
                    marker,
                    "path",
                    {
                        "d": "M 0 0 L 10 10 M 0 10 L 10 0",
                        "fill": "none",
                        "stroke": color,
                    },
                )
            else:
                ET.SubElement(
                    marker,
                    "path",
                    {
                        "d": "M 0 0 L 10 5 L 0 10 z",  # simple triangle (M: MoveTo, L: LineTo, z: ClosePath)
                        "fill": color,
                    },
                )

    def draw_arrow(self, root: ET.Element, x1, x2, y1, y2, arrow_id, color):
        # Params (:>)
        y_delta = 2
        if self.src == self.dst:
            # Special case: curved arc
            arc_magnitude = 100
            ET.SubElement(
                root,
                "path",
                {
                    "stroke": "" if self.element == ":>" else color,
                    "d": f"M{x1},{y1} C{x1+arc_magnitude},{y1} {x1+arc_magnitude},{y2} {x2},{y2}",
                    "fill": "none",
                    "stroke-dasharray": "5, 3" if self.element == ">>" else "",
                    "marker-end": f"url(#{arrow_id})",
                    **self.options,
                },
            )
            if self.element == ":>":
                # approach followed by mscgen: offset the 2 curves above and below the standard one
                ET.SubElement(
                    root,
                    "path",
                    {
                        "stroke": color,
                        "d": f"M{x1},{y1-y_delta} C{x1 + arc_magnitude},{y1-y_delta} {x1 + arc_magnitude},{y2-y_delta} {x2+15},{y2-y_delta}"
                        f"M{x1},{y1+y_delta} C{x1 + arc_magnitude},{y1+y_delta} {x1 + arc_magnitude},{y2+y_delta} {x2+15},{y2+y_delta}",
                        "fill": "none",
                        "stroke-dasharray": "5, 3" if self.element == ">>" else "",
                        **self.options,
                    },
                )
        elif self.element == "-x":
            # Special case: half line arc
            ET.SubElement(
                root,
                "line",
                {
                    "stroke": color,
                    "x1": str(x1),
                    "y1": str(y1),
                    "x2": str(x2 + (x1 - x2) * 0.25),
                    "y2": str(y2 + (y1 - y2) * 0.25),
                    "marker-end": f"url(#{arrow_id})",
                    **self.options,
                },
            )
        elif self.element == ":>":
            # Double line arc
            shorten_factor = (
                0.04  # both lines should be shortened, since the tip is in between
            )
            ET.SubElement(
                root,
                "path",
                {
                    "stroke": color,
                    "d": f"M {x1} {y1+y_delta} L {x2 + (x1-x2)*shorten_factor} {y2+y_delta + (y1-y2)*shorten_factor} "
                    f"M {x1} {y1-y_delta} L {x2 + (x1-x2)*shorten_factor} {y2-y_delta + (y1-y2)*shorten_factor}",
                    **self.options,
                },
            )
            # invisible vertex, on which the marker is drawn
            ET.SubElement(
                root,
                "path",
                {
                    "stroke": "",
                    "d": f"M {x1} {y1} L {x2} {y2}",
                    "marker-end": f"url(#{arrow_id})",
                    **self.options,
                },
            )
        else:
            # Standard line arc
            ET.SubElement(
                root,
                "line",
                {
                    "stroke": color,
                    "x1": str(x1),
                    "y1": str(y1),
                    "x2": str(x2),
                    "y2": str(y2),
                    "marker-end": f"url(#{arrow_id})",
                    "stroke-dasharray": "5, 3" if self.element == ">>" else "",
                    **self.options,
                },
            )

    def draw(self, builder, root: ET.Element, y=0):
        """ y is the coordinate at which we start drawing the arc """
        if self.element == "->*":
            # broadcast: equivalent to simple arcs to every other participant
            participants = list(builder.participants_coordinates.keys())
            participants.remove(self.src)
            y2_list = []
            extra_options = {}
            self.options["ignore_label"] = "1"
            for dst in participants:
                y2, options = Arc(self.src, dst, "->", self.options).draw(builder, root)
                y2_list.append(y2)
                extra_options.update(**(options or {}))
            # draw label, centered around the whole graph
            x1 = min(builder.participants_coordinates.values())
            x2 = max(builder.participants_coordinates.values())
            y += builder.font_size * 2.3
            utils.draw_label(root, x1, x2, y, builder.font, builder.font_size, builder.font_afm, self.options)
            return max(y2_list), extra_options

        # Arc color
        color = self.options.get("linecolour") or self.options.get("linecolor") or "black"
        arrow_id = self.get_arrow_tip_id(color)
        # Arc coordinates
        font = self.options.get('font-family', builder.font)
        afm = utils.get_afm(builder.font_afm, font)
        label = self.options.get("label", "")
        offset = utils.get_offset_from_label_multiple_lines(label, afm, builder.font_size)
        x1 = builder.participants_coordinates[self.src]
        y1 = y + offset
        if self.src == self.dst:
            # the arc from self should start *after* the label
            y1 += offset + builder.margin/2
        x2 = builder.participants_coordinates[self.dst]
        y2 = y1 + builder.parser.context["arcgradient"] * (float(self.options.get("arcskip", "0")) + 1)
        if self.src == self.dst and builder.parser.context["arcgradient"] < 10:
            # avoid having a squashed arc to self
            y2 += 10

        # Arrow (see https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/marker-end)
        self.draw_arrow(root, x1, x2, y1, y2, arrow_id, color)
        self.draw_arrow_tip(builder, arrow_id, color)

        # Label (last element drawn since the rendering order is based on the document order)
        font = self.options.get('font-family', builder.font)
        if not self.options.get("ignore_label"):
            if x1 != x2:
                y = (y1 + y2)/2 - offset
            y2 = max(
                utils.draw_label(root, x1, x2, y, font, builder.font_size, builder.font_afm, self.options),
                y2,
            )
        return y2, {}


class Box(Arity2):
    def __init__(self, src, dst, element, options):
        assert element in ("box", "rbox", "abox", "note")
        super().__init__(src, dst, element, options)

    def __repr__(self):
        return f"<Box> {self.src} {self.element} {self.dst} {self.options}"

    def draw(self, builder, root: ET.Element, extra_options: dict = False, y=0):
        """ y is the coordinate at which we start drawing the box (no margin is added) """
        y1 = y
        space_per_participant = float(builder.width) / len(builder.participants_coordinates.keys())
        x1 = builder.participants_coordinates[self.src] - space_per_participant * 0.4
        x2 = builder.participants_coordinates[self.dst] + space_per_participant * 0.4

        border_color = self.options.get("bordercolour") or self.options.get("bordercolor") or "black"
        background_color = self.options.get("textbgcolour") or self.options.get("textbgcolor") or "white"
        if self.element in ("box", "rbox"):
            rectangle = ET.SubElement(
                root,
                "rect",
                {
                    "x": str(x1),
                    "y": str(y1),
                    "width": str(x2 - x1),
                    "rx": "5" if self.element == "rbox" else "0",
                    "ry": "5" if self.element == "rbox" else "0",
                    **self.options,
                    "stroke": border_color,
                    "fill": background_color,
                },
            )
        else:
            rectangle = ET.SubElement(
                root,
                "path",
                {
                    **self.options,
                    "stroke": border_color,
                    "fill": background_color,
                },
            )
        # draw label
        MARGIN_TOP_BOTTOM = builder.font_size/2  # Margin between text and box borders
        font = self.options.get('font-family', builder.font)
        y2 = utils.draw_label(
            root, x1, x2, y1 + MARGIN_TOP_BOTTOM, font, builder.font_size, builder.font_afm, self.options
        )
        y2 += MARGIN_TOP_BOTTOM
        # update the rectangle based on the lower vertical coordinate
        if self.element in ("box", "rbox"):
            rectangle.attrib["height"] = str(y2 - y1)
        elif self.element == "abox":
            alpha = 5  # height of the lateral triangles
            rectangle.attrib["d"] = (
                f"M {x1},{y1} L {x2},{y1} L {x2 + alpha},{y1 + (y2 - y1)/2}"
                f"L {x2},{y2} L {x1},{y2} L {x1 - alpha},{y1 + (y2 - y1)/2} z"
            )
        else:
            # note
            alpha = 10  # amplitude of the upper right corner
            rectangle.attrib["d"] = (
                f"M {x1},{y1} L {x2 - alpha},{y1} L {x2 - alpha},{y1 + alpha}"
                f"L {x2},{y1 + alpha} M {x2 - alpha}, {y1} L {x2}, {y1 + alpha}"
                f"L {x2},{y2} L {x1},{y2} L {x1},{y1}"
            )
        return y2, extra_options
