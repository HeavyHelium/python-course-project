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