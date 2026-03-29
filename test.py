from tokenizer import word_tokenize, sentence_tokenize, ngrams, char_ngrams, word_frequencies, vocabulary, bag_of_words
assert word_tokenize("Hello, world!") == ["hello", "world"]
assert len(word_tokenize("The quick brown fox")) == 4
sents = sentence_tokenize("Hello. How are you? Fine!")
assert len(sents) == 3
bg = ngrams(["a","b","c","d"], 2)
assert bg == [("a","b"),("b","c"),("c","d")]
assert char_ngrams("abc", 2) == ["ab", "bc"]
freq = word_frequencies("the cat the dog the cat")
assert freq["the"] == 3 and freq["cat"] == 2
v = vocabulary(["hello world", "world peace"])
assert "hello" in v and "peace" in v
bow = bag_of_words("hello world hello", v)
assert isinstance(bow, list)
print("tokenizer tests passed")
