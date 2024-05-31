import xml.etree.ElementTree as ET

import src.utils as utils


class Arity1:
    def __init__(self, element, options):
        assert element in ('...', '---', '|||')
        self.type = element
        self.options = options
        self._name = "Arity1"

    def __repr__(self):
        return f"<{self._name}> {self.options}"

    def draw(self, builder, root: ET.Element, extra_options: dict = False):
        utils.expand_lifelines(builder, root, extra_options or {})
        builder.current_height += builder.vertical_step


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

