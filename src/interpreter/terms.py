"""
Module to represent terms and clauses
"""

from typing import List, Union

class Variable:
    """
    Class for first order variables
    """
    def __init__(self, name: str) -> None:
        self.name = name

    def __eq__(self, o: object) -> bool:
        if isinstance(o, Variable):
            return self.name == o.name

        return False

    def __hash__(self) -> int:
        return id(self) # so as to get a unique hash for each variable, regardless of name

    def __str__(self) -> str:
        return self.name
    def __repr__(self) -> str:
        return "Variable(" + self.name + ")"


class Atom:
    """
    Class for first order atoms a.k.a. symbols
    """
    def __init__(self, name: str) -> None:
        self.name = name

    def __eq__(self, o: object) -> bool:
        if isinstance(o, Atom):
            return self.name == o.name\
                   or self.name == Atom.quoted(o.name)\
                   or self.quoted(self.name) == o.name

        return False

    def __hash__(self) -> int:
        return hash(self.name)

    def __str__(self) -> str:
        return self.name
    def __repr__(self) -> str:
        return "Atom(" + self.name + ")"

    @staticmethod
    def quoted(name: str) -> str:
        """
        quotes a string
        """
        return "'" + name + "'"

class PList:
    """
    Class for first order predicate lists
    Usually used as arguments to predicates
    Also used to represent Prolog lists 
    """
    def __init__(self,
                 elements: List[Union[Atom, Variable, "PList"]]) -> None:
        self.elements = elements

    def __eq__(self, o: object) -> bool:
        if isinstance(o, PList):
            return self.elements == o.elements

        return False

    def get_variables(self) -> List[Variable]:
        """
        Returns a list of variables in the list
        """
        variables: List[Variable] = []
        for e in self.elements:
            if isinstance(e, Variable):
                variables.append(e)
            elif isinstance(e, PList):
                variables += e.get_variables()

        return variables

    def __iter__(self) -> List[Union[Atom, Variable, "PList"]]:
        return iter(self.elements)

    def __len__(self) -> int:
        return len(self.elements)

    def __str__(self) -> str:
        return '[' + ", ".join([str(e) for e in self.elements]) + ']'

    def __repr__(self) -> str:
        return "PList("'[' + ", ".join([repr(e) for e in self.elements]) + '])'

Term = Union[Atom, Variable, PList]

class Predicate:
    """
    Class for first order predicate literals
    """
    def __init__(self,
                 name: str,
                 arguments: PList) -> None:
        self.name: str = name
        self.arguments: PList = arguments

    def __eq__(self, o: object) -> bool:
        if isinstance(o, Predicate):
            return self.name == o.name and self.arguments == o.arguments

        return False

    def __str__(self) -> str:
        return self.name + str(self.arguments)
    def __repr__(self) -> str:
        return "Predicate(" + self.name + ", " + repr(self.arguments) + ")"


class NfPredicate(Predicate):
    """
    To support negation as failure
    """
    def __eq__(self, o: object) -> bool:
        if isinstance(o, NfPredicate):
            return super().__eq__(o)

        return False

    def __str__(self) -> str:
        return "not(" + super().__str__() + ")"

    def __repr__(self) -> str:
        return "NfPredicate(" + self.name + ", " + repr(self.arguments) + ")"


Fact = Predicate # Sematically, a fact is a predicate literal


class Conjunction:
    """
    Conjuctions represent rule tails
    Conjuctions represent also queries 
    """
    def __init__(self,
                 predicates: List[Predicate]) -> None:  # We allow for negation as failure
                                                              # in queries and rule tails
        self.predicates = predicates

    def __str__(self) -> str:
        return ", ".join([str(p) for p in self.predicates])

    def __repr__(self) -> str:
        return "Conjunction(" + ", ".join([repr(p)
                                           for p
                                           in self.predicates]) + ")"

    def __len__(self) -> int:
        return len(self.predicates)

    def __eq__(self, o: object) -> bool:
        if isinstance(o, Conjunction):
            return self.predicates == o.predicates

        return False

    def __iter__(self) -> List[Predicate]:
        return iter(self.predicates)

    def __getitem__(self, index: int) -> Predicate:
        return self.predicates[index]

    def __contains__(self, item: Predicate) -> bool:
        return item in self.predicates

Query = Conjunction # A query is a conjunction

class Rule:
    """
    Rules are made of a head and a tail
    """
    def __init__(self,
                 head: Predicate,
                 tail: Conjunction) -> None:
        self.head = head
        self.tail = tail

    def __eq__(self, o: object) -> bool:
        if isinstance(o, Rule):
            return self.head == o.head and self.tail == o.tail
        else:
            return False

    @property
    def name(self) -> str:
        """
        Returns the name of the rule's head
        """
        return self.head.name

    def __str__(self) -> str:
        return str(self.head) + " :- " + str(self.tail)

    def __repr__(self) -> str:
        return "Rule(" + repr(self.head) + ", " + repr(self.tail) + ")"




if __name__ == "__main__":
    v1 = Variable("X")
    v2 = Variable("X")
    v3 = Variable("Y")

    print(v1 is v2)
    print(hash(v1) == hash(v2))
    print(hash(v1))
    print(hash(v2))
    print(hash(v3))