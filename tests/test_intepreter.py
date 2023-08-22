from src.interpreter.interpreter import Interpreter
from src.interpreter.terms import Variable, Atom
import os

def test_sample():
    prolog: Interpreter = Interpreter()
    print(os.getcwd())
    prolog.load_base("sample/parent.pl")
    print(prolog.answer("parent(X, Y)."))
    assert prolog.answer("parent(X, Y).") == [{Variable('X'): Atom("Maria"), Variable('Y'): Atom("Gosho")},
                                               {Variable('X'): Atom("Maria"), Variable('Y'): Atom("Ana")},
                                               {Variable('X'): Atom("Gosho"), Variable('Y'): Atom("Pesho")}]


def test_simple():
    prolog = Interpreter()
    prolog.load_base_direct("parent(maria, gosho).")
    assert prolog.answer("parent(X, Y).") == [{Variable('X'): Atom("maria"), Variable('Y'): Atom("gosho")}]


def test_rule():
    prolog: Interpreter = Interpreter()
    prolog.load_base("sample/grandparent.pl")

    assert prolog.answer("parent(X, Y), parent(Y, Z).") == None
                                                
