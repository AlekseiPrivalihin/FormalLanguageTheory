from pyformlang.finite_automaton import State, Symbol, DeterministicFiniteAutomaton
from pygraphblas import Matrix

def test_matrix_prod():
    A = Matrix.from_lists(
        [0, 0, 0, 1, 1, 1, 2, 2, 2],
        [0, 1, 2, 0, 1, 2, 0, 1, 2],
        [1, 2, 1, 2, 1, 2, 1, 2, 1])

    B = Matrix.from_lists(
        [0, 0, 0, 1, 1, 1, 2, 2, 2],
        [0, 1, 2, 0, 1, 2, 0, 1, 2],
        [2, 1, 2, 1, 2, 1, 2, 1, 2])

    A_times_B = Matrix.from_lists(
        [0, 0, 0, 1, 1, 1, 2, 2, 2],
        [0, 1, 2, 0, 1, 2, 0, 1, 2],
        [6, 6, 6, 9, 6, 9, 6, 6, 6])

    assert A_times_B.iseq(A @ B)


def test_DFA_intersection():
    symb_a = Symbol("a")
    symb_b = Symbol("b")

    state0 = State(0)
    state1 = State(1)

    dfa1 = DeterministicFiniteAutomaton()
    dfa2 = DeterministicFiniteAutomaton()

    dfa1.add_start_state(state0)
    dfa2.add_start_state(state0)

    dfa1.add_final_state(state1)
    dfa2.add_final_state(state1)

    dfa1.add_transition(state0, symb_a, state1)
    dfa1.add_transition(state1, symb_b, state0)
    dfa2.add_transition(state0, symb_a, state1)
    dfa2.add_transition(state1, symb_b, state1)

    dfa_intersection = dfa1 & dfa2

    assert dfa1.accepts("ababa")
    assert dfa1.accepts("a")
    assert not dfa2.accepts("ababa")
    assert dfa2.accepts("abbbb")
    assert dfa2.accepts("a")
    assert not dfa1.accepts("abbbb")
    assert dfa_intersection.accepts("a")
    assert not dfa_intersection.accepts("ababa")
    assert not dfa_intersection.accepts("abbbb")
