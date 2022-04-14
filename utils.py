import nltk
from nltk.stem.snowball import SnowballStemmer
import numpy as np


stemmer = SnowballStemmer("english")


def tokenize(sentence):
    return nltk.word_tokenize(sentence)

def stem(word):
    return stemmer.stem(word)

def bag_of_words(tokenized_sentence, words):
    tokenized_sentence = set(map(stem,tokenized_sentence))
    bag = np.zeros(len(words),dtype=np.float32)
    for idx, w in enumerate(words):
        if w in tokenized_sentence:
            bag[idx] = 1
    return bag

