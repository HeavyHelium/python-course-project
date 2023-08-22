from typing import List
from src.interpreter.terms import Conjunction
from src.interpreter.knowledge_base import KnowledgeBase
from src.interpreter.prolog_parser import PrologParser

class Interpreter: 
    def __init__(self, kb: KnowledgeBase = KnowledgeBase()) -> None:
        self.kb: KnowledgeBase = kb

    def load_base(self, file_path: str) -> None:
        """
        Loads a knowledge base from a file
        """
        content = open(file_path, "r").read()
        prs = PrologParser(content)
        self.kb = prs.parse_program()

    def load_base_direct(self, content: str) -> None:
        """
        Loads a knowledge base from a string
        """
        prs = PrologParser(content)
        self.kb = prs.parse_program()

    def answer(self, query: str) -> List[Conjunction]:
        """
        Queries the knowledge base
        """
        prs = PrologParser(query)
        query = prs.parse_goal()
        print(query)

        print(self.kb.answer_query(query))

        return self.kb.answer_query(query)
