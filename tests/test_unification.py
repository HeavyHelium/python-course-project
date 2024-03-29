from src.interpreter.terms import Atom, Variable, PList,\
                                  Predicate, Conjunction
from src.interpreter.unification import unify

def test_simple():
    t1 = Atom("a")
    t2 = Atom("b")
    t3 = Variable("X")
    t4 = Variable("Y")

    unif = unify(t1, t2)
    assert not unif

    unif = unify(t1, t3)
    assert unif

    unif = unify(t3, t4)
    assert unif


def test_list():

    t5 = PList([Atom("a"), Atom("b"), Atom("c")])
    t6 = PList([Atom("a"), Atom("b"), Variable("X")])

    unif = unify(t5, t6)

    assert unif

def test_predicate():


    p1 = Predicate("parent", PList([Atom("Maria"), Atom("Gosho")]))
    p2 = Predicate("parent", PList([Atom("Maria"), Atom("Ana")]))

    p3 = Predicate("parent", PList([Atom("Maria"), Variable("X")]))

    unif = unify(p1, p2)
    assert not unif

    unif = unify(p1, p3)
    assert unif

def test_conjunction():
    c1 = Conjunction([Predicate("parent", PList([Atom("Maria"), Atom("Gosho")]))])
    c2 = Conjunction([Predicate("parent", PList([Atom("Maria"), Variable("X")]))])

    unif = unify(c1, c2)
    assert unif
