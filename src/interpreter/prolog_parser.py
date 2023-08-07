from typing import List, Union, Dict
from src.interpreter.tokenizer import Tokenizer
from src.interpreter.terms import Atom, Variable, PList, Predicate,\
                                  NfPredicate, Fact, Rule,\
                                  Conjunction, KnowledgeBase

class PrologParser:
    """
    A parser for Prolog programs
    """
    def __init__(self, text: str) -> None:
        self.text: str = text
        t: Tokenizer = Tokenizer()
        t.tokenize(text)
        self.tokens: List = t.tokens # this might throw an exception,
                                # but we don't catch it here
        self.index = 0 # index of the current token

    def parse_atom(self) -> Atom:
        """
        Parses an atom
        """
        atom = Atom(self.tokens[self.index][1])
        self.index += 1

        return atom

    def parse_variable(self) -> Variable:
        """
        Parses a variable
        """
        variable = Variable(self.tokens[self.index][1])
        self.index += 1
        return variable

    def parse_argument(self) -> Union[Atom, Variable, "PList"]:
        """
        Parses an argument
        """
        if self.tokens[self.index][0] == "VARIABLE" \
          or self.tokens[self.index][0] == "WILDCARD":
            return self.parse_variable()

        elif self.tokens[self.index][0] == "ATOM"\
          or self.tokens[self.index][0] == "INTEGER"\
          or self.tokens[self.index][0] =="QUOTED_ATOM":
            return self.parse_atom()

        elif self.tokens[self.index][0] == "LBRACKET":
            return self.parse_plist()
        else:
            raise ValueError("Expected an atom, variable or list, got "
                            + str(self.tokens[self.index][0]))

    def parse_plist(self,
                    opener: str = "LBRACKET",
                    closer: str = "RBRACKET") -> PList:
        """
        Parses a list of elements
        """
        elements = list()
        self.index += 1 # skip the opener

        while self.tokens[self.index][0] != closer \
              and self.index < len(self.tokens):

            elements.append(self.parse_argument()) 

            if self.index >= len(self.tokens):
                raise ValueError("Expected a closing bracket, got EOF")

            if self.tokens[self.index][0] == "COMMA":
                self.index += 1

            elif self.tokens[self.index][0] != closer: 
                raise ValueError("Expected a comma or a closing bracket, got "
                                + str(self.tokens[self.index][0]))
            else: # closer
                self.index += 1
                return PList(elements)

        raise ValueError("Expected a closing bracket, got "
                        + str(self.tokens[self.index][0]))

    def parse_predicate(self) -> Predicate: # positive literal
        """
        Parses a predicate
        """
        if self.tokens[self.index][0] != "ATOM":
            raise ValueError("Expected an atom, got "
                            + str(self.tokens[self.index][0]))
        name = self.tokens[self.index][1]
        self.index += 1

        if self.tokens[self.index][0] != "LPAREN":
            raise ValueError("Expected an openning parenthesis, got "
                            + str(self.tokens[self.index][0]))

        arguments = self.parse_plist("LPAREN", "RPAREN")
        return Predicate(name, arguments)

    def parse_nf_predicate(self) -> NfPredicate: # negative literal
        """
        Parses a negative literal
        """
        if self.tokens[self.index][0] != "NOT":
            raise ValueError("Expected a not, got "
                            + str(self.tokens[self.index][0]))
        self.index += 1

        if self.tokens[self.index][0] != "LPAREN":
            raise ValueError("Expected an openning parenthesis, got "
                            + str(self.tokens[self.index][0]))
        self.index += 1

        pred: Predicate = self.parse_predicate()

        if self.tokens[self.index][0] != "RPAREN":
            raise ValueError("Expected a closing parenthesis, got "
                            + str(self.tokens[self.index][0]))
        self.index += 1

        return NfPredicate(pred.name, pred.arguments)

    def parse_goal(self) -> Conjunction:
        """
        Parses a conjunction
        """
        predicates: List[Predicate] = []
        while self.tokens[self.index][0] != "PERIOD":
            if self.tokens[self.index][0] == "NOT":
                predicates.append(self.parse_nf_predicate())
            else:
                predicates.append(self.parse_predicate())

            if self.index >= len(self.tokens):
                raise ValueError("Expected a comma or end of clause, got EOF")

            if self.tokens[self.index][0] == "COMMA": 
                self.index += 1
            elif self.tokens[self.index][0] != "PERIOD": 
                raise ValueError("Expected a comma or end of clause, got "
                                + str(self.tokens[self.index][0]))

        self.index += 1

        return Conjunction(predicates)

    def parse_rule(self) -> Rule:
        """
        Parses a rule
        """
        head: Predicate = self.parse_predicate()
        if self.index >= len(self.tokens):
            raise ValueError("Expected implication, got EOF")


        if self.tokens[self.index][0] != "IMPLICATION": 
            raise ValueError("Expected an implication, got " 
                            + str(self.tokens[self.index][0]))

        self.index += 1
        tail: Conjunction = self.parse_goal()
        return Rule(head, tail)
    
    def parse_fact(self) -> Fact:
        """
        Parses a fact
        """
        pred: Predicate = self.parse_predicate()
        if self.index >= len(self.tokens):
            raise ValueError("Expected end of clause, got EOF")

        if self.tokens[self.index][0] != "PERIOD":
            raise ValueError("Expected end of clause, got " 
                            + str(self.tokens[self.index][0]))

        self.index += 1
        return Fact(pred.name, pred.arguments)

    def parse_program_clause(self) -> Union[Fact, Rule]:
        """
        Parses a clause of a Horn program 
        """
        temp_id: int = self.index
        try:
            e: Fact = self.parse_fact()
            return e
        except ValueError:
            self.index = temp_id
            return self.parse_rule()      


    def parse_program(self) -> KnowledgeBase:
        """
        Parses a Horn program
        """
        kb = KnowledgeBase()
        while self.index < len(self.tokens):
            clause = self.parse_program_clause()
            kb.add_clause(clause)
        return kb









if __name__ == "__main__": 
    p = Fact("factorial", PList([Atom("N"), Atom("Res"), PList([Atom("N"), Atom("Res")])]))
    lst = PList([Atom("N"), Atom("Res"), PList([Atom("N"), Atom("Res")])])
    print(lst)
    print(repr(lst))
    print(str(p))
    print(repr(p))