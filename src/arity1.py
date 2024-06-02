import xml.etree.ElementTree as ET

from . import utils


class Arity1:
    def __init__(self, element, options):
        assert element in ('...', '---', '|||')
        self.type = element
        self.options = options
        self._name = "Arity1"

    def __repr__(self):
        return f"<{self._name}> {self.options}"

    def draw(self, builder, root: ET.Element, extra_options: dict = False):
        # TODO: draw labels as well !
        # Expand lifelines: margin
        y1 = builder.current_height
        builder.current_height = y1 + builder.margin
        utils.expand_lifelines(builder, root, y1=y1, y2=builder.current_height, extra_options={})
        # Expand lifelines: element
        y1 = builder.current_height
        builder.current_height = y1 + builder.vertical_step
        utils.expand_lifelines(builder, root, y1=y1, y2=builder.current_height, extra_options=extra_options or {})


class ExtraSpace(Arity1):
    def __init__(self, element, options):
        assert element == '|||'
        super().__init__(element, options)
        self._name = 'ExtraSpace'


class GeneralComment(Arity1):
    def __init__(self, element, options):
        assert element == '---'
        super().__init__(element, options)
        self._name = 'GeneralComment'

    def draw(self, builder, root: ET.Element, extra_options: dict = False):
        super().draw(builder, root, extra_options or {'stroke-dasharray': str(2)})


class OmittedSignal(Arity1):
    def __init__(self, element, options):
        assert element == '...'
        super().__init__(element, options)
        self._name = 'OmittedSignal'

    def draw(self, builder, root: ET.Element, extra_options: dict = False):
        super().draw(builder, root, extra_options or {'stroke-dasharray': str(2)})

