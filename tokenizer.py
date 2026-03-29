#!/usr/bin/env python3
"""tokenizer - Configurable lexical tokenizer with regex rules."""
import sys, re

class Token:
    def __init__(self, type, value, pos):
        self.type = type
        self.value = value
        self.pos = pos
    def __repr__(self):
        return f"Token({self.type}, {self.value!r})"

class Tokenizer:
    def __init__(self, rules, skip=None):
        self.rules = [(name, re.compile(pattern)) for name, pattern in rules]
        self.skip = set(skip or [])
    def tokenize(self, text):
        tokens = []
        pos = 0
        while pos < len(text):
            match = None
            for name, regex in self.rules:
                m = regex.match(text, pos)
                if m:
                    if name not in self.skip:
                        tokens.append(Token(name, m.group(), pos))
                    pos = m.end()
                    match = True
                    break
            if not match:
                raise SyntaxError(f"Unexpected char {text[pos]!r} at pos {pos}")
        return tokens

def test():
    rules = [
        ("NUMBER", r"\d+\.?\d*"),
        ("IDENT", r"[a-zA-Z_]\w*"),
        ("OP", r"[+\-*/=<>!]=?"),
        ("LPAREN", r"\("),
        ("RPAREN", r"\)"),
        ("WS", r"\s+"),
        ("STRING", r'"[^"]*"'),
    ]
    t = Tokenizer(rules, skip=["WS"])
    tokens = t.tokenize('x = 42 + y * 3.14')
    types = [tk.type for tk in tokens]
    assert types == ["IDENT", "OP", "NUMBER", "OP", "IDENT", "OP", "NUMBER"]
    assert tokens[0].value == "x"
    assert tokens[2].value == "42"
    # string
    tokens2 = t.tokenize('"hello" + "world"')
    assert tokens2[0].type == "STRING"
    assert tokens2[0].value == '"hello"'
    print("OK: tokenizer")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test()
    else:
        print("Usage: tokenizer.py test")
