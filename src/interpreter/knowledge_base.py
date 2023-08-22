"""
Module to represent the knowledge base
"""

from typing import List, Union

from src.interpreter.terms import Fact, Rule,\
                                  Predicate, Conjunction

from src.interpreter.unification import unify, Substitution, SubstitutionApplicator

class KnowledgeBase:
    """
    The knowledge base is made up of rules and facts 
    It represents a Horn program
    """

    def __init__(self) -> None:
        self.clauses: dict[str, List[Union[Fact, Rule]]] = {}


    def add_clause(self,
                   clause: Union[Fact, Rule]) -> None:
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


    def __str__(self) -> str:
        return '\n'.join([str(clause) for clause in self.clauses])

    def __repr__(self) -> str:
        return "KnowledgeBase(" + str(self) + ")"

    def query_single(self, goal: Predicate) -> List[Predicate]:
        """
         Queries the knowledge base
        :Returns: substituded goal heads
        """

        preds: List[Predicate] = []

        print(f"Querying {goal}")

        for clause in self.clauses[goal.name]:
            if isinstance(clause, Fact):
                print(f"Checking fact {clause}")
                unif: Substitution = unify(clause, goal)
                print(f"unif: {unif}")

                if unif is not None:
                    preds.append(SubstitutionApplicator(unif).sub_predicate(goal))

            elif isinstance(clause, Rule):
                print(f"Checking rule {clause}")
                unif_head: Substitution = unify(clause.head, goal)
                print(f"unif_head: {unif_head}")

                if unif_head is not None:
                    subbed_head: Predicate = SubstitutionApplicator(unif_head).sub_predicate(clause.head)
                    subbed_tail: Conjunction = SubstitutionApplicator(unif_head).sub_conjunction(clause.tail)
                    print(f"subbed_head: {subbed_head}")
                    print(f"subbed_tail: {subbed_tail}")

                    for conj in self.answer_query_rec(subbed_tail, 0, unif_head):
                        subs: Substitution = unify(subbed_tail, conj)

                        if subs is not None:
                            preds.append(SubstitutionApplicator(subs).sub_predicate(subbed_head))

            print(f"Given goal {goal}, found {preds}")
        return preds

    def answer_query_rec(self,
                         goal: Conjunction,
                         id: int,
                         sub: Substitution) -> List[Conjunction]:
        """
        Answers a query
        :Returns: a list of substitutioned goals
        """
        if id == len(goal):
            return [SubstitutionApplicator(sub).sub_conjunction(goal)] # we found a solution
        
        sols: List[Conjunction] = []
        current_pred: Predicate = goal[id]
        print(f"Current predicate: {current_pred}")

        subs_applicator: SubstitutionApplicator = SubstitutionApplicator(sub)
        print(f"Current substitution: {sub}")


        for pred in self.query_single(subs_applicator.sub_predicate(current_pred)):
            # for each matchings of the current predicate(in the current substitution)
            # we try to match the next predicate

            unif: Substitution = unify(pred, current_pred)
            print(f"for predicate {pred} and {current_pred}, found {unif}")

            comp_sub: Substitution = subs_applicator.compose(unif, sub) # compose the current substitution with the new one

            if comp_sub is not None:
                # go your own way
                sols.extend(self.answer_query_rec(goal, id + 1, comp_sub)) # extend the solutions with the ones given the new substitution
                print(f"Given goal {goal}, found {sols}")
        
        print(f"Given goal {goal}, found {sols}")

        return sols

    def answer_query(self, goal: Conjunction) -> List[Conjunction]:
        """
        Answers a query
        :Returns: a list of substitutted goals
        """
        return self.answer_query_rec(goal, 0, {})








        



        