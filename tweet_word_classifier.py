import nltk
import csv
import sys
import re
from collections import defaultdict

PRINT_PROGRESS = True
PRINT_UNRECOGNIZED_TWEETS = False
BIN_TWEETS = True
TWEET_BIN_SIZE = 10000
TWEET_LIMIT = 40000
DUMP_DICTIONARY = True
DUMP_BINS = True
DICTIONARY_FILE = "wordDict"
BIN_FILE = "wordBins"

# used for binning
nouns = {}
nouns = defaultdict(lambda: 0, nouns)

# used to track full dictionary of nouns
allNouns = {}
allNouns = defaultdict(lambda: 0, allNouns)

nounsBins = []

# Words that the bigram will
disasterWords = ["earthquake", "terremoto", "sismo"]

# filters out all words that have numbers
# or more than 3 of the same letter in a row
regex = re.compile("\d")
regex2 = re.compile("(.)\1{3,}")

# aggressively filters non-useful words
def isNotGarbage(x):
  return ((regex.search(x)==None) and
    ('_' not in x) and
    ("'" not in x) and
    (len(x)<10)and(len(x)>4) and
    (regex.search(x)==None) )

# bins the nouns
def splitList():
  global nouns
  importantNouns = filter(lambda x: nouns[x] > 3, nouns)
  nounsBins.append(importantNouns)
  # print nouns
  nouns = {}
  nouns = defaultdict(lambda: 0, nouns)

# get first element of a list if the list isn't empty
def first(l):
  if len(l) > 0:
    return l[0]
  else:
    return None

# Will print over itself every 100 tweets to show progress
def printProgress(i):
  if PRINT_PROGRESS and i%100 == 0:
    sys.stdout.write("\rParsed tweets: %i" % i)
    sys.stdout.flush()


with open('tweets/No_Retweets.csv', 'rb') as csvfile:
  reader = csv.reader(csvfile)
  i = 0
  for row in reader:
    # end bin if it's reached the TWEET_BIN_SIZE
    if BIN_TWEETS and (i % TWEET_BIN_SIZE == TWEET_BIN_SIZE-1):
      splitList()
    if i > TWEET_LIMIT:
      break

    printProgress(i)

    text = nltk.word_tokenize(row[1])
    tagged = nltk.pos_tag(text)

    # get tagged bigrams that contain a word in the disasterWords list
    rowwordpairs = zip(tagged[0::1], tagged[1::1])
    disasterpairs = []
    printTweet = True
    for x in rowwordpairs:
      # words will be on one side of the tuple or the other, this grabs the
      # tagged word in the bigram that isn't a disaster word
      if first(re.findall("[a-zA-Z]+", x[0][0].lower())) in disasterWords:
        disasterpairs.append(x[1])
        printTweet = False
      elif first(re.findall("[a-zA-Z]+", x[1][0].lower())) in disasterWords:
        disasterpairs.append(x[0])
        printTweet = False

    if PRINT_UNRECOGNIZED_TWEETS and printTweet:
      print row[1]

    # data type is [("word", "NN"), ("Bob", "NNP")]
    # use "NNP" to find all proper nouns
    currentNouns = filter(lambda x: x[1].startswith('NNP'), disasterpairs)

    #               get the first element of all tuples in array
    for noun in [j[0] for j in currentNouns]:
      if isNotGarbage(noun):
        allNouns[noun.lower()] = allNouns[noun.lower()] + 1
        nouns[noun.lower()] = nouns[noun.lower()] + 1

    i = i+1

if DUMP_BINS:
  f = open(BIN_FILE, 'w')
  f.write(repr(nounsBins))
  f.close()

if DUMP_DICTIONARY:
  f = open(DICTIONARY_FILE, 'w')
  f.write(repr(allNouns))
  f.close()
