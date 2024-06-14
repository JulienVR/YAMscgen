import argparse

from src.builder import Builder

parser = argparse.ArgumentParser(
    prog="Diagrams",
    description="Generate flexible and customizable sequence diagrams.",
    epilog="Written by Julien Van Roy under supervision of Pr. Bruno Quoitin (UMons).",
)

#TODO: allows to read from standard input, as mscgen (stop reading after a CTRL+D)
parser.add_argument(
    "-i", "--input", help="The input file to read from.", required=True,
)
parser.add_argument(
    "-o", "--output", help="The output file to write to.", required=True,
)
parser.add_argument("-f", "--filetype", choices=["svg", "png"], default="svg")

args = parser.parse_args()

with open(args.input) as f:
    text_input = f.read()
image = Builder(text_input).generate()

with open(args.output, 'wb+') as f:
    f.write(image)
