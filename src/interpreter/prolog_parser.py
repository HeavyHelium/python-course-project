"""
A parser for Prolog programs
"""
from typing import List, Union
from src.interpreter.tokenizer import Tokenizer
from src.interpreter.terms import Atom, Variable, PList, Predicate,\
                                  NfPredicate, Fact, Rule,\
                                  Conjunction

from src.interpreter.knowledge_base import KnowledgeBase

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
            self.exp_error("an atom, variable or list", str(self.tokens[self.index][0]))

    def parse_plist(self,
                    opener: str = "LBRACKET",
                    closer: str = "RBRACKET") -> PList:
        """
        Parses a list of elements
        """
        elements = []
        self.index += 1 # skip the opener

        if self.tokens[self.index][0] == closer:
            self.index += 1
            return PList(elements)

        while self.tokens[self.index][0] != closer \
              and self.index < len(self.tokens):

            elements.append(self.parse_argument())

            if self.index >= len(self.tokens):
                self.eof_error("a closing bracket")

            if self.tokens[self.index][0] == "COMMA":
                self.index += 1

            elif self.tokens[self.index][0] != closer:
                self.exp_error("a closing bracket",
                                str(self.tokens[self.index][0]))
            else: # closer
                self.index += 1
                return PList(elements)

        self.exp_error("a closing bracket",
                       str(self.tokens[self.index][0]))

    def parse_predicate(self) -> Predicate: # positive literal
        """
        Parses a predicate
        """
        if self.tokens[self.index][0] != "ATOM":
            self.exp_error("an atom",
                            str(self.tokens[self.index][0]))

        name = self.tokens[self.index][1]
        self.index += 1

        if self.index >= len(self.tokens):
            self.eof_error("an openning parenthesis")

        if self.tokens[self.index][0] != "LPAREN":
            if self.tokens[self.index][0] == "PERIOD":
                return Predicate(name, PList([]))

            self.exp_error("an openning parenthesis",
                            str(self.tokens[self.index][0]))

        arguments = self.parse_plist("LPAREN", "RPAREN")
        return Predicate(name, arguments)

    def parse_nf_predicate(self) -> NfPredicate: # negative literal
        """
        Parses a negative literal
        """
        if self.tokens[self.index][0] != "NOT":
            self.exp_error("a not",
                           str(self.tokens[self.index][0]))
        self.index += 1

        if self.index >= len(self.tokens):
            self.eof_error("opening parenthesis")

        if self.tokens[self.index][0] != "LPAREN":
            self.exp_error("openning parenthesis",
                            str(self.tokens[self.index][0]))
        self.index += 1

        if self.index >= len(self.tokens):
            self.eof_error("atom")

        pred: Predicate = self.parse_predicate()

        if self.index >= len(self.tokens):
            self.eof_error("closing parenthesis")

        if self.tokens[self.index][0] != "RPAREN":
            self.exp_error("closing parenthesis",
                            str(self.tokens[self.index][0]))
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
                self.eof_error("a comma or end of clause")

            if self.tokens[self.index][0] == "COMMA":
                self.index += 1
            elif self.tokens[self.index][0] != "PERIOD":
                self.exp_error("a comma or end of clause",
                                str(self.tokens[self.index][0]))

        self.index += 1

        return Conjunction(predicates)

    def parse_rule(self) -> Rule:
        """
        Parses a rule
        """
        head: Predicate = self.parse_predicate()
        if self.index >= len(self.tokens):
            self.eof_error("implication")


        if self.tokens[self.index][0] != "IMPLICATION":
            self.exp_error("implication",
                            str(self.tokens[self.index][0]))

        self.index += 1
        tail: Conjunction = self.parse_goal()
        return Rule(head, tail)

    def parse_fact(self) -> Fact:
        """
        Parses a fact
        """
        pred: Predicate = self.parse_predicate()
        if self.index >= len(self.tokens):
            self.eof_error("end of clause")

        if self.tokens[self.index][0] != "PERIOD":
            self.exp_error("end of clause",
                           str(self.tokens[self.index][0]))

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
        kb: KnowledgeBase = KnowledgeBase()
        while self.index < len(self.tokens):
            clause = self.parse_program_clause()
            kb.add_clause(clause)
        return kb

    @staticmethod
    def exp_error(expected: str = None, got: str = None) -> None:
        """
        Raises a ValueError with a message, 
        indicating that an expected token did not match the actual token
        """
        raise ValueError(f"Expected {expected}. Got {got}.")

    @staticmethod
    def eof_error(expected: str = None) -> None:
        """
        Same as exp_error, but when the end of file is reached unexpectedly 
        """
        PrologParser.exp_error(expected, "EOF")









if __name__ == "__main__": 
    p = Fact("factorial", PList([Atom("N"), Atom("Res"), PList([Atom("N"), Atom("Res")])]))
    lst = PList([Atom("N"), Atom("Res"), PList([Atom("N"), Atom("Res")])])
    print(lst)
    print(repr(lst))
    print(str(p))
    print(repr(p))