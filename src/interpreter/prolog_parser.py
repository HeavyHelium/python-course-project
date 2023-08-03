from typing import List, Union, Dict
from src.interpreter.tokenizer import Tokenizer

# could've made those two dataclasses, but decided not to for consistency
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

class KnowledgeBase:
    """
    The knowledge base is made up of rules and facts 
    It represents a Horn program
    """

    def __init__(self): 
        self.clauses: dict[str, List[Union[Fact, Rule]]] = dict()


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
        
    def handle_query(self, query: Query) -> List[Dict[Variable, Term]]:
        """
        Handles a query, for now the query is a predicate, 
        later will implement conjunctions support and negation as failure 
        """
        if query.name not in self.clauses:
            return False

        answers: List[Dict[Variable, Term]] = []

        print(self.clauses[query.name])
        for clause in self.clauses[query.name]:
            unification = Unification()
            print(clause)
            if unification.unify(clause, query):
                answers.append(unification.substitution)

        return answers




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
          or self.tokens[self.index][0] == "INTEGER":
            return self.parse_atom()

        elif self.tokens[self.index][0] == "LBRACKET":
            return self.parse_plist()
        else:
            raise ValueError("Expected an atom, variable or list, got "
                            + str(self.tokens[self.index][0]))

    def parse_plist(self,
                    opener: str = "LBRACKET",
                    closer: str = "RBRACKET") -> PList:
        """
        Parses a list of elements
        """
        elements = list()
        self.index += 1 # skip the opener

        while self.tokens[self.index][0] != closer \
              and self.index < len(self.tokens):

            elements.append(self.parse_argument()) 

            if self.index >= len(self.tokens):
                raise ValueError("Expected a closing bracket, got EOF")

            if self.tokens[self.index][0] == "COMMA":
                self.index += 1

            elif self.tokens[self.index][0] != closer: 
                raise ValueError("Expected a comma or a closing bracket, got "
                                + str(self.tokens[self.index][0]))
            else: # closer
                self.index += 1
                return PList(elements)

        raise ValueError("Expected a closing bracket, got "
                        + str(self.tokens[self.index][0]))

    def parse_predicate(self) -> Predicate: # positive literal
        """
        Parses a predicate
        """
        if self.tokens[self.index][0] != "ATOM":
            raise ValueError("Expected an atom, got "
                            + str(self.tokens[self.index][0]))
        name = self.tokens[self.index][1]
        self.index += 1

        if self.tokens[self.index][0] != "LPAREN":
            raise ValueError("Expected an openning parenthesis, got "
                            + str(self.tokens[self.index][0]))

        arguments = self.parse_plist("LPAREN", "RPAREN")
        return Predicate(name, arguments)

    def parse_nf_predicate(self) -> NfPredicate: # negative literal
        """
        Parses a negative literal
        """
        if self.tokens[self.index][0] != "NOT":
            raise ValueError("Expected a not, got "
                            + str(self.tokens[self.index][0]))
        self.index += 1

        if self.tokens[self.index][0] != "LPAREN":
            raise ValueError("Expected an openning parenthesis, got "
                            + str(self.tokens[self.index][0]))
        self.index += 1

        pred: Predicate = self.parse_predicate()

        if self.tokens[self.index][0] != "RPAREN":
            raise ValueError("Expected a closing parenthesis, got "
                            + str(self.tokens[self.index][0]))
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
                raise ValueError("Expected a comma or end of clause, got EOF")

            if self.tokens[self.index][0] == "COMMA": 
                self.index += 1
            elif self.tokens[self.index][0] != "PERIOD": 
                raise ValueError("Expected a comma or end of clause, got "
                                + str(self.tokens[self.index][0]))
    
        self.index += 1

        return Conjunction(predicates)

    def parse_rule(self) -> Rule:
        """
        Parses a rule
        """
        head: Predicate = self.parse_predicate()
        if self.index >= len(self.tokens):
            raise ValueError("Expected implication, got EOF")


        if self.tokens[self.index][0] != "IMPLICATION": 
            raise ValueError("Expected an implication, got " 
                            + str(self.tokens[self.index][0]))

        self.index += 1
        tail: Conjunction = self.parse_goal()
        return Rule(head, tail)
    
    def parse_fact(self) -> Fact:
        """
        Parses a fact
        """
        pred: Predicate = self.parse_predicate()
        if self.index >= len(self.tokens):
            raise ValueError("Expected end of clause, got EOF")

        if self.tokens[self.index][0] != "PERIOD":
            raise ValueError("Expected end of clause, got " 
                            + str(self.tokens[self.index][0]))

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
        kb = KnowledgeBase()
        while self.index < len(self.tokens):
            clause = self.parse_program_clause()
            kb.add_clause(clause)
        return kb



        









if __name__ == "__main__": 
    p = Fact("factorial", PList([Atom("N"), Atom("Res"), PList([Atom("N"), Atom("Res")])]))
    lst = PList([Atom("N"), Atom("Res"), PList([Atom("N"), Atom("Res")])])
    print(lst)
    print(repr(lst))
    print(str(p))
    print(repr(p))