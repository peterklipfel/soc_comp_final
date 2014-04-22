# Derived from the Capital Word Count script, aimed to keep uniform
import fileinput
import csv
import re
from collections import defaultdict

word_count = dict()
word_dates = defaultdict(list)

# Keeps track of the total number of tweets
tweet_count = 0

with open("All_Tweets.csv", "rb") as infile:
	reader = csv.reader(infile, delimiter=",")
	for i,line in enumerate(reader):
		tweet_count += 1
		current_date = line[0]
		#print current_date

		# Remove special characters and date
		tweet_body = re.sub('[^\w .]+', '', line[1])

		for word in tweet_body.split():
			if word not in word_count:
				word_count[word] = 1
				word_dates[word] = current_date  #  Add whole date string
				#print "Added %s" %(word)
			else:
				word_count[word] += 1
				word_dates[word] += current_date  #  Add Whole Date String
				print "%s: %s" %(word,word_dates[word])

sorted_word_count = word_count.items()
sorted_word_count.sort(key = lambda item: item[1])
for word,freq in sorted_word_count:
	print "Word: %s Freq: %i" %(word,freq)

sorted_word_cdate = word_dates.sortd()
for line in sorted_word_dates:
	print line