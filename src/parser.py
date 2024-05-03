import re

from src.arity2 import Arc, Box
from src.arity1 import ExtraSpace, OmittedSignal, GeneralComment

REGEX_ATTRIBUTES = r'\[(.*)]'
ATTRS = (
    'label',
    'URL',
    'ID',
    'IDURL',
    'arcskip',
    ('linecolour', 'linecolor'),
    ('textbgcolour', 'textbgcolor'),
    ('arclinecolour', 'arclinecolor'),
    ('arctextcolour', 'arctextcolor'),
    ('arctextbgcolour', 'arctextbgcolor'),
)


class Parser:
    def __init__(self, input):
        """
        First line is either the options or the entities

        Options: (example: 'hscale="1.5", arcgradient="5";')

        * hscale = multiply the width by this number, default = 1
        * width = set the width (pixels), default = 600
        * arcgradient = number of pixels vertical difference between the start and the end of the arc
        * wordwraparcs = TODO
        """
        self.input = re.findall(r'msc {([\s\S]*)}', input)[0]
        self.context = {
            'hscale': 1,
            'width': 600,
            'arcgradient': 0,
        }
        self.participants = []
        self.elements = []
        self.parse()

    def __repr__(self):
        elements = ""
        for el in self.elements:
            elements += "\t" + str(el) + "\n"
        return f"<DiagramBuilder>\n" \
               f"Options: {self.context}\n" \
               f"Participants: {self.participants}\n" \
               f"Elements:\n{elements}"

    @staticmethod
    def split_elements_on_line(line):
        """ Split the ',' if they are not inside square brackets (e.g.: a->b [a1=1, a2=2] should not be splitted)
        Returns a list of elements
        """
        pattern = re.compile(",(?![^\[]*])")
        commas_idx = [0] + [match.end() for match in pattern.finditer(line)]
        elements = [line[i:j] for i, j in zip(commas_idx, commas_idx[1:]+[len(line)])]
        # remove leading trailing spaces, trailing ';' and ','
        return [e.rstrip(';').rstrip(',').strip(' ') for e in elements]

    @staticmethod
    def parse_options(line):
        attrs_string = re.findall(REGEX_ATTRIBUTES, line)
        options = {}
        if attrs_string:
            for attr in ATTRS:
                if isinstance(attr, tuple):
                    attr_re = '(' + '|'.join(attr) + ')'
                    val = re.findall(f'{attr_re} ?= ?"(.*?)"', attrs_string[0])
                    if val:
                        options[val[0][0]] = val[0][1]
                else:
                    val = re.findall(f'{attr} ?= ?"(.*?)"', attrs_string[0])
                    if val:
                        options[attr] = val[0]
        return options

    def parse_context(self, line):
        for arg in self.context:
            val = re.findall(f'{arg} ?= ?"(.*?)"', line)
            if val:
                self.context[arg] = float(val[0])

    def parse_participants(self, line):
        """ Parse the participant(s) on a given line """
        participants = []
        for name in line.split(','):
            dirty_name = name.strip(';')
            participants.append({
                'name': re.sub(REGEX_ATTRIBUTES, '', dirty_name).strip(),
                'options': self.parse_options(dirty_name),
            })
        assert participants, f"Could not parse the participants on line {line}"
        self.participants = participants

    def parse_arity1(self, line):
        """ Parse '|||', '---', '...' on a given line """
        elements = []
        for el in self.split_elements_on_line(line):
            element = re.sub(REGEX_ATTRIBUTES, '', el).strip()
            options = self.parse_options(el)
            if element == '|||':
                elements.append(ExtraSpace(element=element, options=options))
            elif element == '---':
                elements.append(GeneralComment(element=element, options=options))
            elif element == '...':
                elements.append(OmittedSignal(element=element, options=options))
            else:
                raise Exception(f"Could not parse line: {line}")
        self.elements.append(elements)

    def parse_arcs(self, line):
        """ Parse the arc(s) on a given line """
        reverted_arc_to_reciprocal = {
            '<<=': '=>>',
            '<-': '->',
            '<=': '=>',
            '<<': '>>',
            '<:': ':>',
            'x-': '-x',
        }
        arcs = []
        for el in self.split_elements_on_line(line):
            el_txt = re.sub(REGEX_ATTRIBUTES, '', el).strip()
            match = re.findall("(\S*?) ?(=>>|<<=|->|<-|=>|<=|<<|>>|:>|<:|-x|x-|->\*|\*<-) ?(\S*)", el_txt)
            assert match, f"Could not parse arc: '{el_txt}'"
            src, dst = match[0][0], match[0][2]
            arc = match[0][1]
            if arc in reverted_arc_to_reciprocal:
                src, dst = dst, src
                arc = reverted_arc_to_reciprocal[arc]
            arcs.append(Arc(src=src, element=arc, dst=dst, options=self.parse_options(el)))
        self.elements.append(arcs)
        
    def parse(self):
        for line in self.input.split(';'):
            # remove comment (anything from # to \n)
            line = re.sub('#.*\n', '', line).strip()
            if not line:
                continue
            if not self.participants and any(line.strip().startswith(option) for option in self.context.keys()):
                # parse options only if the line begins with a known option key
                self.parse_context(line)
            elif not self.participants:
                # parse participants once
                self.parse_participants(line)
            elif line.startswith('|||') or line.startswith('---') or line.startswith('...'):
                self.parse_arity1(line)
            else:
                # parse arcs
                self.parse_arcs(line)
