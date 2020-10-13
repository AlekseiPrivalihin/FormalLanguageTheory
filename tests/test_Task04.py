from Graph import Graph
from ContextFreeGrammar import ChomskyNormalForm as CNF
from pyformlang.cfg import *

def test_from_file():
    gr = CNF.from_file("cfg_input.txt")
    word_accepted = list(map(Terminal, 'aaba'))
    word_declined = list(map(Terminal, 'aabb'))
    assert gr.contains(word_accepted)
    assert not gr.contains([])
    assert not gr.contains(word_declined)

def test_from_file_with_eps():
    gr = CNF.from_file("cfg_eps_input.txt")
    word_accepted = list(map(Terminal, 'aaba'))
    word_declined = list(map(Terminal, 'aabb'))
    assert gr.contains(word_accepted)
    assert gr.contains([])
    assert not gr.contains(word_declined)

def test_CYK():
    gr = CNF.from_file("cfg_input.txt")
    assert gr.CYK('ab')
    assert gr.CYK('aaba')
    assert not gr.CYK('')
    assert not gr.CYK('abc')

def test_CYK_with_eps():
    gr = CNF.from_file("cfg_eps_input.txt")
    assert gr.CYK('ab')
    assert gr.CYK('aaba')
    assert gr.CYK('')
    assert not gr.CYK('abc')

def test_Hellings():
    gr = CNF.from_file("cfg_input.txt")
    g = Graph()
    g.from_file("input4.txt")
    reachable = frozenset(gr.Hellings(g))
    assert reachable == {(0, 2), (2, 0), (0, 0), (2, 1), (0, 1)}

def test_Hellings_empty_graph():
    gr = CNF.from_file("cfg_eps_input.txt")
    g = Graph()
    g.from_file("empty_input.txt")
    reachable = frozenset(gr.Hellings(g))
    assert reachable == frozenset()

def test_Hellings_empty_grammar():
    gr = CNF.from_file("empty_input.txt")
    g = Graph()
    g.from_file("input.txt")
    reachable = frozenset(gr.Hellings(g))
    assert reachable == frozenset()

def test_Hellings_eps():
    gr = CNF.from_file("cfg_eps_input.txt")
    g = Graph()
    g.from_file("input4.txt")
    reachable = frozenset(gr.Hellings(g))
    assert reachable == {(0, 0), (0, 1), (0, 2), (1, 1), (2, 0), (2, 1), (2, 2)}
