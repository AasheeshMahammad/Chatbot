import nltk
from nltk.stem.snowball import SnowballStemmer
stemmer = SnowballStemmer("english")


def tokenize(sentence):
    return nltk.word_tokenize(sentence)

def stem(word):
    return stemmer.stem(word)

def bag_of_words(tokenzied_sentence, words):
    pass
