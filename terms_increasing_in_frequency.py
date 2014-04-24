#!/usr/bin/env python
import fileinput
import csv
import re
from datetime import datetime
from operator import itemgetter

# Key value pairs that keep track of each word and the number of times it occurs
word_and_freq = dict()
previous_word_and_freq = dict()

# Change this number to tweak how much a term's popularity must be increasing in order to be added
exponent_threshold = 10

# Keeps track of the tweets each time period
tweet_count = 0

# "Stop Words" to ignore in search
stop_words = open("english.stop").read().splitlines() + open("spanish.stop").read().splitlines() + ["rt"]

# Key value pair that will carry all the terms that will eventually be added to the search, along with 
# how many times they are reported as increasing
important_terms_to_watch = dict()
with open("No_Retweets.csv", "rb") as infile:
   reader = csv.reader(infile, delimiter=",")
   # Ignore first line of csv
   infile.readline()
   for i,line in enumerate(reader):
      tweet_count += 1
      tweet_time = datetime.strptime(line[0].replace("+0000 ", ""), "%a %b %d %H:%M:%S %Y")
      # Remove special characters
      tweet_body = re.sub('[^\w .]+', '', line[1]).lower()
 
      # Grab the intial time of the first tweet
      if (i == 0):
         initial_time = tweet_time

      # Go through each word and increase it's frequency count
      for word in tweet_body.split():
         # ignore stop words
         if word not in stop_words:
            if word not in word_and_freq:
               word_and_freq[word] = 1
            else:
               word_and_freq[word] += 1
  
      # After time interval has passed, compare the terms 
      if ((tweet_time - initial_time).seconds > (3 * 60 * 60)):
         if previous_word_and_freq:
            for word,freq in word_and_freq.items():
               if word in previous_word_and_freq:
                  prev_freq = previous_word_and_freq[word]
                  # Calculate the rate of occurance for that word for this 10 mins and last 10 mins
                  freq_rate = (float(freq) / tweet_count)
                  prev_freq_rate = (float(prev_freq) / tweet_count)
                  # If the rate of occurance for the word is increasing by a significant amount, add it to the list
                  if freq_rate > (prev_freq_rate * exponent_threshold) and freq_rate > .1:
                     print "Frequency of word %s is increasing.  %.1f%% -> %.1f%% occurrence rate" % (word, prev_freq_rate * 100, freq_rate * 100)
                     # Keep track of the words that are increasing in frequency
                     if word not in important_terms_to_watch:
                        important_terms_to_watch[word] = 1
                     else:
                        important_terms_to_watch[word] += 1
         # Reset variables for the next time interval
         previous_word_and_freq = word_and_freq
         word_and_freq = dict() 
         initial_time = tweet_time
         tweet_count = 0

# Sort the list of words
important_terms_to_watch = sorted(important_terms_to_watch.items(), key=itemgetter(1))

# Print out final list
print "\nSome terms that are rapidly increasing in frequency which you may want to start monitoring are:"
print "==============================================================================================="
for word,increases in important_terms_to_watch:
   print "\"%s\": %d increases" % (word, increases)
