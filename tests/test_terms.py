from src.interpreter.terms import Conjunction, Predicate,\
                                  PList, Variable, Atom


def test_var_extraction():
    c:  Conjunction = Conjunction([Predicate("parent", PList([Atom("Maria"), Variable("X")])),
                                    Predicate("parent", PList([Variable("X"), Atom("Gosho")]))])

    assert c.variables == {'X': Variable("X")}
