import fileinput
import csv
import re

word_count = dict()

# Keeps track of the total number of tweets
tweet_count = 0

with open("All_Tweets.csv", "rb") as infile:
	reader = csv.reader(infile, delimiter=",")
	for i,line in enumerate(reader):
		tweet_count += 1

		# Remove special characters and date
		tweet_body = re.sub('[^\w .]+', '', line[1])

		for word in tweet_body.split():
			if word not in word_count:
				word_count[word] = 1
			else:
				word_count[word] += 1

sorted_word_count = word_count.items()
sorted_word_count.sort(key = lambda item: item[1])
for word,freq in sorted_word_count:
	print "Word: %s Freq: %i" %(word,freq)
