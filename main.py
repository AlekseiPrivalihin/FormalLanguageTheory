from Graph import Graph
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='command line interface for simple graph/dfa operations')
    parser.add_argument(
        '--graph'
        , required=True
        , type=str
        , help='path to the graph file'
    )
    parser.add_argument(
        '--regex'
        , required=True
        , type=str
        , help='path to the regular expression file'
    )
    parser.add_argument(
        '--initial'
        , required=False
        , type=str
        , help='path to the initial set file'
    )
    parser.add_argument(
        '--destination'
        , required=False
        , type=str
        , help='path to the destination set file'
    )
    args = parser.parse_args()

    g1 = Graph()
    g1.from_file(args.graph)
    g2 = Graph()
    g2.from_regex(args.regex)
    g_intersection = g1.intersect(g2)
    g_intersection.print_reachable(args.initial, args.destination)
    g_intersection.print_n_edges_by_labels()
