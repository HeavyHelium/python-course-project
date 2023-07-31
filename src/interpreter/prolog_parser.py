import re
from typing import List
from src.interpreter.tokenizer import Tokenizer

class PrologParser: 
    COMMENT = r'%[^\n]*|/\*(.|\n)*?\*/'

    def __init__(self, source: str) -> None:
        self._source: str = re.sub(PrologParser.COMMENT, '', source) # remove comments
        t: Tokenizer = Tokenizer()
        t.tokenize(self._source)
        self._tokens: List[str] = t.tokens

    def parse_term(self): 
        pass


if __name__ == "__main__":
    src = """
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
    p = PrologParser(src)
    print(p._tokens)