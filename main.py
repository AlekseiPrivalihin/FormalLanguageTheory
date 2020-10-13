from Graph import Graph
import argparse
from ContextFreeGrammar import ChomskyNormalForm as CNF

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='command line interface for simple graph/dfa operations')
    parser.add_argument(
        '--graph'
        , required=True
        , type=str
        , help='path to the graph file'
    )
    parser.add_argument(
        '--cfg'
        , required=True
        , type=str
        , help='path to the regular expression file'
    )
    parser.add_argument(
        '--string'
        , required=True
        , type=str
        , help='path to the file containing string for CYK'
    )
    args = parser.parse_args()

    g = Graph()
    g.from_file(args.graph)
    cfg = CNF.from_file(args.cfg)
    with open(args.string) as input_file:
        s = input_file.readline().rstrip()
    print(cfg.CYK(s))
    print(cfg.Hellings(g))
    print(cfg.Asimov(g))
    print(cfg.Tenzor(g))
