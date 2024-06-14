import xml.etree.ElementTree as ET

from . import utils


class Arity1:
    def __init__(self, options):
        self.options = options
        self._name = "Arity1"

    def __repr__(self):
        return f"<{self._name}> {self.options}"

    def draw(self, builder, root: ET.Element, extra_options: dict = False):
        # Expand lifelines: margin
        offset = utils.get_offset_from_label_multiple_lines(self.options.get('label', ''), builder.font_size)
        y1 = builder.current_height + offset
        y2 = y1 + builder.margin
        utils.expand_lifelines(builder, root, y1=builder.current_height, y2=y2, extra_options={})
        builder.current_height = y2
        # Expand lifelines: element
        y1 = builder.current_height
        y2 = y1 + builder.vertical_step
        # Label
        x1 = min(builder.participants_coordinates.values())
        x2 = max(builder.participants_coordinates.values())
        y = y1 + (y2 - y1)/2
        y_offset_factor = -1 if self._name in ("ExtraSpace", "OmittedSignal") else 1
        utils.draw_label(root, x1, x2, y, y, builder.font_size, self.options, y_offset_factor=y_offset_factor)
        return y2


class ExtraSpace(Arity1):
    def __init__(self, options):
        """ ||| """
        super().__init__(options)
        self._name = 'ExtraSpace'


class GeneralComment(Arity1):
    def __init__(self, options):
        """ --- """
        super().__init__(options)
        self._name = 'GeneralComment'

    def draw(self, builder, root: ET.Element, extra_options: dict = False):
        offset = utils.get_offset_from_label_multiple_lines(self.options.get('label', ''), builder.font_size)
        y1 = builder.current_height + builder.margin + offset
        y2 = y1 + builder.vertical_step
        y = (y1 + y2)/2
        x1 = min(builder.participants_coordinates.values()) * 0.5
        x2 = x1 + max(builder.participants_coordinates.values())
        color = self.options.get('linecolour') or self.options.get('linecolor') or "black"
        ET.SubElement(root, 'line', {
            **self.options,
            'stroke': color,
            'x1': str(x1),
            'y1': str(y),
            'x2': str(x2),
            'y2': str(y),
            'stroke-dasharray': '5, 3',
        })
        return super().draw(builder, root, extra_options)


class OmittedSignal(Arity1):
    def __init__(self, options):
        """ ... """
        super().__init__(options)
        self._name = 'OmittedSignal'

    def draw(self, builder, root: ET.Element, extra_options: dict = False):
        return super().draw(builder, root, {'stroke-dasharray': str(2)})

