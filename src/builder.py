import xml.etree.ElementTree as ET

from . import utils


class Builder:
    def __init__(self, parser):
        self.parser = parser
        self.participants_coordinates = {}
        self.vertical_step = (
            28 + self.parser.context["arcgradient"]
        )  # margin after drawing any element
        self.margin = self.vertical_step / 2  # margin before drawing any element
        self.stylesheets = []
        self.current_height = 0
        self.width = self.parser.context["width"] * self.parser.context["hscale"]
        self.font_size = self.parser.context["font-size"]
        self.font = self.parser.context['font']
        self.font_afm = utils.parse_afm_files()
        self.defs = ET.Element("defs")

    def draw_participants(self, root, height):
        """Draw participants (on top of the image)"""
        relative_position = float(self.width) / (2 * len(self.parser.participants))
        x = relative_position
        y2_list = []
        for entity in self.parser.participants:
            self.participants_coordinates[entity["name"]] = x
            if not entity["options"].get("label"):
                entity["options"]["label"] = entity["name"]
            font_size = float(entity["options"].get("font-size", self.font_size))
            y2 = utils.draw_label(
                root, x - 1, x + 1, height, self.font, font_size, self.font_afm, entity["options"]
            )
            y2_list.append(y2)
            x += 2 * relative_position
        return min(y2_list)

    def generate(self):
        root = ET.Element(
            "svg",
            {
                "version": "1.1",
                "width": str(self.width),
                "xmlns": "http://www.w3.org/2000/svg",
            },
        )
        ET.SubElement(root, "defs")

        self.current_height = self.font_size
        y2 = self.draw_participants(root, self.current_height)
        self.current_height = y2
        for line in self.parser.elements:
            g = ET.SubElement(root, "g")
            g_elements = ET.SubElement(root, "g")
            # draw all the elements on the line
            y2_list = []
            extra_options = {}
            for element in line:
                y2, options = element.draw(builder=self, root=g_elements)
                assert isinstance(
                    y2, float
                ), "The 'draw' method should return a tuple (float, dict)"
                y2_list.append(y2)
                extra_options.update(**(options or {}))
            # expand the participants lifelines using the maximum y2 coordinate
            utils.expand_lifelines(
                self,
                g,
                y1=self.current_height,
                y2=max(y2_list),
                extra_options=extra_options,
            )
            self.current_height = max(y2_list)

        # add the defs to the root
        for marker in self.defs:
            root.find('defs').append(marker)

        # add a bottom margin
        y2 = self.current_height + self.margin
        utils.expand_lifelines(
            self, root, y1=self.current_height, y2=y2, extra_options={}
        )
        # set height
        root.attrib["height"] = str(self.current_height + self.vertical_step)
        # indent
        tree = ET.ElementTree(root)
        ET.indent(tree, space="\t", level=0)
        return ET.tostring(root, encoding="UTF-8")
