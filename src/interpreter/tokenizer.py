"""
Module for the tokenizer class
"""
import re
from typing import List, Tuple

class Tokenizer:
    """
    Simple lexer for Prolog-style syntax.
    """
    COMMENT: str = r'%[^\n]*|/\*(.|\n)*?\*/'
    KEYWORDS: List[str] = ['not', 'true']
    PATTERNS: List[Tuple[str, str]] = [
                                        (r'\'[^\']*\'', 'QUOTED_ATOM'),
                                        (r'\_', 'WILDCARD'),
                                        (r'[A-Z_][A-Za-z0-9_]*', 'VARIABLE'),
                                        (r'not', 'NOT'),
                                        (r'true', 'TRUE'),
                                        (r'[a-z][A-Za-z0-9_]*', 'ATOM'),
                                        (r'[1-9][0-9]*|0', 'INTEGER'), # for potential arithmetic, not implemented yet
                                        (r':-', 'IMPLICATION'),
                                        (r',', 'COMMA'),
                                        (r'\.', 'PERIOD'),
                                        (r'\(', 'LPAREN'),
                                        (r'\)', 'RPAREN'),
                                        (r'\[', 'LBRACKET'),
                                        (r'\]', 'RBRACKET'),
                                        (r'\|', 'PIPE'), #TODO: implement list pattern matching; might add head predicate instead
                                        (r'\s+', 'WHITESPACE'),
                                    ]
    def __init__(self) -> None:
        self.tokens: List[Tuple[str, str]] = []

    def tokenize(self, source_code: str) -> None:
        """
        Tokenizes the source code
        """
        self.tokens = []
        source_code: str = re.sub(Tokenizer.COMMENT, '', source_code) # remove comments

        combined: str = '|'.join(f'(?P<{name}>{pattern})'
                                          for pattern, name
                                          in Tokenizer.PATTERNS)

        regex = re.compile(combined)

        i: int = 0

        while i < len(source_code):
            match = regex.match(source_code, i)
            if match is None:
                raise ValueError(f'Invalid syntax: {source_code[i:]}')
            else:
                i = match.end()
                token_type: str = match.lastgroup
                token_value: str = match.group(token_type)

                if token_type != 'WHITESPACE':
                    self.tokens.append((token_type, token_value))
        