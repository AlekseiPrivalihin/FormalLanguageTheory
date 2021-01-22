from Graph import Graph
from ContextFreeGrammar import ChomskyNormalForm as CNF
from pyformlang.cfg import *

grammar_file = 'Grammar.txt'


def test_string():
    parser = CNF.from_file(grammar_file, 'String')
    assert parser.CYK(preprocess('abacaba'))
    assert parser.CYK(preprocess('qwe_rty/io.p'))
    assert parser.CYK(preprocess(''))
    assert not parser.CYK(preprocess('Abba'))
    assert not parser.CYK(preprocess('#qqq'))

def test_pattern():
    parser = CNF.from_file(grammar_file, 'Pattern')
    assert parser.CYK(preprocess('abacaba'))
    assert parser.CYK(preprocess('a|b'))
    assert parser.CYK(preprocess('b*'))
    assert parser.CYK(preprocess('(abc)+'))
    assert parser.CYK(preprocess('d?e'))
    assert not parser.CYK(preprocess('A(bb)+a'))
    assert not parser.CYK(preprocess('@?'))

def test_statement():
    parser = CNF.from_file(grammar_file, 'Statement')
    assert parser.CYK(preprocess('connect to "/usr/local/mydb"'))
    assert parser.CYK(preprocess('select count edges from graph "graph" intersect with query "(abc)+d?" intersect with graph "other_graph"'))
    assert not parser.CYK(preprocess('connect to "/usr/local/mydb";'))
    assert not parser.CYK(preprocess('connect to abacaba'))

def test_script():
    parser = CNF.from_file(grammar_file, 'Script')
    assert parser.CYK(preprocess('connect to "/usr/local/mydb";'))
    assert parser.CYK(preprocess('select count edges from graph "graph" intersect with query "(abc)+d?" intersect with graph "other_graph";connect to "dududu";'))
    assert not parser.CYK(preprocess('select;connect;select;'))
    assert not parser.CYK(preprocess('connect to "/usr/local/mydb"'))
    assert not parser.CYK(preprocess('connect to abacaba'))


def preprocess(raw_script):
    return "".join(raw_script.replace('#', '@').replace('|', '#').split())
