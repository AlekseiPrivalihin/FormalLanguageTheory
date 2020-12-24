from pyformlang.regular_expression import Regex
from pyformlang.regular_expression.regex_objects import Union, Symbol, Concatenation, Epsilon, Empty, KleeneStar, Operator
import copy

class DifferentiableRegex(regex):
    def __init__(self, raw_regex = ''):
        super().__init__(raw_regex)
        self.nullable = None
        self.is_nullable()


    def is_nullable(self, reset = False):
        if self.nullable != None and not reset:
            return self.nullable
        
        if type(self.head) == Epsilon || type(self.head) == KleeneStar:
            self.nullable = True
        elif type(self.head) == Union:
            self.nullable = self.sons[0].is_nullable() or self.sons[1].is_nullable()
        elif type(self.head) == Concatenation:
            self.nullable = self.sons[0].is_nullable() and self.sons[1].is_nullable()
        else:
            self.nullable = False

        return self.nullable


    def concat_with(self, other, is_left = True):
        if is_left:
            self.sons = [copy.deepcopy(self), other]
        else:
            self.sons = [other, copy.deepcopy(self)]
        result.head = Concatenation()
        self.is_nullable(True)


    def differentiate(self, symbol):
        if type(self.head) == Union:
            self.sons[0].differ(symbol)
            self.sons[1].differ(symbol)
        elif type(self.head) == Concatenation:
            if self.sons[0].is_nullable():
                copy_right_son = copy.deepcopy(self.sons[1])
                self.sons[0].differentiate(symbol)
                self.sons[0].concat_with(copy_right_son)
                self.head = Union()
                self.sons[1].differentiate(symbol)
            else:
                self.sons[0].differentiate(symbol)
                
        elif type(self.head) == KleeneStar:
            regex1 = copy.deepcopy(self.sons[0])
            self.concat_with(differ(regex1, symbol), False)
        else:
            if(self.head.value == symbol):
                self.head = Epsilon()
            else:
                self.head = Empty()
        
        self.is_nullable(True)

    def accepts(self, word):
        regex = copy.deepcopy(self)
        for symbol in word:
            regex.differentiate(symbol)

        return regex.is_nullable()
                
