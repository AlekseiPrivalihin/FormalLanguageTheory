from pyformlang.finite_automaton import State, Symbol, DeterministicFiniteAutomaton
from pygraphblas import Matrix

from Graph import Graph

def test_from_file():
    g = Graph()
    g.from_file("input.txt")
    g.start_vertices.add(0)
    g.terminal_vertices.add(1)
    dfa = g.to_dfa()
    assert dfa.accepts('a')
    assert dfa.accepts('abbbbb')
    assert not dfa.accepts('aba')
    assert not dfa.accepts('c')

def test_from_regex():
    g = Graph()
    g.from_regex("regex_input.txt")
    dfa = g.to_dfa()
    assert dfa.accepts('a')
    assert dfa.accepts('abababa')
    assert not dfa.accepts('ab')
    assert not dfa.accepts('c')

def test_transitive_closure():
    g = Graph()
    g.from_file("input3.txt")
    reachability_matrix = g.transitive_closure()
    expected = Matrix.from_lists(
        [0, 0, 1, 3, 3, 3, 4, 4],
        [1, 2, 2, 1, 2, 4, 1, 2],
        [True, True, True, True, True, True, True, True]
    )

    assert expected.iseq(reachability_matrix)

def test_intersect():
    g1 = Graph()
    g1.from_file("input.txt")
    g1.start_vertices.add(0)
    g1.terminal_vertices.add(1)
    g2 = Graph()
    g2.from_file("input2.txt")
    g2.start_vertices.add(0)
    g2.terminal_vertices.add(1)
    dfa = g1.intersect(g2).to_dfa()
    assert dfa.accepts('a')
    assert not dfa.accepts('abbbbb')
    assert not dfa.accepts('aba')
    assert not dfa.accepts('c')
