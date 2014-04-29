#!/usr/bin/env python
import fileinput
import csv
import re
from datetime import datetime

capital_count = dict()
date_reached = dict()

# Keeps track of the total number of tweets
tweet_count = 0
baseline = 1000

with open("No_Retweets.csv", "rb") as infile:
	reader = csv.reader(infile, delimiter=",")
	# Ignore first line of csv
   	infile.readline()
	for i,line in enumerate(reader):
		tweet_count += 1
		tweet_time = datetime.strptime(line[0].replace("+0000 ", ""), "%a %b %d %H:%M:%S %Y")
		# Remove special characters
		tweet_body = re.sub('[^\w .]+', '', line[1])

		# Go through each word and increase it's frequency count
		for word in tweet_body.split():
			#x = re.search(r"[A-Z]\S+", word)
			#if x:
			# Only check if first letter is capitalized
			if len(word) > 2:
				if word[0].isupper():
					word = word.lower()
					if word not in capital_count:
						#print(word)
						capital_count[word] = [1, ""]
					else:
						capital_count[word][0] += 1
						if capital_count[word][0] == baseline:
							capital_count[word][1] = tweet_time


sorted_capital_count = capital_count.items()
sorted_capital_count.sort(key = lambda item: item[1])
for word,freq in sorted_capital_count:
	print "Word: %s Freq: %i Time: %s" %(word, freq[0], freq[1])