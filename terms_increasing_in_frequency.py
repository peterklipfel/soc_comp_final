#!/usr/bin/env python
import fileinput
import csv
import re
from datetime import datetime

# Key value pairs that keep track of each word and the number of times it occurs
word_and_freq = dict()
previous_word_and_freq = dict()

# Change this number to tweak how much a term's popularity must be increasing in order to be adde
exponent_threshold = 10

# Keeps track of the tweets each 10 minute period
tweet_count = 0

# Array that will carry all the terms that will eventually be added to the search
important_terms_to_watch = []
with open("All_Tweets.csv", "rb") as infile:
   reader = csv.reader(infile, delimiter=",")
   for i,line in enumerate(reader):

      tweet_count += 1
      tweet_time = datetime.strptime(line[0].replace("+0000 ", ""), "%a %b %d %H:%M:%S %Y")
      tweet_body = re.sub('[^A-Za-z0-9\n ]+', '', line[1])
 
      # Grab the intial time of the first tweet
      if (i == 0):
         initial_time = tweet_time

      # Go through each word and increase it's frequency count
      for word in tweet_body.split():
         if word not in word_and_freq:
            word_and_freq[word] = 1
         else:
            word_and_freq[word] += 1
  
      # After 10 minutes have past, compart the terms 
      if ((tweet_time - initial_time).seconds > (10 * 60)):
         if previous_word_and_freq:
            for word,freq in word_and_freq.items():
               if word in previous_word_and_freq:
                  prev_freq = previous_word_and_freq[word]
                  # Calculate the rate of occurance for that word for this 10 mins and last 10 mins
                  freq_rate = (float(freq) / tweet_count)
                  prev_freq_rate = (float(prev_freq) / tweet_count)
                  # If the rate of occurance for the word is increasing by a significant amount, add it to the list
                  if freq_rate > (prev_freq_rate * exponent_threshold):
                     print "Frequency of word %s is increasing.  %.1f%% -> %.1f%% of tweets" % (word, prev_freq_rate * 100, freq_rate * 100)
                     important_terms_to_watch.append(word)
         # Reset variables for the next 10 minutes
         previous_word_and_freq = word_and_freq
         word_and_freq = dict() 
         initial_time = tweet_time
         tweet_count = 0

# Make the list of items unique
important_terms_to_watch = set(important_terms_to_watch)

# Print out final list
print "Some terms that are rapidly increasing in frequency which you may want to start monitoring are:"
for word in important_terms_to_watch:
   print word
