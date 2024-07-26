import xml.etree.ElementTree as ET

from . import utils


class Arity0:
    def __init__(self, options):
        self.options = options
        self._name = "Arity0"

    def __repr__(self):
        return f"<{self._name}> {self.options}"

    def draw(self, builder, root: ET.Element, extra_options: dict = False):
        root.attrib['class'] = "lifelines"
        # Expand lifelines: margin
        y2 = builder.current_height + builder.margin + builder.font_size
        utils.expand_lifelines(
            builder, root, y1=builder.current_height, y2=y2, extra_options=self.options
        )
        builder.current_height = y2
        # Expand lifelines: element
        y1 = builder.current_height
        y2 = y1 + builder.vertical_step
        # Label
        x1 = min(builder.participants_coordinates.values())
        x2 = max(builder.participants_coordinates.values())
        g = ET.SubElement(root, "g")
        font = self.options.get('font-family', builder.font)
        if self._name in ("OmittedSignal", "ExtraSpace"):
            y_label = (y1 + y2)/2 + builder.font_size/2
        else:
            y_label = (y1 + y2)/2 - builder.font_size
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
        return max(y2, y2_label), extra_options


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

    def draw(self, builder, root: ET.Element, extra_options: dict = False):
        return super().draw(builder, root, extra_options)


class OmittedSignal(Arity0):
    def __init__(self, options):
        """..."""
        super().__init__(options)
        self._name = "OmittedSignal"

    def draw(self, builder, root: ET.Element, extra_options: dict = False):
        return super().draw(builder, root, {"stroke-dasharray": str(2)})
