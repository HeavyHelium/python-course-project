from typing import List, Union
from src.interpreter.tokenizer import Tokenizer

# could've made those two dataclasses, but decided not to for consistency
class Variable:
    def __init__(self, name: str) -> None:
        self.name = name

    def __eq__(self, o: object) -> bool:
        if isinstance(o, Variable):
            return self.name == o.name
        else:
            return False

    def __str__(self) -> str:
        return self.name
    def __repr__(self) -> str:
        return "Variable(" + self.name + ")"

class Atom:
    def __init__(self, name: str) -> None:
        self.name = name

    def __eq__(self, o: object) -> bool:
        if isinstance(o, Atom):
            return self.name == o.name
        else:
            return False
    
    def __str__(self) -> str:
        return self.name
    def __repr__(self) -> str:
        return "Atom(" + self.name + ")"
    

class PList: 
    def __init__(self, elements: List[Union[Atom, Variable, "PList"]]) -> None: 
        self.elements = elements
    
    def __eq__(self, o: object) -> bool:
        if isinstance(o, PList):
            return self.elements == o.elements
        else:
            return False

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
        else:
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
        else:
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
        else:
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
        return self.head.name

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

    def __eq__(self, o: object) -> bool:
        if isinstance(o, KnowledgeBase):
            return self.clauses == o.clauses
        else:
            return False

    
    
    

class PrologParser: 
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
            raise Exception("Expected an atom, variable or list, got " 
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
                raise Exception("Expected a closing bracket, got EOF")
            
            if self.tokens[self.index][0] == "COMMA": 
                self.index += 1
            
            elif self.tokens[self.index][0] != closer: 
                raise Exception("Expected a comma or a closing bracket, got " 
                                + str(self.tokens[self.index][0]))
            else: # closer
                self.index += 1
                return PList(elements)
            
        raise Exception("Expected a closing bracket, got " 
                        + str(self.tokens[self.index][0]))

    def parse_predicate(self) -> Predicate: # positive literal
        """
        Parses a predicate
        """
        if self.tokens[self.index][0] != "ATOM": 
            raise Exception("Expected an atom, got " 
                            + str(self.tokens[self.index][0]))
        name = self.tokens[self.index][1]
        self.index += 1

        if self.tokens[self.index][0] != "LPAREN": 
            raise Exception("Expected an openning parenthesis, got " 
                            + str(self.tokens[self.index][0]))
        
        arguments = self.parse_plist("LPAREN", "RPAREN")
        return Predicate(name, arguments)
    
    def parse_nf_predicate(self) -> NfPredicate: # negative literal
        """
        Parses a negative literal
        """
        if self.tokens[self.index][0] != "NOT": 
            raise Exception("Expected a not, got " 
                            + str(self.tokens[self.index][0]))
        self.index += 1
        
        if self.tokens[self.index][0] != "LPAREN": 
            raise Exception("Expected an openning parenthesis, got " 
                            + str(self.tokens[self.index][0]))
        self.index += 1

        pred: Predicate = self.parse_predicate()

        if self.tokens[self.index][0] != "RPAREN": 
            raise Exception("Expected a closing parenthesis, got " 
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
                raise Exception("Expected a comma or end of clause, got EOF")

            if self.tokens[self.index][0] == "COMMA": 
                self.index += 1
            elif self.tokens[self.index][0] != "PERIOD": 
                raise Exception("Expected a comma or end of clause, got " 
                                + str(self.tokens[self.index][0]))
            
        self.index += 1

        return Conjunction(predicates)
    
    def parse_rule(self) -> Rule:
        """
        Parses a rule
        """
        head: Predicate = self.parse_predicate()
        if self.index >= len(self.tokens):
            raise Exception("Expected implication, got EOF")
        

        if self.tokens[self.index][0] != "IMPLICATION": 
            raise Exception("Expected an implication, got " 
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
            raise Exception("Expected end of clause, got EOF")
        
        if self.tokens[self.index][0] != "PERIOD":
            raise Exception("Expected end of clause, got " 
                            + str(self.tokens[self.index][0]))
        
        self.index += 1
        return Fact(pred.name, pred.arguments)
    
    def parse_program_clause(self) -> Union[Fact, Rule]:
        """
        Parses a clause of a Horn program 
        """
        temp_id = self.index
        try: 
            e: Fact = self.parse_fact()
            return e
        except Exception:
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