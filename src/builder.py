import xml.etree.ElementTree as ET

from . import utils


class Builder:
    def __init__(self, parser, css_content=False):
        self.parser = parser
        self.participants_coordinates = {}
        self.margin = 10  # margin before drawing any element
        self.current_height = 0
        self.width = self.parser.context["width"] * self.parser.context["hscale"]
        self.font_size = self.parser.context["font-size"]
        self.font = self.parser.context['font']
        self.font_afm = utils.parse_afm_files()
        self.defs = ET.Element("defs")
        self.css_content = css_content

    def draw_participant(self, root, participant, x, y=0):
        """ Draw a single participant, y being the coordinate to draw the label to
        Returns the lowest y coordinate
        """
        self.participants_coordinates[participant["name"]] = x
        if not participant["options"].get("label"):
            participant["options"]["label"] = participant["name"]
        font_size = float(participant["options"].get("font-size", self.font_size))
        font = participant["options"].get("font-family", self.font)
        y2 = utils.draw_label(
            root, x - 1, x + 1, y, font, font_size, self.font_afm, participant["options"]
        )
        return y2

    def draw_participants(self, root):
        """ Draw all participants """
        self.current_height = self.font_size
        g = ET.SubElement(root, "g", {'class': "participants"})
        relative_position = float(self.width) / (2 * len(self.parser.participants))
        x = relative_position
        heights = [self.draw_participant(ET.Element('tmp'), p, x) for p in self.parser.participants]
        actual_y2_list = []
        for participant, height in zip(self.parser.participants, heights):
            ET.SubElement(g, "rect", {
                'x': str(x - relative_position/2),
                'y': str(self.current_height - self.margin/2),
                'width': str(relative_position),
                'height': str(max(heights) + self.margin),
                'stroke': participant['options'].get('linecolour') or participant['options'].get('linecolor') or 'black',
                'fill': participant['options'].get('textbgcolor') or participant['options'].get('textbgcolour') or 'white',
                'class': participant['name'],
                **participant['options'],
            })
            y2 = self.draw_participant(g, participant, x, self.current_height + (max(heights)-height)/2)
            actual_y2_list.append(y2)
            x += 2 * relative_position
        self.current_height = max(actual_y2_list) + self.margin/2

    def draw_line(self, root, line, idx):
        g = ET.SubElement(root, "g", {'class': "line", 'id': f"line-{idx}"})
        g_lifelines = ET.SubElement(g, "g", {'class': "lifelines"})
        g_elements = ET.SubElement(g, "g", {'class': "elements"})
        # draw all the elements on the line
        y2_list = []
        extra_options = {}
        # get the height of each element on the line, so we can center the elements on a given line
        heights = [el.draw(builder=self, root=ET.Element("g"), y=0)[0] for el in line]
        for element, height in zip(line, heights):
            y2, options = element.draw(builder=self, root=g_elements, y=self.current_height + (max(heights) - height)/2)
            assert isinstance(
                y2, float
            ), "The 'draw' method should return a tuple (float, dict)"
            y2_list.append(y2)
            extra_options.update(**(options or {}))
        # expand lifelines until the end of the greater element
        utils.expand_lifelines(self, g_lifelines, y1=self.current_height, y2=max(y2_list), extra_options=extra_options)
        # add a margin between the lines
        y2_final = max(y2_list) + self.margin
        # expand lifelines after add a small margin
        utils.expand_lifelines(self, g_lifelines, y1=max(y2_list), y2=y2_final, extra_options={})
        g.attrib['y1'] = str(self.current_height)
        self.current_height = y2_final
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

    def add_empty_margin(self, root, margin):
        g = ET.SubElement(root, "g", {
            'class': "line",
            'id': "line-0",
            'y1': str(self.current_height),
            'y2': str(self.current_height + margin),
        })
        g = ET.SubElement(g, "g", {
            'class': "lifelines",
        })
        utils.expand_lifelines(self, g, self.current_height, self.current_height + margin, {})
        self.current_height += margin

    def generate(self):
        """ Returns a list of bytes which are the output SVG diagrams """
        svgs = []
        max_height = self.parser.context['max-height']
        while self.parser.lines:
            self.current_height = 0
            root = self.initialize_root()
            self.draw_participants(root)
            self.add_empty_margin(root, self.margin)
            idx = 0
            while self.parser.lines:
                idx += 1
                line = self.parser.lines.pop(0)
                g = self.draw_line(root, line, idx)
                if max_height and float(g.attrib['y2']) + self.margin > max_height:
                    # If the max-height has been exceeded, need to remove the last element drawn and finish drawing
                    # the current SVG. Then, draw one or several new SVGs with the remaining elements.
                    self.current_height = float(g.attrib['y1'])
                    root.remove(g)
                    self.parser.lines = [line] + self.parser.lines
                    if idx == 1:
                        raise utils.InvalidInputException(f"The max-height '{max_height}' is insufficient for the diagram to be drawn.")
                    break
            # add the defs to the root
            for marker in self.defs:
                root.find('defs').append(marker)
            # set height
            root.attrib["height"] = str(self.current_height + self.margin)
            # indent
            tree = ET.ElementTree(root)
            if hasattr(ET, 'indent'):  # not 'indent' attribute in python 3.8 or lower
                ET.indent(tree, space="\t", level=0)
            svg = ET.tostring(root, encoding="UTF-8")
            extra_content = f"""<style>\n\t\t<![CDATA[\n{self.css_content}\n]]>\n\t</style>\n\t""".encode()
            svg = svg.replace(b"<defs>", extra_content + b"<defs>")
            svgs.append(svg)

        return svgs
