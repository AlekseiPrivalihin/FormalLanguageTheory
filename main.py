import argparse
from DifferentiableRegex import DifferentiableRegex
from pyformlang.regular_expression import Regex

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='command line interface for simple graph/dfa operations')
    parser.add_argument(
        '--regex'
        , required=True
        , type=str
        , help='path to the regular expression file'
    )
    parser.add_argument(
        '--string'
        , required=True
        , type=str
        , help='path to the file containing string for acceptance check'
    )
    args = parser.parse_args()

    with open(args.regex) as regex_file:
        regex = DifferentiableRegex(Regex(regex_file.readline().rstrip()))
    
    with open(args.string) as input_file:
        s = input_file.readline().rstrip()
    
    print(regex.accepts(s))
