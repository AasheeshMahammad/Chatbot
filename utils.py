import nltk
from nltk.stem.snowball import SnowballStemmer
import numpy as np
import sqlite3

def init_db():
    # Connecting to sqlite
    # connection object
    connection_obj = sqlite3.connect('log.db')
    # cursor object
    cursor_obj = connection_obj.cursor()
    print("Preparing database...",end="")
    # Drop the GEEK table if already exists.
    cursor_obj.execute("DROP TABLE IF EXISTS GEEK")
    # Creating table
    table = """ CREATE TABLE INFO (
                First_Name VARCHAR(25) NOT NULL,
                Last_Name VARCHAR(25),
                Lap_name VARCHAR(25) NOT NULL,
                Serv_centre VARCHAR(100) NOT NULL,
                Serv_contact VARCHAR(20),
                Apntmnt_dt DATETIME
            ); """

    cursor_obj.execute(table)
    print("Done!")
    # Close the connection
    connection_obj.close()

stemmer = SnowballStemmer("english")


def tokenize(sentence):
    return nltk.word_tokenize(sentence)

def stem(word):
    return stemmer.stem(word).lower()

def bag_of_words(tokenized_sentence, words):
    tokenized_sentence = set(map(stem,tokenized_sentence))
    bag = np.zeros(len(words),dtype=np.float32)
    for idx, w in enumerate(words):
        if w in tokenized_sentence:
            bag[idx] = 1
    return bag

