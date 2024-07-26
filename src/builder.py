import xml.etree.ElementTree as ET

from . import utils


class Builder:
    def __init__(self, parser, css_content=False):
        self.parser = parser
        self.participants_coordinates = {}
        self.vertical_step = 28 + self.parser.context["arcgradient"]  # margin after drawing any element
        self.margin = self.vertical_step / 2  # margin before drawing any element
        self.current_height = 0
        self.width = self.parser.context["width"] * self.parser.context["hscale"]
        self.font_size = self.parser.context["font-size"]
        self.font = self.parser.context['font']
        self.font_afm = utils.parse_afm_files()
        self.defs = ET.Element("defs")
        self.css_content = css_content

    def draw_participants(self, root):
        """Draw participants (on top of the image)"""
        self.current_height = self.font_size
        g = ET.SubElement(root, "g", {'class': "participants"})
        relative_position = float(self.width) / (2 * len(self.parser.participants))
        x = relative_position
        y2_list = []
        for entity in self.parser.participants:
            self.participants_coordinates[entity["name"]] = x
            if not entity["options"].get("label"):
                entity["options"]["label"] = entity["name"]
            font_size = float(entity["options"].get("font-size", self.font_size))
            y2 = utils.draw_label(
                g, x - 1, x + 1, self.current_height, self.font, font_size, self.font_afm, entity["options"]
            )
            y2_list.append(y2)
            x += 2 * relative_position
        self.current_height = min(y2_list)

    def draw_line(self, root, line, idx):
        g = ET.SubElement(root, "g", {'class': "line", 'id': f"line-{idx}"})
        g_lifelines = ET.SubElement(g, "g", {'class': "lifelines"})
        g_elements = ET.SubElement(g, "g", {'class': "element"})
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
        utils.expand_lifelines(self, g_lifelines, y1=self.current_height, y2=max(y2_list), extra_options=extra_options)
        g.attrib['y1'] = str(self.current_height)
        self.current_height = max(y2_list)
        g.attrib['y2'] = str(self.current_height)
        return g

    def initialize_root(self):
        root = ET.Element(
            "svg",
            {
                "version": "1.1",
                "width": str(self.width),
                "xmlns": "http://www.w3.org/2000/svg",
            },
        )
        ET.SubElement(root, "defs")
        return root

    def generate(self):
        """ Returns a list of bytes which are the output SVG diagrams """
        svgs = []
        while self.parser.elements:
            self.current_height = 0
            root = self.initialize_root()
            self.draw_participants(root)
            idx = 0
            while self.parser.elements:
                idx += 1
                line = self.parser.elements.pop(0)
                g = self.draw_line(root, line, idx)
                if (
                    self.parser.context['max-height']
                    and float(g.attrib['y2']) + 2 * self.margin > self.parser.context['max-height']
                ):
                    # If the max-height has been exceeded, need to remove the last element drawn and finish drawing
                    # the current SVG. Then, draw one or several new SVGs with the remaining elements.
                    self.current_height = float(g.attrib['y1'])
                    root.remove(g)
                    self.parser.elements = [line] + self.parser.elements
                    break
            # add the defs to the root
            for marker in self.defs:
                root.find('defs').append(marker)
            # add a bottom margin
            y1 = self.current_height
            y2 = self.current_height + self.margin
            g = ET.SubElement(root, "g", {'class': "lifelines", 'y1': str(y1), 'y2': str(y2)})
            utils.expand_lifelines(self, g, y1=y1, y2=y2, extra_options={})
            # set height
            root.attrib["height"] = str(self.current_height + 2 * self.margin)
            # indent
            tree = ET.ElementTree(root)
            ET.indent(tree, space="\t", level=0)
            svg = ET.tostring(root, encoding="UTF-8")
            extra_content = f"""<style>\n\t\t<![CDATA[\n{self.css_content}\n]]>\n\t</style>\n\t""".encode()
            svg = svg.replace(b"<defs>", extra_content + b"<defs>")
            svgs.append(svg)

        return svgs
