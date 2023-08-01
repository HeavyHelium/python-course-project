from typing import List, Union

# could've made those two dataclasses, but decided not to for consistency
class Variable:
    def __init__(self, name: str) -> None:
        self.name = name

    def __str__(self) -> str:
        return self.name
    def __repr__(self) -> str:
        return "Variable(" + self.name + ")"

class Atom:
    def __init__(self, name: str) -> None:
        self.name = name
    def __str__(self) -> str:
        return self.name
    def __repr__(self) -> str:
        return "Atom(" + self.name + ")"
    

class PList: 
    def __init__(self, elements: List[Union[Atom, Variable, "PList"]]) -> None: 
        self.elements = elements
        
    def __str__(self) -> str:
        return '[' + ", ".join([str(e) for e in self.elements]) + ']'

    def __repr__(self) -> str:
        return "PList("'[' + ", ".join([repr(e) for e in self.elements]) + '])'

class Predicate: 
    """
    Class for first order predicate literals
    """
    def __init__(self, name: str, arguments: PList) -> None: 
        self.name = name 
        self.arguments = arguments

    def __str__(self) -> str:
        return self.name + str(self.arguments)
    def __repr__(self) -> str:
        return "Predicate(" + self.name + ", " + repr(self.arguments) + ")"
    
class NfPreficate(Predicate): 
    """
    To support negation as failure
    """
    def __init__(self, name: str, arguments: PList) -> None:
        super().__init__(name, arguments)

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
    def __init__(self, predicates: List[Predicate]) -> None: 
        self.predicates = predicates

    def __str__(self) -> str:
        return ", ".join([str(p) for p in self.predicates])
    
    def __repr__(self) -> str:
        return "Conjunction(" + ", ".join([repr(p) for p in self.predicates]) + ")"

Query = Conjunction # Semantically, a query is a conjunction    

class Rule: 
    """
    Rules are made of a head and a tail
    """
    def __init__(self, head: Predicate, tail: Conjunction) -> None: 
        self.head = head 
        self.tail = tail

    def __str__(self) -> str:
        return str(self.head) + " :- " + str(self.tail)
    
    def __repr__(self) -> str:
        return "Rule(" + repr(self.head) + ", " + repr(self.tail) + ")"


class KnowledgeBase: 
    """
    The knowledge base is made up of rules and facts 
    It represents a Horn program
    """

    def __init__(self): 
        self.clauses: dict[str, List[Union[Fact, Rule]]] = dict()
    
    def add_clause(self, clause: Union[Fact, Rule]) -> None:
        if clause.name not in self.clauses: 
            self.clauses[clause.name] = list()
        self.clauses[clause.name].append(clause)
    



    



if __name__ == "__main__": 
    p = Fact("factorial", PList([Atom("N"), Atom("Res"), PList([Atom("N"), Atom("Res")])]))
    lst = PList([Atom("N"), Atom("Res"), PList([Atom("N"), Atom("Res")])]) 
    print(lst)
    print(repr(lst))
    print(str(p))
    print(repr(p))