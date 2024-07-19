import re

from .arity2 import Arc, Box
from .arity1 import ExtraSpace, OmittedSignal, GeneralComment

REGEX_ATTRIBUTES = r"\[(.*)]"
REVERTED_ARC_TO_RECIPROCAL = {
    "<<=": "=>>",
    "<-": "->",
    "<=": "=>",
    "<<": ">>",
    "<:": ":>",
    "x-": "-x",
    "*<-": "->*",
}


class Parser:
    def __init__(self, input):
        """
        First line is either the options or the entities

        Options: (example: 'hscale="1.5", arcgradient="5";')

        * hscale = multiply the width by this number, default = 1
        * width = set the width (pixels), default = 600
        * arcgradient = number of pixels vertical difference between the start and the end of the arc
        * max-height = split image if height is larger than this: TODO
        * font-family = font (can also be set on a specific element)
        * font-size = font size (can also be set on a specific element)
        """
        self.input = re.findall(r"msc {([\s\S]*)}", input)[0]
        self.context = {
            "hscale": 1,
            "width": 600,
            "arcgradient": 0,
            "max-height": 0,
            "font-size": 12,
            "font-family": "helvetica",
        }
        self.participants = []
        self.elements = []
        self.parse()

    def __repr__(self):
        elements = ""
        for el in self.elements:
            elements += "\t" + str(el) + "\n"
        return (
            f"<DiagramBuilder>\n"
            f"Options: {self.context}\n"
            f"Participants: {self.participants}\n"
            f"Elements:\n{elements}"
        )

    @staticmethod
    def split_elements_on_line(line):
        """Split the ',' if they are not inside square brackets (e.g.: a->b [a1=1, a2=2] should not be splitted)
        Returns a list of elements
        """
        pattern = re.compile(",(?![^\[]*])")
        commas_idx = [0] + [match.end() for match in pattern.finditer(line)]
        elements = [line[i:j] for i, j in zip(commas_idx, commas_idx[1:] + [len(line)])]
        # remove leading trailing spaces, trailing ';' and ','
        return [e.rstrip(";").rstrip(",").strip(" ") for e in elements]

    @staticmethod
    def parse_options(line):
        attrs_string = re.findall(
            REGEX_ATTRIBUTES, line, re.DOTALL
        )  # DOTALL: in case a label contains "\n"
        options = {}
        if attrs_string:
            options = dict(
                re.findall('([\w-]*) ?= ?"(.*?)"', attrs_string[0], re.DOTALL)
            )
        return options

    def parse_context(self, line):
        for arg in self.context:
            val = re.findall(f'{arg} ?= ?"(.*?)"', line)
            if val:
                if arg == 'font-family':
                    self.context[arg] = val[0]
                else:
                    self.context[arg] = float(val[0])

    def parse_participants(self, line):
        """Parse the participant(s) on a given line"""
        participants = []
        line_without_options = re.sub(r"\[(.*?)\]", "", line, flags=re.DOTALL)
        for name in line_without_options.split(","):
            dirty_name = name.strip(";")
            assert (
                " " not in dirty_name.strip()
            ), f"'{dirty_name}' is not a valid participant name."
            options_match = re.findall(
                f"({dirty_name} ?\[.*?\])", line, flags=re.DOTALL
            )
            options = {}
            if options_match:
                options = self.parse_options(options_match[0])
            participants.append(
                {
                    "name": re.sub(REGEX_ATTRIBUTES, "", dirty_name).strip(),
                    "options": options,
                }
            )
        assert participants, f"Could not parse the participants on line {line}"
        self.participants = participants

    def parse_arity1(self, el):
        """Parse '|||', '---', '...' on a given line"""
        element = re.sub(REGEX_ATTRIBUTES, "", el).strip()
        options = self.parse_options(el)
        if element.startswith("|||"):
            return ExtraSpace(options=options)
        elif element.startswith("---"):
            return GeneralComment(options=options)
        elif element.startswith("..."):
            return OmittedSignal(options=options)
        else:
            raise Exception(f"Could not parse line: {el}")

    def parse_arity2(self, el):
        """Parse the arcs/boxes on a given line"""
        el_txt = re.sub(REGEX_ATTRIBUTES, "", el).strip()
        match = re.findall(
            "(\S*?) ?(=>>|<<=|->\*|\*<-|->|<-|=>|<=|<<|>>|:>|<:|-x|x-|box|rbox|abox|note) ?(\S*)",
            el_txt,
        )
        assert match, f"Could not parse arc: '{el_txt}'"
        src, dst = match[0][0], match[0][2]
        arc = match[0][1]
        if arc in REVERTED_ARC_TO_RECIPROCAL:
            src, dst = dst, src
            arc = REVERTED_ARC_TO_RECIPROCAL[arc]
        if arc in ("box", "rbox", "abox", "note"):
            return Box(src=src, element=arc, dst=dst, options=self.parse_options(el))
        else:
            return Arc(src=src, element=arc, dst=dst, options=self.parse_options(el))

    def parse(self):
        input_without_comment = re.sub(
            "\s#.*\n", "", self.input
        )  # /!\ do not remove 'a -> b [textbgcolour="#7fff7f"]'
        for line in input_without_comment.split(";"):
            # remove comment (anything from # to \n)
            line = line.strip()
            if not line:
                continue
            if not self.participants and any(
                line.strip().startswith(option) for option in self.context.keys()
            ):
                # parse options only if the line begins with a known option key
                self.parse_context(line)
            elif not self.participants:
                # parse participants once
                self.parse_participants(line)
            else:
                # parse arcs, boxes, spaces, etc
                elements = []
                for el in self.split_elements_on_line(line):
                    if (
                        el.startswith("|||")
                        or el.startswith("---")
                        or el.startswith("...")
                    ):
                        element = self.parse_arity1(el)
                    else:
                        element = self.parse_arity2(el)
                    elements.append(element)
                self.elements.append(elements)
