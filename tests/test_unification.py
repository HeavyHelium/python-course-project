from src.interpreter.terms import Atom, Variable, PList,\
                                  Predicate, Rule

from src.interpreter.unification import Unification
from src.interpreter.knowledge_base import KnowledgeBase

def test_simple():
    t1 = Atom("a")
    t2 = Atom("b")
    t3 = Variable("X")
    t4 = Variable("Y")

    unif = Unification()

    assert unif.unify(t1, t2) == False
    assert unif.unify(t1, t3) == True
    assert unif.substitution == {Variable('X'): t1}
    assert unif.unify(t3, t4) == True
    assert unif.substitution == {Variable('X'): t1, Variable('Y'): t1}


def test_list():

    unif = Unification()


    t5 = PList([Atom("a"), Atom("b"), Atom("c")])
    t6 = PList([Atom("a"), Atom("b"), Variable("X")])

    assert unif.unify(t5, t6) == True
    assert unif.substitution == {Variable('X'): Atom("c")}

def test_predicate():

    unif = Unification()

    p1 = Predicate("parent", PList([Atom("Maria"), Atom("Gosho")]))
    p2 = Predicate("parent", PList([Atom("Maria"), Atom("Ana")]))

    p3 = Predicate("parent", PList([Atom("Maria"), Variable("X")]))

    assert unif.unify(p1, p2) == False
    assert unif.unify(p3, p1) == True
    assert unif.substitution == {Variable('X'): Atom("Gosho")}

def test_answering_simple():
    kb = KnowledgeBase()
    kb.add_clause(Predicate("parent", PList([Atom("Maria"), Atom("Gosho")])))
    kb.add_clause(Predicate("parent", PList([Atom("Maria"), Atom("Ana")])))
    kb.add_clause(Predicate("parent", PList([Atom("Gosho"), Atom("Pesho")])))


    goal = [Predicate("parent", PList([Atom("Maria"), Variable("X")]))]
    assert kb.answer_query(goal, {}) == [({Variable('X'): Atom("Gosho")}),
                                         ({Variable('X'): Atom("Ana")})]
    
    goal = [Predicate("parent", PList([Variable("X"), Atom("Gosho")]))]
    assert kb.answer_query(goal, {}) == [({Variable('X'): Atom("Maria")})]
    

def test_answering_rules():
    kb = KnowledgeBase()
    grandparent = Rule(Predicate("grandparent", PList([Variable("X"), Variable("Z")])),
                       [Predicate("parent", PList([Variable("X"), Variable("Y")])),
                        Predicate("parent", PList([Variable("Y"), Variable("Z")]))])
    kb.add_clause(grandparent)
    kb.add_clause(Predicate("parent", PList([Atom("Maria"), Atom("Gosho")])))
    kb.add_clause(Predicate("parent", PList([Atom("Maria"), Atom("Ana")])))
    kb.add_clause(Predicate("parent", PList([Atom("Gosho"), Atom("Pesho")])))

    goal = [Predicate("grandparent", PList([Atom("Maria"), Variable("T")]))]
    assert kb.answer_query(goal, {}) == [({Variable('T'): Atom("Pesho")})]
