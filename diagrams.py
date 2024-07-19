try:
    import cairosvg
    cairosvg_installed = True
except ImportError:
    cairosvg_installed = False

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
parser.add_argument("-f", "--filetype", choices=["svg", "png", "pdf"], default="svg")

args = parser.parse_args()

if args.filetype == 'png' and not cairosvg_installed:
    sys.exit("Unable to generate a PNG/PDF because cairosvg is not installed.")

if not args.input:
    # read from stdin (until EOF: CTRL + D)
    text_input = "".join(line for line in sys.stdin)
else:
    # read from a file
    with open(args.input) as f:
        text_input = f.read()

svg = Builder(Parser(text_input)).generate()

if args.filetype == 'png':
    cairosvg.svg2png(svg, write_to=args.output)
elif args.filetype == 'pdf':
    cairosvg.svg2pdf(svg, write_to=args.output)
else:
    with open(args.output, "wb+") as f:
        f.write(svg)
