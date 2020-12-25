from pyformlang.regular_expression import Regex
from pyformlang.regular_expression.regex_objects import Union, Symbol, Concatenation, Epsilon, Empty, KleeneStar, Operator
import copy

class DifferentiableRegex:
    def __init__(self, regex):
        self.head = regex.head
        self.sons = []
        for son in regex.sons:
            self.sons.append(DifferentiableRegex(son))
        self.nullable = None
        self.is_nullable()


    def is_nullable(self, reset = False):
        if self.nullable != None and not reset:
            return self.nullable
        
        if type(self.head) == Epsilon or type(self.head) == KleeneStar:
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
        self.head = Concatenation()
        self.is_nullable(True)


    def differentiate(self, symbol):
        if type(self.head) == Union:
            self.sons[0].differentiate(symbol)
            self.sons[1].differentiate(symbol)
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
            regex1.differentiate(symbol)
            self.concat_with(regex1, False)
        else:
            if(self.head.value == symbol):
                self.head = Epsilon()
            else:
                self.head = Empty()
        
        self.is_nullable(True)


    def to_str(self):
        result = str(self.head) + '['
        for son in self.sons:
            result = result + son.to_str() + '  '
        if result[-1] != '[':
            return result[:-2] + ']'
        else:
            return result + ']'
        

    def accepts(self, word):
        regex = copy.deepcopy(self)
        for symbol in word:
            regex.differentiate(symbol)
            
        return regex.is_nullable()
                
