from src.interpreter.prolog_parser import PrologParser
import re

sample_program = """ factorial(0, 1). 
                     factorial(N, Res) :- N > 0, 
                     N1 is N - 1, 
                     factorial(N1, Res1), 
                     Res is Res1 * N."""


def remove_blankspace(s: str) -> str: 
    pattern = r'\s*^\s*|\s*$'
    return re.sub(pattern, '', s, flags=re.MULTILINE)

def test_comments():
    source = """
                %factorial(N, Res)

                factorial(0, 1).
                /*
                Multiline comment
                %it has a subcomment, which should not matter.*/

                factorial(N, Res) :- N > 0, 
                                     N1 is N - 1, 
                                     factorial(N1, Res1), 
                                     Res is Res1 * N.
            """
    res = sample_program
    p = PrologParser(source)
    print(p._source)
    print(res)
    assert remove_blankspace(p._source) == remove_blankspace(res)

