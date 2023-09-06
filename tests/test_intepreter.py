import os
import pytest
from src.interpreter.interpreter import Interpreter

def test_sample():
    prolog: Interpreter = Interpreter()
    path = os.path.join("sample", "test1.pl")

    with open(path, "r", encoding="utf-8") as f:
        src = f.read()
        prolog.load_base(src)

    exp = """true.
             X = 'Maria', Y = 'Gosho'
             true.
             X = 'Maria', Y = 'Ana'
             true.
             X = 'Gosho', Y = 'Pesho'"""

    assert prolog.answer("parent(X, Y).").split() == exp.split()



def test_longer_goal():
    prolog: Interpreter = Interpreter()
    path = os.path.join("sample", "test2.pl")

    with open(path, "r", encoding="utf-8") as f:
        src = f.read()
        prolog.load_base(src)

    exp = """true.
             X = pesho, Y = gosho, Z = ana"""

    assert prolog.answer("parent(X, Y), parent(Y, Z).").split() == exp.split()

    with pytest.raises(ValueError):
        prolog.answer("ancestor.")
