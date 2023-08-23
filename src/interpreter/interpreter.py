"""
The main class of the interpreter
"""

from typing import List
from src.interpreter.terms import Conjunction
from src.interpreter.knowledge_base import KnowledgeBase
from src.interpreter.prolog_parser import PrologParser
from src.interpreter.unification import Substitution, unify

class Interpreter:
    """
    The main class of the interpreter
    """
    def __init__(self, kb: KnowledgeBase = KnowledgeBase()) -> None:
        self.kb: KnowledgeBase = kb

    def load_base(self, content: str) -> None:
        """
        Loads a knowledge base from a string
        """
        prs: PrologParser = PrologParser(content)
        self.kb: KnowledgeBase = prs.parse_program()

    def answer(self, query: str) -> str:
        """
        Queries the knowledge base
        """
        prs: PrologParser = PrologParser(query)
        query: Conjunction = prs.parse_goal()

        answer: str = ''

        solutions: List[Conjunction] = self.kb.answer_query(query)

        if solutions:
            answer += "true.\n"
            for solution in solutions:
                var_bindings: Substitution = query.variables

                subs: Substitution = unify(query, solution)

                for var, val in subs.items():
                    if var.name in var_bindings:
                        var_bindings[var.name] = str(val)


                res: str = ', '.join([f"{var} = {val}"
                                      for var, val
                                      in var_bindings.items()])
                answer += res + "\n"
        else:
            answer = "false."

        return answer
