import nltk
import csv
import sys

import threading
from multiprocessing import Pool

pool = Pool()
all_nouns = set()

def parse_nouns(tweets):
  for tweet in tweets:
    text = nltk.word_tokenize(tweet)
    tagged = nltk.pos_tag(text)

    # data type is [("word", "NN"), ("something", "NN")]
    current_nouns = filter(lambda x: x[1].startswith('NN'), tagged)

    #               get the first element of all tuples in array
    nouns = Set()
    for noun in [j[0] for j in current_nouns]:
      nouns.add(noun)
    return nouns

def get_tweet_nouns():
  with open('All_Tweets.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile)
    i = 0
    rowbuffer = []
    for row in reader:
      rowbuffer.append(row[1])
      if i%30000 == 0:
        sys.stdout.write("\rWords sent: %i" % i)
        sys.stdout.flush()
        result = pool.apply_async(parse_nouns, [rowbuffer])
        # t1 = threading.Thread(target=parse_nouns(rowbuffer))
        # t1.start()
        # t1.join()
        tweet_nouns = result.get(timeout=600)
        all_nouns.union(tweet_nouns)
        rowbuffer = []
      i = i+1

  print nouns
