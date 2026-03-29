#!/usr/bin/env python3
"""Text tokenizer — word, sentence, BPE-style subword."""
import re, sys
from collections import Counter

class WordTokenizer:
    def tokenize(self, text):
        return re.findall(r"\w+|[^\w\s]", text)
    def detokenize(self, tokens):
        return " ".join(tokens)

class SentenceTokenizer:
    def tokenize(self, text):
        return [s.strip() for s in re.split(r'(?<=[.!?])\s+', text) if s.strip()]

class BPETokenizer:
    def __init__(self, vocab_size=100):
        self.vocab_size = vocab_size; self.merges = []
    def _get_pairs(self, words):
        pairs = Counter()
        for word, freq in words.items():
            symbols = list(word)
            for i in range(len(symbols)-1):
                pairs[(symbols[i], symbols[i+1])] += freq
        return pairs
    def train(self, text):
        word_freqs = Counter(text.lower().split())
        words = {" ".join(w) + " _": freq for w, freq in word_freqs.items()}
        for _ in range(self.vocab_size):
            pairs = self._get_pairs(words)
            if not pairs: break
            best = max(pairs, key=pairs.get)
            self.merges.append(best)
            new_words = {}
            bigram = " ".join(best); replacement = "".join(best)
            for word, freq in words.items():
                new_words[word.replace(bigram, replacement)] = freq
            words = new_words
    def tokenize(self, word):
        symbols = list(word.lower()) + ["_"]
        for a, b in self.merges:
            i = 0
            while i < len(symbols) - 1:
                if symbols[i] == a and symbols[i+1] == b:
                    symbols = symbols[:i] + [a+b] + symbols[i+2:]
                else: i += 1
        return symbols

if __name__ == "__main__":
    text = "The quick brown fox jumps over the lazy dog. The dog barked loudly! Did the fox escape?"
    wt = WordTokenizer(); st = SentenceTokenizer()
    print(f"Word tokens: {wt.tokenize(text)[:10]}...")
    print(f"Sentences: {st.tokenize(text)}")
    corpus = "low lower newest newest widest widest wider wider new new low low"
    bpe = BPETokenizer(vocab_size=20); bpe.train(corpus)
    print(f"\nBPE merges: {bpe.merges[:10]}")
    for word in ["lowest", "newer", "wide"]:
        print(f"  BPE('{word}'): {bpe.tokenize(word)}")
