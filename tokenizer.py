#!/usr/bin/env python3
"""tokenizer - Text tokenizer with BPE training, vocab building, and encoding/decoding."""
import sys, re, collections

class BPETokenizer:
    def __init__(self):
        self.merges = []
        self.vocab = {}
    
    def _get_pairs(self, words):
        pairs = collections.Counter()
        for word, freq in words.items():
            syms = word.split()
            for i in range(len(syms) - 1):
                pairs[(syms[i], syms[i+1])] += freq
        return pairs
    
    def train(self, text, vocab_size=256):
        word_freq = collections.Counter()
        for word in re.findall(r'\S+', text.lower()):
            word_freq[' '.join(word) + ' </w>'] += 1
        
        # Base vocab: all characters
        self.vocab = {chr(i): i for i in range(256) if chr(i).isprintable()}
        idx = len(self.vocab)
        
        while idx < vocab_size:
            pairs = self._get_pairs(word_freq)
            if not pairs: break
            best = max(pairs, key=pairs.get)
            self.merges.append(best)
            self.vocab[best[0] + best[1]] = idx
            idx += 1
            
            new_freq = {}
            bigram = ' '.join(best)
            replacement = ''.join(best)
            for word, freq in word_freq.items():
                new_word = word.replace(bigram, replacement)
                new_freq[new_word] = freq
            word_freq = new_freq
        
        return len(self.vocab)
    
    def encode(self, text):
        tokens = []
        for word in re.findall(r'\S+', text.lower()):
            syms = list(word) + ['</w>']
            while len(syms) > 1:
                merged = False
                for a, b in self.merges:
                    i = 0
                    while i < len(syms) - 1:
                        if syms[i] == a and syms[i+1] == b:
                            syms[i:i+2] = [a + b]
                            merged = True
                        else:
                            i += 1
                if not merged: break
            tokens.extend(syms)
        return tokens
    
    def stats(self):
        return {"vocab_size": len(self.vocab), "merges": len(self.merges)}

def cmd_train(args):
    vocab_size = int(args[0]) if args else 300
    text = sys.stdin.read()
    tok = BPETokenizer()
    sz = tok.train(text, vocab_size)
    words = re.findall(r'\S+', text)
    encoded = tok.encode(text)
    ratio = len(encoded) / len(text) if text else 0
    print(f"Trained BPE tokenizer:")
    print(f"  Vocab size:  {sz}")
    print(f"  Merges:      {len(tok.merges)}")
    print(f"  Input chars: {len(text):,}")
    print(f"  Input words: {len(words):,}")
    print(f"  Tokens:      {len(encoded):,}")
    print(f"  Compression: {ratio:.2f} tokens/char")
    print(f"\nTop merges:")
    for i, (a, b) in enumerate(tok.merges[:15]):
        print(f"  {i+1:>3}. '{a}' + '{b}' → '{a+b}'")
    print(f"\nSample encoding (first 30 tokens):")
    print(f"  {' | '.join(encoded[:30])}")

def cmd_chars(args):
    text = sys.stdin.read()
    freq = collections.Counter(text)
    total = len(text)
    print(f"{'Char':<8} {'Count':>8} {'Freq':>8}")
    print("-" * 26)
    for ch, c in freq.most_common(30):
        display = repr(ch) if ch in '\n\t\r ' else ch
        print(f"{display:<8} {c:>8} {c/total:>8.2%}")
    print(f"\nUnique chars: {len(freq)} | Total: {total:,}")

def main():
    if len(sys.argv) < 2 or sys.argv[1] in ('-h','--help'):
        print("Usage: tokenizer.py <command> [opts] < input.txt\n\nCommands:\n  train [vocab_size]  Train BPE tokenizer on stdin\n  chars               Character frequency analysis"); return
    cmds = {"train": cmd_train, "chars": cmd_chars}
    cmd = sys.argv[1]
    if cmd in cmds: cmds[cmd](sys.argv[2:])
    else: print(f"Unknown: {cmd}")

if __name__ == "__main__": main()
