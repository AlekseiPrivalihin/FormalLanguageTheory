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
    def from_file(self, path):
        productions = []
        with open(path, 'r') as input_file:
            for line in input_file:
                production = line.split()
                productions.append(production[0] + ' -> ' + ' '.join(production[1:]))

        cfg = CFG.from_text('\n'.join(productions))

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

    

        
                

        

