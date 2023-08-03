import pytest
from src.interpreter.prolog_parser import *



def test_parse_variable():
    parser = PrologParser("X")
    assert parser.parse_variable() == Variable("X")

def test_parse_atom():
    parser = PrologParser("atom")
    assert parser.parse_atom() == Atom("atom")

def test_parse_argument():
    parser = PrologParser("X")
    assert parser.parse_argument() == Variable("X")

    parser = PrologParser("atom")
    assert parser.parse_argument() == Atom("atom")
    
    parser = PrologParser("[a, b, c]")
    assert parser.parse_argument() == PList([Atom("a"), Atom("b"), Atom("c")])

def test_parse_plist():
    lst = "[a, b, c, [pesho, gosho], [a, b, c]]"
    parser = PrologParser(lst)
    assert parser.parse_plist() == PList([Atom("a"), Atom("b"), Atom("c"),
                                          PList([Atom("pesho"), Atom("gosho")]),
                                          PList([Atom("a"), Atom("b"), Atom("c")])])
    
def test_parse_predicate(): 
    pred = "p(a, b, c)"
    parser = PrologParser(pred)
    assert parser.parse_predicate() == Predicate("p", PList([Atom("a"), Atom("b"), Atom("c")]))
    
    pred = "p(a, b, c, [a, b, c])"
    parser = PrologParser(pred)
    assert parser.parse_predicate() == Predicate("p", PList([Atom("a"), Atom("b"), 
                                                             Atom("c"), PList([Atom("a"), 
                                                             Atom("b"), Atom("c")])]))
    
def test_parse_nf_predicate(): 
    nf_pred = "not(q(a, b, c))"
    parser = PrologParser(nf_pred)
    assert parser.parse_nf_predicate() == NfPredicate("q", PList([Atom("a"),
                                                                  Atom("b"), 
                                                                  Atom("c")]))
    

def test_parse_goal(): 
    goal = "p(a, b, c), q(a, b, _), not(r(a, b, X))."
    parser = PrologParser(goal)
    assert parser.parse_goal() == Conjunction([Predicate("p", PList([Atom("a"),
                                                                     Atom("b"),
                                                                     Atom("c")])),
                                               Predicate("q", PList([Atom("a"),
                                                                     Atom("b"),
                                                                     Variable("_")])),
                                               NfPredicate("r", PList([Atom("a"),
                                                                       Atom("b"),
                                                                       Variable("X")]))])
    goal = "p(a, b, c), q(a, b, _), not(r(a, b, X))"
    with pytest.raises(Exception):
        parser = PrologParser(goal)
        parser.parse_goal()
    
def test_parse_fact(): 
    fact = "p([1, 2, X], _, X)."
    parser = PrologParser(fact)
    assert parser.parse_fact() == Predicate("p", PList([PList([Atom("1"),
                                                               Atom("2"),
                                                               Variable("X")]),
                                                        Variable("_"),
                                                        Variable("X")]))

def test_parse_rule(): 
    rule = "p(X, Y, Z) :- q(X, Y), not(r(X, Y, Z))."
    parser = PrologParser(rule)
    assert parser.parse_rule() == Rule(Predicate("p", PList([Variable("X"),
                                                             Variable("Y"),
                                                             Variable("Z")])),
                                       Conjunction([Predicate("q", PList([Variable("X"),
                                                                          Variable("Y")])),
                                                    NfPredicate("r", PList([Variable("X"),
                                                                            Variable("Y"),
                                                                            Variable("Z")]))]))
    
    rule = "p(X, Y, Z) :- q(X, Y), not(r(X, Y, Z))"
    with pytest.raises(Exception):
        parser = PrologParser(rule)
        parser.parse_rule()


def test_parse_program(): 
    program = "p(X, Y, Z) :- q(X, Y), not(r(X, Y, Z)).\np([1, 2, X], _, X)."
    parser = PrologParser(program)
    res_kb = KnowledgeBase()
    res_kb.add_clause(Rule(Predicate("p", PList([Variable("X"),
                                                  Variable("Y"),
                                                    Variable("Z")])),
                            Conjunction([Predicate("q", PList([Variable("X"),
                                                                Variable("Y")])),
                                            NfPredicate("r", PList([Variable("X"),
                                                                    Variable("Y"),
                                                                    Variable("Z")]))])))
    res_kb.add_clause(Predicate("p", PList([PList([Atom("1"),
                                                    Atom("2"),
                                                    Variable("X")]),
                                            Variable("_"),
                                            Variable("X")])))
    assert parser.parse_program() == res_kb


def test_atom_equality():
    a1 = Atom("a")
    a2 = Atom("'a'")
    a3 = Atom("a")
    a4 = Atom("b")
    assert a1 == a2 and a1 == a3 and a1 != a4





def test_unification():
    t1 = Atom("a")
    t2 = Atom("b")
    t3 = Variable("X")
    t4 = Variable("Y")

    unif = Unification()

    # assert unif.unify(t1, t2) == False
    # assert unif.unify(t1, t3) == True
    # assert unif.substitution == {Variable('X'): t1}
    # assert unif.unify(t3, t4) == True
    # assert unif.substitution == {Variable('X'): t1, Variable('Y'): t1}

    # t5 = PList([Atom("a"), Atom("b"), Atom("c")])
    # t6 = PList([Atom("a"), Atom("b"), Variable("X")])

    # assert unif.unify(t5, t6) == True
    # assert unif.substitution == {Variable('X'): Atom("c")}

    p1 = Predicate("parent", PList([Atom("Maria"), Atom("Gosho")]))
    p2 = Predicate("parent", PList([Atom("Maria"), Atom("Ana")]))

    p3 = Predicate("parent", PList([Atom("Maria"), Variable("X")]))

    assert unif.unify(p1, p2) == False
    assert unif.unify(p3, p1) == True
    assert unif.substitution == {Variable('X'): Atom("Gosho")}
    # assert unif.unify(p2, p3) == True
    # assert unif.substitution == {Variable('X'): Atom("Ana")}


def test_answering():
    kb = KnowledgeBase()
    kb.add_clause(Predicate("parent", PList([Atom("Maria"), Atom("Gosho")])))
    kb.add_clause(Predicate("parent", PList([Atom("Maria"), Atom("Ana")])))
    kb.add_clause(Predicate("parent", PList([Atom("Gosho"), Atom("Pesho")])))


    goal = Predicate("parent", PList([Atom("Maria"), Variable("X")]))
    assert kb.handle_query(goal) == [({Variable('X'): Atom("Gosho")}),
                                     ({Variable('X'): Atom("Ana")})]