#!/usr/bin/env python
import fileinput
import csv
import re
from datetime import datetime, timedelta

word_count = dict()
date_reached = dict()
date_last = dict() # Last occurence of word

# Keeps track of the total number of tweets
tweet_count = 0
baseline = 1000
stopwords = 1

with open("No_Retweets.csv", "rb") as infile:
	reader = csv.reader(infile, delimiter=",")
	# Ignore first line of csv
	infile.readline()
	# Runs through each line of input csv
	for i,line in enumerate(reader):
		tweet_count += 1
		tweet_time = datetime.strptime(line[0].replace("+0000 ", ""), "%a %b %d %H:%M:%S %Y")


		# Remove special characters and date
		tweet_body = re.sub('[^\w .]+', '', line[1])

		# Go through each word and increase its frequency count
		for word in tweet_body.split():
			word = word.lower()
			if len(word) > 3: # Length greater than 3 (and not stop word?)
				if word not in word_count:
					word_count[word] = [1, "", ""]
				else:
					word_count[word][0] += 1
					# Time when trending word hits threshold
					if word_count[word][0] == baseline:
						word_count[word][1] = tweet_time
					# Last time trending word was used
					if word_count[word][0] > baseline:
						word_count[word][2] = tweet_time

sorted_word_count = word_count.items()
sorted_word_count.sort(key = lambda item: item[1])
for word,freq in sorted_word_count:
	if freq[0] > baseline:
		print "Word: %s Freq: %i Time: %s Last Used: %s" %(word,freq[0], freq[1], freq[2])
