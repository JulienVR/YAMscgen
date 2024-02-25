import argparse

from src.diagrams_builder import DiagramBuilder

parser = argparse.ArgumentParser(
    prog="Diagrams",
    description="Generate flexible and customizable sequence diagrams.",
    epilog="Written by Julien Van Roy under supervision of Pr. Bruno Quoitin (UMons).",
)

parser.add_argument(
    "-i", "--input", help="The input file to read from.", required=True,
)
parser.add_argument(
    "-o", "--output", help="The output file to write to.", required=True,
)
parser.add_argument("-f", "--filetype", choices=["svg", "png"], default="svg")

args = parser.parse_args()

# GENERATING DIAGRAMS
#si text dépasse: faire grossir vers le bas (on fixe donc width dès le départ: 600px, mais height pas)
# Si 3 éléments: x = 100, 300, 500
# Si 4: x = 75, 225, 375, 525
# Chaque élément texte est à l'intérieur d'un polygon (qui fit exactement la taille du texte !, peut être pas nécessaire d'avoir ce polygon)
# une ligne = tout jusqu'à ';' (chaque élement séparé par ',')

image = DiagramBuilder(args.input).parse()

with open(args.output, 'w+') as f:
    f.write(image)
