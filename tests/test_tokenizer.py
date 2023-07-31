from src.interpreter.tokenizer import Tokenizer 

sample_program = """good('Pain') :- meaningful('Pain'), 
                                    not(deadly('Pain')).

                    list([]).
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
                        ('RBRACKET', ']'), ('RPAREN', ')'), ('PERIOD', '.')
                        ]
