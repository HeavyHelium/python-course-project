"""
Module to represent terms and clauses
"""

from typing import List, Union

# could've made those two dataclasses, but decided not to, for consistency
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
        return hash(self.name)

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
    def __init__(self, elements: List[Union[Atom, Variable, "PList"]]) -> None:
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
    
    def __len__(self) -> int:
        return len(self.elements)

    def __str__(self) -> str:
        return '[' + ", ".join([str(e) for e in self.elements]) + ']'

    def __repr__(self) -> str:
        return "PList("'[' + ", ".join([repr(e) for e in self.elements]) + '])'

class Predicate:
    """
    Class for first order predicate literals
    """
    def __init__(self, name: str, arguments: PList) -> None: 
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
    def __init__(self, name: str, arguments: PList) -> None:
        super().__init__(name, arguments)

    def __eq__(self, o: object) -> bool:
        if isinstance(o, NfPredicate):
            return super().__eq__(o)

        return False

    def __str__(self) -> str: 
        return "not(" + super().__str__() + ")"
    
    def __repr__(self) -> str:
        return "NfPredicate(" + self.name + ", " + repr(self.arguments) + ")"



Fact = Predicate # Sematically, a fact is a predicate
                 # In the other way around it's not true.


class Conjunction:
    """
    Conjuctions represent rule tails
    Conjuctions represent also queries 
    """
    def __init__(self, predicates: List[Predicate]) -> None:  # We allow for negation as failure
                                                              # in queries and rule tails
        self.predicates = predicates

    def __str__(self) -> str:
        return ", ".join([str(p) for p in self.predicates])

    def __repr__(self) -> str:
        return "Conjunction(" + ", ".join([repr(p) for p in self.predicates]) + ")"
    
    def __len__(self) -> int:
        return len(self.predicates)

    def __eq__(self, o: object) -> bool:
        if isinstance(o, Conjunction):
            return self.predicates == o.predicates

        return False

Query = Conjunction # Semantically, a query is a conjunction

class Rule:
    """
    Rules are made of a head and a tail
    """
    def __init__(self, head: Predicate, tail: Conjunction) -> None:
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


Term = Union[Atom, Variable, PList]
