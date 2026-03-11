#!/usr/bin/env python3
"""BPE tokenizer from scratch."""
import sys, collections, re
def get_pairs(word):
    pairs=collections.Counter()
    for w,freq in word.items():
        symbols=w.split()
        for i in range(len(symbols)-1): pairs[(symbols[i],symbols[i+1])]+=freq
    return pairs
def merge(word,pair):
    new={}; bigram=' '.join(pair); replacement=''.join(pair)
    for w,f in word.items():
        new_w=w.replace(bigram,replacement)
        new[new_w]=f
    return new
text=sys.argv[1] if len(sys.argv)>1 else "the cat sat on the mat the cat ate the rat"
words=collections.Counter(text.split())
word_freq={' '.join(w)+'</w>':f for w,f in words.items()}
num_merges=int(sys.argv[2]) if len(sys.argv)>2 else 10
merges=[]
for i in range(num_merges):
    pairs=get_pairs(word_freq)
    if not pairs: break
    best=max(pairs,key=pairs.get)
    word_freq=merge(word_freq,best)
    merges.append(best)
    print(f"Merge {i+1}: {best[0]} + {best[1]} → {''.join(best)} (freq={pairs[best]})")
print(f"\nVocabulary after {len(merges)} merges:")
vocab=set()
for w in word_freq: vocab.update(w.split())
print(f"  {sorted(vocab)}")
