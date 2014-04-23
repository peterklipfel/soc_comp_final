#!/usr/bin/env python
import fileinput
import csv
import re
from datetime import datetime

capital_count = dict()

# Keeps track of the total number of tweets
tweet_count = 0

with open("All_Tweets.csv", "rb") as infile:
	reader = csv.reader(infile, delimiter=",")
	for i,line in enumerate(reader):
		tweet_count += 1

		# Remove special characters
		tweet_body = re.sub('[^\w .]+', '', line[1])

		# Go through each word and increase it's frequency count
		for word in tweet_body.split():
			#x = re.search(r"[A-Z]\S+", word)
			#if x:
			# Only check if first letter is capitalized
			if word[0].isupper():
				word = word.lower()
				if word not in capital_count:
					#print(word)
					capital_count[word] = 1
				else:
					capital_count[word] += 1


sorted_capital_count = capital_count.items()
sorted_capital_count.sort(key = lambda item: item[1])
for word,freq in sorted_capital_count:
	print "Word: %s Freq: %i" %(word, freq)