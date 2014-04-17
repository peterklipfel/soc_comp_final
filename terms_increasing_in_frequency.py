#!/usr/bin/env python
import fileinput

word_and_freq = dict()
previous_word_and_freq = dict()
exponent_threshold = 1.8
with open("rough_example_data.csv") as infile:
   for i, line in enumerate(infile):
      csv_fields = line.split(",")
      tweet_time = int(csv_fields[0])
      tweet_body = csv_fields[2].replace("\"", "")

      if (i == 0):
         initial_time = tweet_time

      for word in tweet_body.split():
         if word not in word_and_freq:
            word_and_freq[word] = 1
         else:
            word_and_freq[word] += 1
   
      if ((tweet_time - initial_time) == 10):
         if previous_word_and_freq:
            for key, value in word_and_freq.items():
               if key in previous_word_and_freq:
                  if value > (previous_word_and_freq[key] * exponent_threshold):
                     print "Frequency of word %s is increasing" % key
         previous_word_and_freq = word_and_freq
         word_and_freq = dict() 
         initial_time = tweet_time
