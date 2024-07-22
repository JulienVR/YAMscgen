# YAMscgen

### Command Line Interface

```
$ python3 yamscgen.py -h
usage: YAMscgen [-h] [-i INPUT] -o OUTPUT [-t {svg,png,pdf}]

Generate flexible and customizable sequence diagrams using and extending the synthax of Mscgen: https://www.mcternan.me.uk/mscgen/.

options:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        The input file to read from. If omitted, reads from the standard input.
  -o OUTPUT, --output OUTPUT
                        The output file to write to.
  -t {svg,png,pdf}, --type {svg,png,pdf}

Written by Julien Van Roy under supervision of Prof. Bruno Quoitin (UMons). Code available at https://github.com/JulienVR/YAMscgen.
```

### Tests

To run all tests :

> $ python3 -m unittest discover

To run a particular test:

> $ python3 -m unittest test.test_parser.TestParser.test_parse_options
