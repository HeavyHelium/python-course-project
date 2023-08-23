import os
import pytest
from src.interpreter.interpreter import Interpreter

def test_sample():
    prolog: Interpreter = Interpreter()
    path = os.path.join("sample", "test1.pl")
    src = open(path, "r").read()

    prolog.load_base(src)

    exp = """true.
             X = 'Maria', Y = 'Gosho'
             X = 'Maria', Y = 'Ana'
             X = 'Gosho', Y = 'Pesho'"""
    assert prolog.answer("parent(X, Y).").split() == exp.split()



def test_longer_goal():
    prolog: Interpreter = Interpreter()
    path = os.path.join("sample", "test2.pl")
    src = open(path, "r").read()

    prolog.load_base(src)

    exp = """true.
             X = pesho, Y = gosho, Z = ana"""

    assert prolog.answer("parent(X, Y), parent(Y, Z).").split() == exp.split()

    with pytest.raises(ValueError):
        prolog.answer("ancestor.")
