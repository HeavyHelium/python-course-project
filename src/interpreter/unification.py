from typing import Dict
from src.interpreter.terms import Atom, Variable, PList, Predicate, Term


class Unification:
    """
    Encapsulates the process of a unification and querying
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