from typing import AbstractSet, Iterable
from pyformlang.cfg import *
from pygraphblas import *
from Graph import Graph
from itertools import product
from collections import deque

class ChomskyNormalForm(CFG):
    def __init__(self,
                 variables: AbstractSet[Variable] = None,
                 terminals: AbstractSet[Terminal] = None,
                 start_symbol: Variable = None,
                 productions: Iterable[Production] = None):

        cfg = CFG(
            variables = variables,
            terminals = terminals,
            start_symbol = start_symbol,
            productions = productions
        )

        self.generates_eps = cfg.generate_epsilon()
        cfg = cfg.to_normal_form()

        if self.generates_eps:
            cfg._productions |= {Production(cfg.start_symbol, [])}

        super(ChomskyNormalForm, self).__init__(
            variables=cfg._variables,
            terminals=cfg._terminals,
            start_symbol=cfg._start_symbol,
            productions=cfg._productions
        )

        self.heads_for_body = dict()

        for production in self._productions:
            if len(production.body) == 1:
                body = production.body[0]
            else:
                body = tuple(production.body)
            self.heads_for_body[body] = self.heads_for_body.get(body, set()) | {production.head}

    @classmethod
    def from_file(self, path, start_symbol='S'):
        productions = []
        with open(path, 'r') as input_file:
            for line in input_file:
                production = line.split()
                productions.append(production[0] + ' -> ' + ' '.join(production[1:]))

        cfg = CFG.from_text('\n'.join(productions), start_symbol)
        return ChomskyNormalForm(
            variables=cfg.variables,
            terminals=cfg.terminals,
            start_symbol=cfg.start_symbol,
            productions=cfg.productions
        )

    def CYK(self, input_string):
        n = len(input_string)
        if n == 0:
            return self.generates_eps
        
        r = len(self._variables)
        produced_by = [[set() for _ in range(n)] for _ in range(n)]
        for i in range(n):
            produced_by[i][0] |= self.heads_for_body.get(Terminal(input_string[i]), set())

        for l in range(2, n + 1):
            for start_span in range(n - l + 1):
                for start_partition in range(start_span + 1, start_span + l):
                    l_left = start_partition - start_span
                    l_right = l - l_left
                    for left in produced_by[start_span][l_left - 1]:
                        for right in produced_by[start_partition][l_right - 1]:
                            produced_by[start_span][l - 1] |= self.heads_for_body.get((left, right), set())

        return self.start_symbol in produced_by[0][n - 1]

    def Hellings(self, graph):
        n = graph.n_vertices
        cur_edges_by_end = [set() for i in range(n)]
        cur_edges_by_start = [set() for i in range(n)]
        q = deque()
        ans = set()
        for (label, label_matrix) in graph.label_matrices.items():
            [fros, tos, _] = label_matrix.to_lists()
            for i in range(len(fros)):
                fro = fros[i]
                to = tos[i]
                variables = self.heads_for_body.get(Terminal(label), set())
                for var in variables:
                    if var == self.start_symbol:
                        ans.add((fro, to))
                        
                    cur_edges_by_end[to].add((var, fro))
                    cur_edges_by_start[fro].add((var, to))
                    q.append((var, fro, to))

        if self.generates_eps:
            for i in range(n):
                cur_edges_by_end[i].add((self.start_symbol, i))
                cur_edges_by_start[i].add((self.start_symbol, i))
                ans.add((i, i))

        while(len(q) > 0):
            (var, fro, to) = q.pop()
            to_add = set()
            cur_edges_mid = list(cur_edges_by_end[fro])
            for (var_left, fro1) in cur_edges_mid:
                for var_concat in self.heads_for_body.get((var_left, var), set()):
                    if (var_concat, fro1) not in cur_edges_by_end[to]:
                        q.append((var_concat, fro1, to))
                        cur_edges_by_end[to].add((var_concat, fro1))
                        cur_edges_by_start[fro1].add((var_concat, to))
                        if to == fro:
                            cur_edges_mid.append((var_concat, fro1))
                        if var_concat == self.start_symbol:
                            ans.add((fro1, to))

            cur_edges_mid = list(cur_edges_by_start[to])
            for (var_right, to1) in cur_edges_mid:
                for var_concat in self.heads_for_body.get((var, var_right), set()):
                    if (var_concat, fro1) not in cur_edges_by_start[fro]:
                        q.append((var_concat, fro, to1))
                        cur_edges_by_end[to1].add((var_concat, fro))
                        cur_edges_by_start[fro].add((var_concat, to1))
                        if to == fro:
                            cur_edges_mid.append((var_concat, to1))
                        if var_concat == self.start_symbol:
                            ans.add((fro, to1))
                            
        return list(ans)

    def Asimov(self, graph):
        result = Graph()
        n = graph.n_vertices
        result.n_vertices = n
        for (label, label_matrix) in graph.label_matrices.items():
            [fros, tos, _] = label_matrix.to_lists()
            for i in range(len(fros)):
                fro = fros[i]
                to = tos[i]
                variables = self.heads_for_body.get(Terminal(label), set())
                for var in variables:
                    result.get_by_label(var.value)[fro, to] = True

        if self.generates_eps:
            for i in range(n):
                result.get_by_label(self.start_symbol.value)[i, i] = True

        changes = True
        while changes:
            changes = False
            for production in self.productions:
                if len(production.body) == 2:
                    prev = result.get_by_label(production.head.value).nvals
                    mat = result.get_by_label(production.head.value)
                    toAdd = result.get_by_label(production.body[0].value) @ result.get_by_label(production.body[1].value)
                    if toAdd.nvals != 0:
                        mat += toAdd
                    if prev != result.get_by_label(production.head.value).nvals:
                        changes = True

        return list(zip(*result.get_by_label(self.start_symbol).to_lists()[:2]))

    def Tenzor(self, graph):
        (RA, heads) = self.to_recursive_automaton()
        result = Graph()
        result.n_vertices = graph.n_vertices
        for label in graph.labels():
            mat = result.get_by_label(label)
            mat += graph.get_by_label(label)
            
        result.start_vertices = graph.start_vertices
        result.terminal_vertices = graph.terminal_vertices

        result.get_by_label(self.start_symbol.value)
        if self.generate_epsilon():
            for i in range(graph.n_vertices):
                result.get_by_label(self.start_symbol)[i, i] = True
                
        intersection = result.intersect(RA)
        transitive_closure = intersection.transitive_closure()
        n = intersection.n_vertices
        changes = True
        while changes:
            prev = transitive_closure.nvals
            for i in range(n):
                for j in range(n):
                    if (i, j) in transitive_closure:
                        fro = i % RA.n_vertices
                        to = j % RA.n_vertices
                        if (fro in RA.start_vertices) and (to in RA.terminal_vertices):
                            fro_graph = i // RA.n_vertices
                            to_graph = j // RA.n_vertices
                            result.get_by_label(heads[fro, to])[fro_graph, to_graph] = True
                            
            intersection = result.intersect(RA)
            transitive_closure = intersection.transitive_closure()
            if transitive_closure.nvals == prev:
                changes = False
                
        return list(zip(*result.get_by_label(self.start_symbol).to_lists()[:2]))


    def to_recursive_automaton(self):
        RA = Graph()
        heads = {}
        RA.n_vertices = sum((len(production.body) + 1 for production in self.productions))
        v = 0
        for production in self.productions:
            RA.start_vertices.add(v)
            for i in range(len(production.body)):
                RA.get_by_label(production.body[i].value)[v, v + 1] = True
                v += 1
            RA.terminal_vertices.add(v)
            heads[v - len(production.body), v] = production.head.value
            v += 1
            
        return (RA, heads)

