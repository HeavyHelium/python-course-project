"""
Module to represent terms and clauses
"""

from typing import List, Union, Dict

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



class Unification:
    """
    Encapsulates the process of a unification
    Unification is the process of finding the most general unifier of two predicate literals
    """
    def __init__(self) -> None:
        self.substitution: Dict[Variable, Term] = {}

    @staticmethod
    def occurs_check(var: Variable, term: Term) -> bool:
        """
        Checks if a variable occurs in a term
        """
        if isinstance(term, Variable):
            return var == term
        if isinstance(term, PList):
            return any(Unification.occurs_check(var, t) for t in term.elements)

        return False


    def substitute(self, term: Term) -> Term:
        """
        Applies the substitution to a term
        """
        return Unification.apply_substitution(self.substitution, term)

    @staticmethod
    def apply_substitution(substitution: Dict[Variable, Term], term: Term) -> Term:
        """
        Applies a substitution to a term
        """
        if isinstance(term, Variable):
            if term in substitution:
                return substitution[term]

            return term
        if isinstance(term, PList):
            return PList([Unification.apply_substitution(substitution, t) for t in term.elements])

        return term

    def unify_variable(self, var: Variable, term: Term) -> bool:
        """
        Unifies a variable with a term
        """
        if var in self.substitution:
            return self.unify(self.substitution[var], term)

        if Unification.occurs_check(var, term):
            return False

        self.substitution[var] = term
        return True
    
    def unify_list(self, l1: PList, l2: PList) -> bool:
        """
        Unifies two lists
        """
        if len(l1.elements) != len(l2.elements):
            return False

        for elem in zip(l1.elements, l2.elements):
            if not self.unify(elem[0], elem[1]):
                return False
        
        return True


    def unify_predicate(self, p1: Predicate, p2: Predicate) -> bool:
        """
        Unifies two predicates
        """
        if p1.name != p2.name:
            return False

        if len(p1.arguments) != len(p2.arguments):
            return False

        
        return self.unify_list(p1.arguments, p2.arguments)
    

    def unify(self, t1: Term, t2: Term) -> bool:
        """
        Finds the most general unifier of two "terms"
        We unify variables with terms 
        Lists with lists
        and predicates with predicates
        """
        if isinstance(t1, Atom) and isinstance(t2, Atom):
            return t1 == t2 # no substitution is performed
        if isinstance(t1, Variable):
            return self.unify_variable(t1, t2)
        if isinstance(t2, Variable):
            return self.unify_variable(t2, t1)
        if isinstance(t1, PList) and isinstance(t2, PList):
            return self.unify_list(t1, t2)
        if isinstance(t1, Predicate) and isinstance(t2, Predicate):
            return self.unify_predicate(t1, t2)
        
        return False


class KnowledgeBase:
    """
    The knowledge base is made up of rules and facts 
    It represents a Horn program
    """

    def __init__(self): 
        self.clauses: dict[str, List[Union[Fact, Rule]]] = {}


    def add_clause(self, clause: Union[Fact, Rule]) -> None:
        """
        Adds a clause to the knowledge base
        """
        if clause.name not in self.clauses:
            self.clauses[clause.name] = []
        self.clauses[clause.name].append(clause)

    def __eq__(self, o: object) -> bool:
        if isinstance(o, KnowledgeBase):
            return self.clauses == o.clauses
        else:
            return False
        
    
    def answer_query(self, query: Query, sub: Dict[Variable, Term]) -> List[Dict[Variable, Term]]:
        """
        Answers a query
        Returns a list of substitutions, which satisfy the query
        """

        # print(f"Goal is: {query}")
        # print(f"Inital sub is: {sub}")

        if len(query) == 0:
            # print(f"Sub is: {sub}")
            return [sub]

        first = query[0]
        # for now we suppose there is no negation as failure

        subs = []



        for clause in self.clauses[first.name]: # for each clause with the same atom as name
            if isinstance(clause, Fact):
                #print(clause)
                #print(f"The parent sub is {sub}")
                #print(f"Unifying {first} with {clause}")
                unif = Unification()
                unif.substitution = sub.copy()
                #print(unif.substitution)
                if unif.unify(first, clause):
                     subs.extend(self.answer_query(query[1:], unif.substitution.copy()))

            elif isinstance(clause, Rule):
                unif = Unification()
                unif.substitution = sub.copy()
                if unif.unify(first, clause.head):
                    val_subs = self.answer_query(clause.tail,
                                                 unif.substitution.copy()) # we answer the tail of the rule
                    #print(f"For rule {clause} we got {val_subs}")
                    for val_sub in val_subs: # for each substitution of the tail
                        res = self.answer_query(query[1:], val_sub.copy()) # we answer the rest of the query
                        # get only relevant substitutions
                        #print(type(res))

                        if res is not None:
                            #print(f"Res is {res}")
                            #print(f"Query is {query}")
                            #print(f"Subs are {subs}")
                            subs.extend(res)

        return subs