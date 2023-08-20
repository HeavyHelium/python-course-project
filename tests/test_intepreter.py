from src.interpreter.interpreter import Interpreter
from src.interpreter.terms import Variable, Atom
import os

def test_sample():
    prolog: Interpreter = Interpreter()
    print(os.getcwd())
    prolog.load_base("sample/parent.pl")
    assert prolog.answer("parent(X, Y).") == [{Variable('X'): Atom("Maria"), Variable('Y'): Atom("Gosho")},
                                               {Variable('X'): Atom("Maria"), Variable('Y'): Atom("Ana")},
                                               {Variable('X'): Atom("Gosho"), Variable('Y'): Atom("Pesho")}]
