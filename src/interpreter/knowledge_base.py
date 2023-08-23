"""
Module to represent the knowledge base
"""

from typing import List, Union

from src.interpreter.terms import Fact, NfPredicate, Rule,\
                                  Predicate, Conjunction

from src.interpreter.unification import unify,\
                                        Substitution,\
                                        SubstitutionApplicator

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
        return False


    def __str__(self) -> str:
        return '\n'.join([str(clause) for clause in self.clauses])

    def __repr__(self) -> str:
        return "KnowledgeBase(" + str(self) + ")"

    def query_single(self, goal: Predicate) -> List[Predicate]:
        """
         Queries the knowledge base
        :Returns: substitued goal heads
        """

        preds: List[Predicate] = []

        if goal.name not in self.clauses:
            raise ValueError("No such predicate: "
                              + str(goal.name)
                              + "\\"
                              + str(len(goal)))

        for clause in self.clauses[goal.name]:
            if isinstance(clause, Fact):
                unif: Substitution = unify(clause, goal)

                if unif is not None:
                    preds.append(SubstitutionApplicator(unif).sub_predicate(goal))

            elif isinstance(clause, Rule):
                unif_head: Substitution = unify(clause.head, goal)

                if unif_head is not None:
                    sa: SubstitutionApplicator = SubstitutionApplicator(unif_head)

                    subbed_head: Predicate = sa.sub_predicate(clause.head)
                    subbed_tail: Conjunction = sa.sub_conjunction(clause.tail)

                    for conj in self.answer_query_rec(subbed_tail, 0, unif_head):
                        subs: Substitution = unify(subbed_tail, conj)
                        if subs is not None:
                            preds.append(SubstitutionApplicator(subs).sub_predicate(subbed_head))

        return preds

    def answer_query_rec(self,
                         goal: Conjunction,
                         idx: int,
                         sub: Substitution) -> List[Conjunction]:
        """
        Answers a query
        :Returns: a list of substitutioned goals
        """
        if idx == len(goal):
            return [SubstitutionApplicator(sub).sub_conjunction(goal)] # we found a solution


        sols: List[Conjunction] = []
        current_pred: Predicate = goal[idx]

        subs_applicator: SubstitutionApplicator = SubstitutionApplicator(sub)

        preds: List[Predicate] = self.query_single(subs_applicator.sub_predicate(current_pred))

        for pred in preds:
            # for each matchings of the current predicate(in the current substitution)
            # we try to match the next predicate

            unif: Substitution = unify(pred, current_pred)

            # compose the current substitution with the new one
            comp_sub: Substitution = subs_applicator.compose(unif, sub)

            if comp_sub is not None:
                # extend the solutions with the ones given the new substitution
                sols.extend(self.answer_query_rec(goal, idx + 1, comp_sub))

        if not preds and isinstance(current_pred, NfPredicate):
            sols.extend(self.answer_query_rec(goal, idx + 1, sub))

        elif preds and isinstance(current_pred, NfPredicate):
            return []

        return sols

    def answer_query(self, goal: Conjunction) -> List[Conjunction]:
        """
        Answers a query
        :Returns: a list of substitutted goals
        """
        sol = self.answer_query_rec(goal, 0, {})

        return sol
