import re

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


class Parser():
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
        self.entities = []
        self.arcs = []
        self.parse()

    def __str__(self):
        arcs = ""
        for line in self.arcs:
            arcs += "\t" + str(line) + "\n"
        return f"<DiagramBuilder>\n" \
               f"Options: {self.context}\n" \
               f"Entities: {self.entities}\n" \
               f"Arcs:\n{arcs}"

    def parse_options(self, line):
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

    def parse_entities(self, line):
        entities = []
        for name in line.split(','):
            dirty_name = name.strip(';')
            entities.append({
                'name': re.sub(REGEX_ATTRIBUTES, '', dirty_name).strip(),
                'options': self.parse_options(dirty_name),
            })
        if not entities:
            raise Exception("Could not parse the entities.")
        self.entities = entities

    def parse_arcs(self, line):
        arcs_list = []
        # split the ',' if they are not inside square brackets (a->b [a1=1, a2=2] should not be splitted for instance)
        pattern = re.compile(",(?![^\[]*])")
        commas = [match.end() for match in pattern.finditer(line)]
        start = 0
        for end in commas + [len(line)]:
            arc = line[start:end]
            arcs_list.append({
                'arc': re.sub(REGEX_ATTRIBUTES, '', arc).strip(),
                'options': self.parse_options(arc),
            })
            start = end
        self.arcs.append(arcs_list)
        
    def parse(self):
        for line in self.input.split(';'):
            # remove comment (anything from # to \n)
            line = re.sub('#.*\n', '', line).strip()
            if not line:
                continue
            if not self.entities and any(line.strip().startswith(option) for option in self.context.keys()):
                # parse options only if the line begins with a known option key
                self.parse_context(line)
            elif not self.entities:
                # parse entities once
                self.parse_entities(line)
            else:
                # parse lines
                self.parse_arcs(line)
        print("PARSING GAVE:\n", self)
