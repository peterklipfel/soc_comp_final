#!/usr/bin/env python
import fileinput
import csv
import re
import os
from datetime import datetime

capital_count = dict()
city_count = dict()

# Keeps track of city tweets to help with sorting
tweet_count = 0

# Find whole words within the list of cities
def findWholeWord(w):
    return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search

# List of cites - Thanks Dan!
city_list = open(os.path.dirname(__file__) + "cityText.txt").read().splitlines()
# "Stop Words" to ignore in search - Thanks Greg!
stop_words = open(os.path.dirname(__file__) + "stop_words/english.stop").read().splitlines() + open(os.path.dirname(__file__) + "stop_words/spanish.stop").read().splitlines() + ["rt"]
# "Stop Cities" which includes unuseful words listed as cities in our city list
stop_cities = open(os.path.dirname(__file__) + "stop_words/city.stop").read().splitlines()

# Input a value to check for. I've been testing with 1000
userInput = input("Please enter a baseline value: ")
try:
   baseline = int(userInput)
except ValueError:
   print("That's not an int!")

print "==============================================================================================="

with open("No_Retweets.csv", "rb") as infile:
	reader = csv.reader(infile, delimiter=",")
	# Ignore first line of csv
   	infile.readline()
	for i,line in enumerate(reader):
		tweet_time = datetime.strptime(line[0].replace("+0000 ", ""), "%a %b %d %H:%M:%S %Y")
		# Remove special characters
		tweet_body = re.sub('[^\w .]+', '', line[1])

		# Go through each word and increase it's frequency count
		for word in tweet_body.split():
			# Check if first letter is capitalized and it is a reasonable length
			if len(word) > 2 and word[0].isupper():
				word = word.lower()
				if word not in stop_words:
					if word not in capital_count:
						capital_count[word] = [1, ""]
					else:
						capital_count[word][0] += 1
						if capital_count[word][0] == baseline:
							capital_count[word][1] = tweet_time
							if word in city_list and word not in stop_cities:
								city_count[word] = [tweet_count, tweet_time]
								tweet_count = tweet_count+1

# sort the list of capital words by frequency
sorted_capital_count = capital_count.items()
sorted_capital_count.sort(key = lambda item: item[1])

# sort cites by when they were added to dict (effectively date once baseline was reached)
dated_cities = city_count.items()
dated_cities.sort(key = lambda item: item[1])

# Print everything
print "\nTop Words that Matched our cities list:\n "
for word,date in dated_cities:
	print "City: %15s  Time: %s" %(word, date[1])

print "==============================================================================================="
print "\nWords that hit a baseline of %i and the time they reached it:\n" %(baseline)

for word,freq in sorted_capital_count:
	if freq[1] != "":
		print "Word: %18s Freq: %8i Time: %s" %(word, freq[0], freq[1])