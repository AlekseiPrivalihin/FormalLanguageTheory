import argparse
from ContextFreeGrammar import ChomskyNormalForm as CNF

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='command line interface for simple graph/dfa operations')
    parser.add_argument(
        '--script'
        , required=True
        , type=str
        , help='path to the script file'
    )

    args = parser.parse_args()

    grammar_file = 'Grammar.txt'
    parser = CNF.from_file(grammar_file, 'Script')
    
    with open(args.script) as input_file:
        script = input_file.read().rstrip()
    
    print(parser.CYK("".join(script.replace('#', '@').replace('|', '#').split())))

