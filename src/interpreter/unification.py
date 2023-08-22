"""
Module to represent the unification algorithm
"""
from typing import Dict, List, Union
from functools import reduce

from src.interpreter.terms import Atom, Variable,\
                                  PList, Predicate, Term,\
                                  Conjunction

Substitution = Dict[Variable, Term]

class SubstitutionApplicator:
    """
    Class to apply substitution of different terms
    """
    def __init__(self, subs: Substitution) -> None:
        self.subs = subs


    def sub_term(self, t: Term) -> Term:
        """
        Applies substitution to a term
        """
        if self.subs == {}:
            return t

        if isinstance(t, Variable):
            val: Term = self.subs.get(t)
            return self.sub_term(val) if val else t

        if isinstance(t, PList):
            elems: List[Term] = [self.sub_term(e) for e in t.elements]
            return PList(elems)

        return t # Atom

    def sub_predicate(self, p: Predicate) -> Predicate:
        """
        Applies substitution to a predicate
        """
        return Predicate(p.name,
                         self.sub_term(p.arguments))

    def sub_conjunction(self, c: Conjunction) -> Conjunction:
        """
        Applies substitution to a conjunction
        """
        return Conjunction([self.sub_predicate(p) for p in c])

    @staticmethod
    def compose(sub1: Substitution,
                sub2: Substitution) -> Union[Substitution, None]:
        """
        Composes two substitutions
        :Returns: the composition of the two substitutions
        or None if there are conflicts or one of the substutions is the empty substitution
        """
        if sub1 is None or sub2 is None:
            return None

        sub: Substitution = {}

        for var, term in sub1.items():
            sub[var] = sub2.get(term, term)

        print(sub2)
        for var, term in sub2.items():
            if var not in sub:
                sub[var] = term
            else:
                t1: Term = sub[var]
                unifed: Union[Substitution, None] = unify(t1, term)
                if not unifed is None:
                    for var1, term1 in unifed.items():
                        sub[var1] = term1
                else:
                    return None

        return sub



def occurs_check(var: Variable,
                 term: Term) -> bool:
    """
    Checks if a variable occurs in a term
    """
    if isinstance(term, Variable):
        return var is term

    if isinstance(term, PList):
        return any(occurs_check(var, t) for t in term.elements)

    return False


def unify(t1: Union[Term, Predicate, Conjunction],
          t2: Union[Term, Predicate, Conjunction]) -> Union[Substitution, None]:
    """
    Finds the most general unifier of two terms
    """

    sub: Substitution = None

    if isinstance(t1, Atom) and isinstance(t2, Atom):
        return {} if t1 == t2 else None

    if isinstance(t1, Variable):
        return unify_variable(t1, t2)

    if isinstance(t2, Variable):
        return unify_variable(t2, t1)

    if isinstance(t1, PList) and isinstance(t2, PList):
        return unify_list(t1, t2)

    if isinstance(t1, Predicate) and isinstance(t2, Predicate):
        return unify_predicate(t1, t2)
    
    if isinstance(t1, Conjunction) and isinstance(t2, Conjunction):
        return unify_conjunction(t1, t2)
    
    return None


def unify_variable(var: Variable,
                   term: Term) -> Union[Substitution, None]:
    """
    Unifies a variable with a term
    """
    if var is term:
        return {} # Trivial case, identity substitution

    if occurs_check(var, term):
        return None # Occurs check failed

    subs: Substitution = {}
    subs[var] = term

    return subs


def unify_list(l1: PList,
               l2: PList) -> Union[Substitution, None]:
    """
    Unifies two lists
    """
    if len(l1.elements) != len(l2.elements):
        return None

    subs: List[Substitution] = [unify(t1, t2)
                                for t1, t2
                                in zip(l1.elements, l2.elements)]

    if any(s is None for s in subs):
        return None

    return reduce(SubstitutionApplicator.compose, subs, {}) # Compose all substitutions



def unify_predicate(p1: Predicate,
                    p2: Predicate) -> Union[Substitution, None]:
    """
    Unifies two predicates
    """
    if p1.name != p2.name:
        return None

    if len(p1.arguments) != len(p2.arguments):
        return None


    return unify_list(p1.arguments, p2.arguments)


def unify_conjunction(c1: Conjunction,
                      c2: Conjunction) -> Union[Substitution, None]:
    """
    Unifies two conjunctions
    """
    if len(c1) != len(c2):
        return None

    subs: List[Substitution] = [unify(p1, p2) # Unify predicates
                                for p1, p2
                                in zip(c1, c2)]


    if any(s is None for s in subs):
        return None

    return reduce(SubstitutionApplicator.compose, subs, {}) # Compose all substitutions
