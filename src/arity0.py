import xml.etree.ElementTree as ET

from . import utils


class Arity0:
    def __init__(self, options):
        self.options = options
        self._name = "Arity0"

    def __repr__(self):
        return f"<{self._name}> {self.options}"

    def draw(self, builder, root: ET.Element, extra_options: dict = False, y=0):
        root.attrib['class'] = "lifelines"
        x1 = min(builder.participants_coordinates.values())
        x2 = max(builder.participants_coordinates.values())
        g = ET.SubElement(root, "g")
        font = self.options.get('font-family', builder.font)
        afm = utils.get_afm(builder.font_afm, font)
        label = self.options.get("label", "")
        offset = utils.get_offset_from_label_multiple_lines(label, afm, builder.font_size)
        y1 = y + offset
        y2 = y1 + builder.margin * 2
        y_label = (y1 + y2)/2 - offset
        y2_label = utils.draw_label(
            root, x1, x2, y_label, font, builder.font_size, builder.font_afm, self.options
        )
        if self._name == "GeneralComment":
            y = (y1 + y2)/2
            color = self.options.get("linecolour") or self.options.get("linecolor") or "black"
            ET.SubElement(
                g,
                "line",
                {
                    **self.options,
                    "stroke": color,
                    "x1": str(min(builder.participants_coordinates.values())),
                    "y1": str(y),
                    "x2": str(max(builder.participants_coordinates.values())),
                    "y2": str(y),
                    "stroke-dasharray": "5, 3",
                },
            )
        self.options.update(**(extra_options or {}))
        return max(y2, y2_label), self.options


class ExtraSpace(Arity0):
    def __init__(self, options):
        """|||"""
        super().__init__(options)
        self._name = "ExtraSpace"


class GeneralComment(Arity0):
    def __init__(self, options):
        """---"""
        super().__init__(options)
        self._name = "GeneralComment"


class OmittedSignal(Arity0):
    def __init__(self, options):
        """..."""
        super().__init__(options)
        self._name = "OmittedSignal"

    def draw(self, builder, root: ET.Element, extra_options: dict = False, y=0):
        return super().draw(builder, root, {"stroke-dasharray": str(2)}, y)
