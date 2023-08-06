from src.interpreter.tokenizer import Tokenizer
import pytest

sample_program = """good('Pain') :- meaningful('Pain'), 
                                not(deadly('Pain')).
                    /* In our definition, 
                    the empty list is not an atom(syntactically)

                    */
                                    
                                    % the empty list is a list
                            
                                    list([]).
                                    something(_).
                                    """

def test_tokenizer():
    t = Tokenizer()
    t.tokenize(sample_program)
    assert t.tokens == [('ATOM', 'good'), ('LPAREN', '('), 
                        ('QUOTED_ATOM', "'Pain'"), ('RPAREN', ')'), 
                        ('IMPLICATION', ':-'), ('ATOM', 'meaningful'), 
                        ('LPAREN', '('), ('QUOTED_ATOM', "'Pain'"), 
                        ('RPAREN', ')'), ('COMMA', ','), ('NOT', 'not'),
                        ('LPAREN', '('), ('ATOM', 'deadly'),
                        ('LPAREN', '('), ('QUOTED_ATOM', "'Pain'"),
                        ('RPAREN', ')'), ('RPAREN', ')'), ('PERIOD', '.'), 
                        ('ATOM', 'list'), ('LPAREN', '('), ('LBRACKET', '['), 
                        ('RBRACKET', ']'), ('RPAREN', ')'), ('PERIOD', '.'), 
                        ('ATOM', 'something'), ('LPAREN', '('), ('WILDCARD', '_'),
                        ('RPAREN', ')'), ('PERIOD', '.'),
                        ]

def test_list_tokens(): 
    t = Tokenizer()
    t.tokenize('[]')
    assert t.tokens == [('LBRACKET', '['), ('RBRACKET', ']')]
    t.tokenize('[1]')
    assert t.tokens == [('LBRACKET', '['), ('INTEGER', '1'), ('RBRACKET', ']')]
    t.tokenize('[1, 2]')
    assert t.tokens == [('LBRACKET', '['), ('INTEGER', '1'), ('COMMA', ','),
                        ('INTEGER', '2'), ('RBRACKET', ']')]
    t.tokenize('list([H | T]).')
    assert t.tokens == [('ATOM', 'list'), ('LPAREN', '('), ('LBRACKET', '['),
                        ('VARIABLE', 'H'), ('PIPE', '|'), ('VARIABLE', 'T'),
                        ('RBRACKET', ']'), ('RPAREN', ')'), ('PERIOD', '.')]


def test_invalid(): 
    src = """
        
        nat(0).
        nat(N) :- nat(N1), is(N, succ(N1)). 
    fsgsdoi$
    """
    t = Tokenizer()
    with pytest.raises(ValueError):
        t.tokenize(src)

def test_true():
    src = """
    is_is_not(_) :- true.

    """
    t = Tokenizer()
    t.tokenize(src)
    assert t.tokens == [('ATOM', 'is_is_not'), ('LPAREN', '('),
                        ('WILDCARD', '_'), ('RPAREN', ')'), ('IMPLICATION', ':-'),
                        ('TRUE', 'true'), ('PERIOD', '.')]