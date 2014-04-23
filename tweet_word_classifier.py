import nltk
import csv
import sys

nouns = set()

with open('All_Tweets.csv', 'rb') as csvfile:
  reader = csv.reader(csvfile)
  i = 0
  for row in reader:
    # if i > 1000:
    #   break
    if i%100 == 0:
      sys.stdout.write("\rParsed tweets: %i" % i)
      sys.stdout.flush()
    text = nltk.word_tokenize(row[1])
    tagged = nltk.pos_tag(text)

    # data type is [("word", "NN"), ("Bob", "NNP")]
    # use "NNP" to find all proper nouns
    current_nouns = filter(lambda x: x[1].startswith('NNP'), tagged)
    # current_nouns = filter(lambda x: x[1].startswith('NN'), tagged)

    #               get the first element of all tuples in array
    for noun in [j[0] for j in current_nouns]:
      nouns.add(noun.lower())

    i = i+1

f = open('propernouns', 'w')
f.write(repr(nouns))
f.close()
