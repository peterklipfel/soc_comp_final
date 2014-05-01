import nltk
import csv
import sys
import re
from collections import defaultdict

PRINT_PROGRESS = True
PRINT_UNRECOGNIZED_TWEETS = True
BIN_TWEETS = True
TWEET_BIN_SIZE = 10000
TWEET_LIMIT = 40000

# nouns = set()
nouns = {}
nouns = defaultdict(lambda: 0, nouns)

nounsBins = []

disaster_words = ["earthquake", "tsunami", "sismo"]
regex = re.compile("\d")
regex2 = re.compile("(.)\1{3,}")

def isNotGarbage(x):
  return ((regex.search(x)==None) and
    ('_' not in x) and
    ("'" not in x) and
    (len(x)<10)and(len(x)>4) and
    (regex.search(x)==None) )

def split_list():
  global nouns
  important_nouns = filter(lambda x: nouns[x] > 3, nouns)
  nounsBins.append(important_nouns)
  # print nouns
  nouns = {}
  nouns = defaultdict(lambda: 0, nouns)

def first(l):
  if len(l) > 0:
    return l[0]
  else:
    return None


with open('tweets/No_Retweets.csv', 'rb') as csvfile:
  reader = csv.reader(csvfile)
  i = 0
  for row in reader:
    if BIN_TWEETS and (i % TWEET_BIN_SIZE == TWEET_BIN_SIZE-1):
      split_list()
    if i > TWEET_LIMIT:
      break
    if PRINT_PROGRESS and i%100 == 0:
      sys.stdout.write("\rParsed tweets: %i" % i)
      sys.stdout.flush()
    text = nltk.word_tokenize(row[1])
    tagged = nltk.pos_tag(text)

    # get tagged bigrams that contain a word in the disaster_word list
    rowwordpairs = zip(tagged[0::1], tagged[1::1])
    disasterpairs = []
    print_tweet = True
    for x in rowwordpairs:
      if first(re.findall("[a-zA-Z]+", x[0][0].lower())) in disaster_words:
        disasterpairs.append(x[1])
        print_tweet = False
      elif first(re.findall("[a-zA-Z]+", x[1][0].lower())) in disaster_words:
        disasterpairs.append(x[0])
        print_tweet = False

    if print_tweet:
      print row[1]

    # data type is [("word", "NN"), ("Bob", "NNP")]
    # use "NNP" to find all proper nouns
    current_nouns = filter(lambda x: x[1].startswith('NNP'), disasterpairs)
    # current_nouns = filter(lambda x: x[1].startswith('NN'), tagged)

    #               get the first element of all tuples in array
    for noun in [j[0] for j in current_nouns]:
      if isNotGarbage(noun):
        nouns[noun.lower()] = nouns[noun.lower()] + 1

    i = i+1

# print nounsBins
print set(nounsBins[0]).union(set(nounsBins[1])).union(set(nounsBins[2])).union(set(nounsBins[3]))
# f = open('propernouns', 'w')
# f.write(repr(nouns))
# f.close()
