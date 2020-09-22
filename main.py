from Graph import Graph
import argparse
import time
import os

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
        , help='path to the regular expression file or ALL to use all files in ./regexes'
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

    current_t_sec = time.process_time()
    g1 = Graph()
    g1.from_file(args.graph)
    print(f"It took {time.process_time() - current_t_sec} sec to read the graph", flush=True)
    
    regex_fnames = [args.regex]
    prefix = ''
    if args.regex == 'ALL':
        regex_fnames = os.listdir('regexes')
        prefix = 'regexes/'

    n_regexes = len(regex_fnames)
    cum_time_mul_sec = 0
    max_time_mul_sec = 0
    cum_time_square_sec = 0
    max_time_square_sec = 0
    cum_time_intersect_sec = 0
    max_time_intersect_sec = 0
    cum_time_checksum_sec = 0
    max_time_checksum_sec = 0

    for regex_fname in regex_fnames:
        
        g2 = Graph()
        g2.from_regex(f'{prefix}{regex_fname}')
        
        current_t_sec = time.process_time()
        g_intersection = g1.intersect(g2)
        task_t_sec = time.process_time() - current_t_sec
        cum_time_intersect_sec += task_t_sec
        max_time_intersect_sec = max(max_time_intersect_sec, task_t_sec)

        current_t_sec = time.process_time()
        adj_matrix_square = g_intersection.transitive_closure_square()
        task_t_sec = time.process_time() - current_t_sec
        cum_time_square_sec += task_t_sec
        max_time_square_sec = max(max_time_square_sec, task_t_sec)

        current_t_sec = time.process_time()
        adj_matrix_mul = g_intersection.transitive_closure_mul()
        task_t_sec = time.process_time() - current_t_sec
        cum_time_mul_sec += task_t_sec
        max_time_mul_sec = max(max_time_mul_sec, task_t_sec)

        g_intersection.print_reachable(adj_matrix_square, args.initial, args.destination)
        
        current_t_sec = time.process_time()
        g_intersection.print_n_edges_by_labels()
        task_t_sec = time.process_time() - current_t_sec
        cum_time_checksum_sec += task_t_sec
        max_time_checksum_sec = max(max_time_checksum_sec, task_t_sec)

    print(f'It took on average {cum_time_intersect_sec / n_regexes} sec to intersect the graphs')
    print(f'The maximum time was {max_time_intersect_sec} sec')
    print(f'It took on average {cum_time_mul_sec / n_regexes} sec to compute transitive closure via multiplying by adjacency matrix')
    print(f'The maximum time was {max_time_mul_sec} sec')
    print(f'It took on average {cum_time_square_sec / n_regexes} sec to compute transitive closure via repeatedly taking adjacency matrix to the power of 2')
    print(f'The maximum time was {max_time_square_sec} sec')
    print(f'It took on average {cum_time_checksum_sec / n_regexes} sec to print the checksums')
    print(f'The maximum time was {max_time_checksum_sec} sec', flush=True)
    
        
        
