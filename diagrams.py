import argparse
import sys

from src.builder import Builder
from src.parser import Parser

parser = argparse.ArgumentParser(
    prog="Diagrams",
    description="Generate flexible and customizable sequence diagrams.",
    epilog="Written by Julien Van Roy under supervision of Prof. Bruno Quoitin (UMons).",
)

parser.add_argument(
    "-i",
    "--input",
    help="The input file to read from. If omitted, reads from the standard input.",
    required=False,
)
parser.add_argument(
    "-o",
    "--output",
    help="The output file to write to.",
    required=True,
)
parser.add_argument("-f", "--filetype", choices=["svg", "png"], default="svg")

args = parser.parse_args()

if not args.input:
    # read from stdin (until EOF: CTRL + D)
    text_input = "".join(line for line in sys.stdin)
else:
    # read from a file
    with open(args.input) as f:
        text_input = f.read()

image = Builder(Parser(text_input)).generate()

with open(args.output, "wb+") as f:
    f.write(image)
