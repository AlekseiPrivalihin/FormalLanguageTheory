from pyformlang.regular_expression import Regex
from DifferentiableRegex import DifferentiableRegex

def test_simple_regex():
    regexes = ["a", "a b", "a | b", "a*"]
    answers = ["a", "ab", "b", "aaa"]
    for i in range(4):
        regex = DifferentiableRegex(Regex(regexes[i]))
        word = answers[i]
        assert(regex.accepts(word))


def test_wrong_regex():
    regexes = ["a", "a b", "a | b", "a*"]
    answers = ["b", "a", "ab", "aba"]
    for i in range(4):
        regex = DifferentiableRegex(Regex(regexes[i]))
        word = answers[i]
        assert(not regex.accepts(word))


def test_default_regex():
    answers = ["", "a", "ab", "aaab"]
    for word in answers:
        regex = DifferentiableRegex(Regex("a * | a * b"))
        assert(regex.accepts(word)) 


def test_comp_regex():
    regex = DifferentiableRegex(Regex('(a * b | c) * d'))
    correct = ['cd', 'aaabd', 'aabcd', 'abbd']
    incorrect = ['dd', 'aaaad', 'ababc', 'q']
    for word in correct:
        assert(regex.accepts(word))

    for word in incorrect:
        assert(not regex.accepts(word))


def test_comp_regex_redundant():
    regexes = ['a *', 'a | a * | a | a *', 'a * * * * *', '(a | ) *']
    answers = ['', 'a', 'aaa', 'aaaaaaaa']
    for raw_regex in regexes:
        regex = DifferentiableRegex(Regex(raw_regex))
        for word in answers:
            assert(regex.accepts(word))
