#!/usr/bin/env python3
"""tokenizer - BPE and word-piece tokenizer."""
import sys,re
from collections import defaultdict,Counter
def get_pairs(word):return[(word[i],word[i+1]) for i in range(len(word)-1)]
def bpe_train(corpus,num_merges=100):
    vocab=defaultdict(int)
    for word in corpus:vocab[" ".join(word)+" </w>"]+=1
    merges=[]
    for _ in range(num_merges):
        pairs=defaultdict(int)
        for word,freq in vocab.items():
            symbols=word.split()
            for i in range(len(symbols)-1):pairs[(symbols[i],symbols[i+1])]+=freq
        if not pairs:break
        best=max(pairs,key=pairs.get);merges.append(best)
        new_vocab={}
        bigram=re.escape(" ".join(best));pattern=re.compile(r"(?<!\S)"+bigram+r"(?!\S)")
        for word in vocab:new_vocab[pattern.sub("".join(best),word)]=vocab[word]
        vocab=new_vocab
    return merges
def bpe_encode(word,merges):
    tokens=list(word)+["</w>"]
    for a,b in merges:
        i=0
        while i<len(tokens)-1:
            if tokens[i]==a and tokens[i+1]==b:tokens[i:i+2]=[a+b]
            else:i+=1
    return tokens
if __name__=="__main__":
    corpus=["low","lower","newest","widest","low","low","newest"]
    merges=bpe_train(corpus,20);print(f"Learned {len(merges)} merges:")
    for a,b in merges[:10]:print(f"  {a} + {b} → {a+b}")
    for word in["low","newer","lowest"]:
        tokens=bpe_encode(word,merges);print(f"  '{word}' → {tokens}")
