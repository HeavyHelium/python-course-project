"""
Module to represent the knowledge base
"""

from typing import List, Union, Dict
from src.interpreter.terms import Variable, Fact, Rule, Query, Term
from src.interpreter.unification import Unification

class KnowledgeBase:
    """
    The knowledge base is made up of rules and facts 
    It represents a Horn program
    """

    def __init__(self) -> None:
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

        if not first.name in self.clauses:
            raise ValueError("Unknown predicate")

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