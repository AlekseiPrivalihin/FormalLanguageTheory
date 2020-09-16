from pygraphblas.matrix import Matrix
from pygraphblas.types import BOOL
from pyformlang.regular_expression import Regex
from pyformlang.finite_automaton import State, Symbol, DeterministicFiniteAutomaton

class Graph:
    def __init__(self):
        self.n_vertices = 0
        self.label_matrices = dict()
        self.start_vertices = set()
        self.terminal_vertices = set()

    def from_file(self, filename):
        input_file = open(filename)
        edges = input_file.read().rstrip().split('\n')
        input_file.close()
        max_vertice_number = 0
        for edge in edges:
            fro, label, to = edge.split(' ')
            max_vertice_number = max(max_vertice_number, int(fro))
            max_vertice_number = max(max_vertice_number, int(to))            

        self.n_vertices = max_vertice_number + 1
        for edge in edges:
            fro, label, to = edge.split(' ')
            self.get_by_label(label)[int(fro), int(to)] = True

    def from_regex(self, filename):
        input_file = open(filename)
        regex = Regex(input_file.read().rstrip())
        dfa = regex.to_epsilon_nfa().to_deterministic().minimize()
        self.n_vertices = len(dfa.states)
        state_renumeration = dict()
        i = 0
        for state in dfa.states:
            state_renumeration[state] = i
            i += 1
            
        for fro, label, to in dfa._transition_function.get_edges():
            self.get_by_label(str(label))[state_renumeration[fro], state_renumeration[to]] = True

        self.start_vertices.add(state_renumeration[dfa.start_state])

        for state in dfa.final_states:
            self.terminal_vertices.add(state_renumeration[state])

    def to_dfa(self):
        dfa = DeterministicFiniteAutomaton()
        states = [State(i) for i in range(self.n_vertices)]
        for i in self.start_vertices:
            dfa.add_start_state(states[i])

        for i in self.terminal_vertices:
            dfa.add_final_state(states[i])

        for label in self.labels():
            symbol = Symbol(label)
            fro, to, has_edge = self.get_by_label(label).to_lists()
            for i in range(len(fro)):
                if has_edge:
                    dfa.add_transition(states[fro[i]], symbol, states[to[i]])
        return dfa
    
        
        
    def transitive_closure(self):
        adj_matrix = Matrix.sparse(BOOL, self.n_vertices, self.n_vertices)
        for label_matrix in self.label_matrices.values():
            adj_matrix = adj_matrix | label_matrix

        for k in range(self.n_vertices):
            adj_matrix += adj_matrix @ adj_matrix

        return adj_matrix

    def labels(self):
        return self.label_matrices.keys()

    def get_by_label(self, label):
        if label not in self.label_matrices.keys():
            self.label_matrices[label] = Matrix.sparse(BOOL, self.n_vertices, self.n_vertices)
        return self.label_matrices[label]

    def intersect(self, graph):
        result = Graph()
        result.n_vertices = self.n_vertices * graph.n_vertices
        for i in self.start_vertices:
            for j in graph.start_vertices:
                result.start_vertices.add(i * self.n_vertices + j)

        for i in self.terminal_vertices:
            for j in graph.terminal_vertices:
                result.terminal_vertices.add(i * self.n_vertices + j)
        
        for label in self.labels() | graph.labels():
            result.label_matrices[label] = self.get_by_label(label).kronecker(graph.get_by_label(label))

        return result

    def print_n_edges_by_labels(self):
        for label in self.labels():
            print(label, self.get_by_label(label).nvals)

    def print_reachable(self, fro_fname, to_fname):
        fro = set()
        if fro_fname != None:
            fro_file = open(fro_fname)
            fro = set(map(int, fro_file.readline().rstrip().split()))
            fro_file.close()
        else:
            fro = set([i for i in range(self.n_vertices)])
            
        to = set()
        if to_fname != None:
            to_file = open(to_fname)
            to = set(map(int, to_file.readline().rstrip().split()))
            to_file.close()
        else:
            to = set([i for i in range(self.n_vertices)])

        reachability_matrix = self.transitive_closure()
        for i, j, _ in zip(*reachability_matrix.to_lists()):
            if (i in fro) and (j in to):
                print(f'{j} reachable from {i}')
                
