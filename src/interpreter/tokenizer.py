import re
from typing import List, Tuple

class Tokenizer:
    KEYWORDS = ['not']
    PATTERNS: List[Tuple[str, str]] = [
                                        (r'\'[^\']*\'', 'QUOTED_ATOM'),
                                        (r'[A-Z_][A-Za-z0-9_]*', 'VARIABLE'),
                                        (r'not', 'NOT'),
                                        (r'[a-z][A-Za-z0-9_]*', 'ATOM'),
                                        (r'[1-9][0-9]*|0', 'INTEGER'),
                                        (r':-', 'IMPLICATION'),
                                        (r',', 'COMMA'),
                                        (r'\.', 'PERIOD'),
                                        (r'\(', 'LPAREN'),
                                        (r'\)', 'RPAREN'),
                                        (r'\[', 'LBRACKET'),
                                        (r'\]', 'RBRACKET'),
                                    ]
    def __init__(self) -> None:
        self.tokens: List[Tuple[str, str]] = []

    def tokenize(self, source_code: str) -> None:
        self.tokens = []

        combined_PATTERNS: str = '|'.join(pair[0] for pair in self.PATTERNS)
        regex = re.compile(combined_PATTERNS)

        for match in regex.finditer(source_code):
            token = match.group(0)
            token_type = None
            for pattern, pattern_type in self.PATTERNS:
                if re.match(pattern, token):
                    token_type = pattern_type
                    break
            self.tokens.append((token_type, token))

