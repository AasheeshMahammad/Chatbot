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
    cursor_obj.execute("DROP TABLE IF EXISTS INFO")
    # Creating table
    table = """ CREATE TABLE INFO (
                Name VARCHAR(25) NOT NULL,
                Lap_name VARCHAR(25) NOT NULL,
                Problem VARCHAR(300),
                Serv_centre VARCHAR(100) NOT NULL,
                Serv_addr VARCHAR(200) NOT NULL,
                Apntmnt_dt DATETIME
            ); """

    cursor_obj.execute(table)
    print("Done!")
    # Close the connection
    connection_obj.close()

def insertdb(name,lapname,problem,servcentre,servaddr):
    conn = sqlite3.connect('log.db')
    cur = conn.cursor()
    cur.execute(f"INSERT INTO INFO VALUES ('{name}','{lapname}','{servcentre}','{problem}','{servaddr}', DATE('now','+1 day'))")
    conn.commit()
    conn.close()

def viewdb():
    conn = sqlite3.connect('log.db')
    cur = conn.cursor()
    data = cur.execute('''SELECT * FROM INFO''')
    # print(data[0])
    for row in data:
        print(row)
    conn.close()

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

