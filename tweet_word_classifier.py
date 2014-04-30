import nltk
import csv
import sys
import re
from collections import defaultdict

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
  nouns = {}
  nouns = defaultdict(lambda: 0, nouns)

with open('tweets/No_Retweets.csv', 'rb') as csvfile:
  reader = csv.reader(csvfile)
  i = 0
  for row in reader:
    if i % 5001 == 5000:
      split_list()
    if i > 10001:
      break
    if i%100 == 0:
      sys.stdout.write("\rParsed tweets: %i" % i)
      sys.stdout.flush()
    text = nltk.word_tokenize(row[1])
    tagged = nltk.pos_tag(text)

    # get tagged bigrams that contain a word in the disaster_word list
    rowwordpairs = zip(tagged[0::1], tagged[1::1])
    disasterpairs = []
    for x in rowwordpairs:
      if x[0][0].lower() in disaster_words:
        disasterpairs.append(x[1])
      elif x[1][0].lower() in disaster_words:
        disasterpairs.append(x[0])

    # data type is [("word", "NN"), ("Bob", "NNP")]
    # use "NNP" to find all proper nouns
    current_nouns = filter(lambda x: x[1].startswith('NNP'), disasterpairs)
    # current_nouns = filter(lambda x: x[1].startswith('NN'), tagged)

    #               get the first element of all tuples in array
    for noun in [j[0] for j in current_nouns]:
      if isNotGarbage(noun):
        nouns[noun.lower()] = nouns[noun.lower()] + 1

    i = i+1

print nounsBins
# f = open('propernouns', 'w')
# f.write(repr(nouns))
# f.close()
