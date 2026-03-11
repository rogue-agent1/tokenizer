#!/usr/bin/env python3
"""tokenizer — Programming language tokenizer/lexer. Zero deps."""
import re

class Token:
    def __init__(self, kind, value, line=0, col=0):
        self.kind, self.value, self.line, self.col = kind, value, line, col
    def __repr__(self): return f"Token({self.kind}, {self.value!r})"

RULES = [
    ('WHITESPACE', r'\s+'),
    ('COMMENT', r'//[^\n]*|/\*[\s\S]*?\*/|#[^\n]*'),
    ('STRING', r'"(?:[^"\\]|\\.)*"|\'(?:[^\'\\]|\\.)*\''),
    ('NUMBER', r'\d+\.?\d*(?:[eE][+-]?\d+)?'),
    ('KEYWORD', r'\b(?:if|else|while|for|return|def|class|import|from|in|not|and|or|true|false|null|let|const|var|fn|pub|struct|enum|match)\b'),
    ('IDENT', r'[a-zA-Z_]\w*'),
    ('OP', r'[+\-*/%]=?|[<>!=]=|&&|\|\||[<>]=?|[!=]=|=>|->|\.\.\.|\.\.|\?\.|\?\?'),
    ('PUNCT', r'[{}()\[\];:,.]'),
    ('UNKNOWN', r'.'),
]

class Lexer:
    def __init__(self, rules=None):
        self.rules = rules or RULES
        self.pattern = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in self.rules)
        self.regex = re.compile(self.pattern)

    def tokenize(self, source, skip_ws=True, skip_comments=True):
        tokens = []
        line, col = 1, 1
        for match in self.regex.finditer(source):
            kind = match.lastgroup
            value = match.group()
            if kind == 'WHITESPACE':
                if not skip_ws: tokens.append(Token(kind, value, line, col))
                lines = value.split('\n')
                if len(lines) > 1:
                    line += len(lines) - 1
                    col = len(lines[-1]) + 1
                else:
                    col += len(value)
                continue
            if kind == 'COMMENT' and skip_comments:
                line += value.count('\n')
                continue
            tokens.append(Token(kind, value, line, col))
            col += len(value)
        return tokens

    def highlight(self, source):
        colors = {
            'KEYWORD': '\033[1;34m', 'STRING': '\033[32m', 'NUMBER': '\033[33m',
            'COMMENT': '\033[90m', 'IDENT': '\033[0m', 'OP': '\033[35m',
            'PUNCT': '\033[0m', 'UNKNOWN': '\033[31m',
        }
        result = []
        for match in self.regex.finditer(source):
            kind = match.lastgroup
            value = match.group()
            color = colors.get(kind, '\033[0m')
            result.append(f"{color}{value}\033[0m")
        return ''.join(result)

def main():
    code = '''
def fibonacci(n):
    # Classic recursive implementation
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

result = fibonacci(10)  // 55
print("fib(10) =", result)
'''
    lexer = Lexer()
    tokens = lexer.tokenize(code)
    print("Tokenizer:\n")
    for tok in tokens:
        print(f"  {tok.kind:<10} {tok.value!r:<20} L{tok.line}:C{tok.col}")
    print(f"\n  Total: {len(tokens)} tokens")
    kinds = {}
    for t in tokens:
        kinds[t.kind] = kinds.get(t.kind, 0) + 1
    print(f"  Breakdown: {dict(sorted(kinds.items()))}")
    print(f"\n  Highlighted:\n{lexer.highlight(code)}")

if __name__ == "__main__":
    main()
