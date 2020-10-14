from Graph import Graph
from ContextFreeGrammar import ChomskyNormalForm as CNF
from pyformlang.cfg import *

def test_Asimov():
    gr = CNF.from_file("cfg_input.txt")
    g = Graph()
    g.from_file("input4.txt")
    reachable = frozenset(gr.Asimov(g))
    reachable_actual = frozenset(gr.Hellings(g))
    assert reachable == reachable_actual

def test_Asimov_empty_graph():
    gr = CNF.from_file("cfg_eps_input.txt")
    g = Graph()
    g.from_file("empty_input.txt")
    reachable = frozenset(gr.Asimov(g))
    reachable_actual = frozenset(gr.Hellings(g))
    assert reachable == reachable_actual
    
def test_Asimov_empty_grammar():
    gr = CNF.from_file("empty_input.txt")
    g = Graph()
    g.from_file("input.txt")
    reachable = frozenset(gr.Asimov(g))
    reachable_actual = frozenset(gr.Hellings(g))
    assert reachable == reachable_actual

def test_Asimov_eps():
    gr = CNF.from_file("cfg_eps_input.txt")
    g = Graph()
    g.from_file("input4.txt")
    reachable = frozenset(gr.Asimov(g))
    reachable_actual = frozenset(gr.Hellings(g))
    assert reachable == reachable_actual

def test_Tenzor():
    gr = CNF.from_file("cfg_input.txt")
    g = Graph()
    g.from_file("input4.txt")
    reachable = frozenset(gr.Tenzor(g))
    reachable_actual = frozenset(gr.Hellings(g))
    assert reachable == reachable_actual

def test_Tenzor_empty_graph():
    gr = CNF.from_file("cfg_eps_input.txt")
    g = Graph()
    g.from_file("empty_input.txt")
    reachable = frozenset(gr.Tenzor(g))
    reachable_actual = frozenset(gr.Hellings(g))
    assert reachable == reachable_actual
    
def test_Tenzor_empty_grammar():
    gr = CNF.from_file("empty_input.txt")
    g = Graph()
    g.from_file("input.txt")
    reachable = frozenset(gr.Tenzor(g))
    reachable_actual = frozenset(gr.Hellings(g))
    assert reachable == reachable_actual

def test_Tenzor_eps():
    gr = CNF.from_file("cfg_eps_input.txt")
    g = Graph()
    g.from_file("input4.txt")
    reachable = frozenset(gr.Tenzor(g))
    reachable_actual = frozenset(gr.Hellings(g))
    assert reachable == reachable_actual
