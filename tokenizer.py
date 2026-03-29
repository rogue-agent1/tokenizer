#!/usr/bin/env python3
"""Text tokenizer. Zero dependencies."""
import re

def word_tokenize(text):
    return re.findall(r"\b\w+\b", text.lower())

def sentence_tokenize(text):
    return [s.strip() for s in re.split(r'(?<=[.!?])\s+', text) if s.strip()]

def ngrams(tokens, n):
    return [tuple(tokens[i:i+n]) for i in range(len(tokens)-n+1)]

def char_ngrams(text, n):
    return [text[i:i+n] for i in range(len(text)-n+1)]

def word_frequencies(text):
    from collections import Counter
    return Counter(word_tokenize(text))

def vocabulary(texts):
    vocab = set()
    for t in texts: vocab.update(word_tokenize(t))
    return sorted(vocab)

def bag_of_words(text, vocab):
    words = word_tokenize(text)
    return [words.count(w) for w in vocab]

if __name__ == "__main__":
    text = "The quick brown fox jumps over the lazy dog."
    print(f"Tokens: {word_tokenize(text)}")
    print(f"Bigrams: {ngrams(word_tokenize(text), 2)[:5]}")
