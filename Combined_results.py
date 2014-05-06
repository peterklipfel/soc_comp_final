# Combine All Results
#
#
# Take each piece of code, run it on a common data set, output individual results, output combined results
#
#
import fileinput
import csv
import re
from math import fabs, floor
from datetime import datetime, timedelta
import os
import sys
import time
from operator import itemgetter


byron = []
willie =[]
greg = []
peter= []


# Import csv files (give options for 1=all_chile 2=no_retweets_chile 3=no_retweets_guatemala 4=no_retweets_tornado)
userInput = input("What file would you like to use?(1=all_chile 2=no_retweets_chile 3=no_retweets_guatemala 4=no_retweets_tornado): ")
if userInput == 1:
	inputfile = open("All_Tweets_chile.csv")
elif userInput == 2:
	inputfile = open("No_Retweets_chile.csv")
elif userInput == 3:
	inputfile = open("No_Retweets_guatemala.csv")
elif userInput == 4:
	inputfile = open("No_Retweets_tornado.csv")


# Change this number to tweak how much a term's popularity must be increasing in order to be added
baseline = raw_input("Enter a basline (How many times a term is used before it is added)(Default 1000): ")
if baseline == "":
   baseline = 1000
baseline = float(baseline)

# Change this number to tweak how much a term's popularity must be increasing in order to be added
exponent_threshold = raw_input("Enter an exponent threshold (By how many times much a number increase in popularity to be added)(Default 10): ")
if exponent_threshold == "":
   exponent_threshold = 10
exponent_threshold = float(exponent_threshold)

# Change this number to tweak the percentage of occurrence a term must have among tweets in order to 
# be added
frequency_threshold = raw_input("Enter a frequency threshold (What proportion of tweets must contain the term before it is added)(Default 0.1): ")
if frequency_threshold == "":
   frequency_threshold = 0.1
frequency_threshold = float(frequency_threshold)

# Change this number to tweak the time intervals that are compared
time_interval = raw_input("Enter a time interval in minutes (How long should terms be collected before comparing to the previous interval)(Default 180): ")
if time_interval == "":
   time_interval = 3 * 60 * 60
else:
   time_interval = int(time_interval) * 60 


# Run Byrons code (allow for variables)
# Save to a variable/file
word_count = dict()
date_reached = dict()
date_last = dict() # Last occurence of word

# Keeps track of the total number of tweets
tweet_count = 0
stopwords = 1

with inputfile as infile:
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
			if len(word) > 3: # Length greater than 3
				if word not in word_count:
					word_count[word] = [1,tweet_time,tweet_time, 0]
				else:
					word_count[word][0] += 1
					# Time when trending word hits threshold
					if word_count[word][0] == baseline:
						word_count[word][1] = tweet_time
					# Last time trending word was used
					if word_count[word][0] > baseline:
						word_count[word][2] = tweet_time
				x = word_count[word][2] - word_count[word][1]
				y = floor(fabs(x.total_seconds() / 3600))
				if y > 0:
					z = word_count[word][0] / y
				word_count[word][3] = y

sorted_word_count = word_count.items()
sorted_word_count.sort(key = lambda item: item[1])
for word,freq in sorted_word_count:
	if freq[0] > baseline:
		#print "Word: %s Freq: %i Baseline Time: %s Avg: %s uses per minute" %(word,freq[0], freq[1], freq[3])
		#print word
		byron.insert(0,word)



# Run Willie's code (allow for variables)
# Save to a variable/file
#!/usr/bin/env python
if userInput == 1:
	inputfile = open("All_Tweets_chile.csv")
elif userInput == 2:
	inputfile = open("No_Retweets_chile.csv")
elif userInput == 3:
	inputfile = open("No_Retweets_guatemala.csv")
elif userInput == 4:
	inputfile = open("No_Retweets_tornado.csv")

capital_count = dict()
city_count = dict()

# Keeps track of city tweets to help with sorting
tweet_count = 0

# Find whole words within the list of cities
def findWholeWord(w):
    return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search

# List of cites - Thanks Dan!
city_list = open("cityText.txt").read().splitlines()
# "Stop Words" to ignore in search - Thanks Greg!
stop_words = open("stop_words/english.stop").read().splitlines() + open("stop_words/spanish.stop").read().splitlines() + ["rt"]
# "Stop Cities" which includes unuseful words listed as cities in our city list
stop_cities = open("stop_words/city.stop").read().splitlines()

# Input a value to check for. I've been testing with 1000
# userInput = input("Please enter a baseline value: ")
# try:
#   baseline = int(userInput)
# except ValueError:
#   print("That's not an int!")

#print "==============================================================================================="

with inputfile as infile:
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
#print "\nTop Words that Matched our cities list:\n "
#for word,date in dated_cities:
    #print "City: %15s  Time: %s" %(word, date[1])
    #willie.insert(0,word)


#print "==============================================================================================="
#print "\nWords that hit a baseline of %i and the time they reached it:\n" %(baseline)

for word,freq in sorted_capital_count:
    if freq[1] != "":
        #print "Word: %18s Freq: %8i Time: %s" %(word, freq[0], freq[1])
        #print word
        willie.insert(0,word)
        
if userInput == 1:
	inputfile = open("All_Tweets_chile.csv")
elif userInput == 2:
	inputfile = open("No_Retweets_chile.csv")
elif userInput == 3:
	inputfile = open("No_Retweets_guatemala.csv")
elif userInput == 4:
	inputfile = open("No_Retweets_tornado.csv")
# Run Greg's code (allow for variables)
# Save to a variable/file
#!/usr/bin/env python
# Key value pairs that keep track of each word and the number of times it occurs
word_and_freq = dict()
previous_word_and_freq = dict()



# Keeps track of the tweets each time period
tweet_count = 0

# "Stop Words" to ignore in search
stop_words = open(os.path.dirname(__file__) + "/stop_words/english.stop").read().splitlines() + open(os.path.dirname(__file__) + "/stop_words/spanish.stop").read().splitlines() + ["rt"]

# Key value pair that will carry all the terms that will eventually be added to the search, along with 
# how many times they are reported as increasing
important_terms_to_watch = dict()

# Term and it's total occurrences
term_total_occurrences = dict()
with inputfile as infile:
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
         word = word.rstrip(".")
         # ignore stop words
         if word not in stop_words:
            if word not in word_and_freq:
               word_and_freq[word] = 1
            else:
               word_and_freq[word] += 1
               # keep track of the total occurrences of each word
               if word not in term_total_occurrences:
                  term_total_occurrences[word] = 1
               else:
                  term_total_occurrences[word] += 1
  
      # After time interval has passed, compare the terms 
      if ((tweet_time - initial_time).seconds > time_interval):
         if previous_word_and_freq:
            for word,freq in word_and_freq.items():
               if word in previous_word_and_freq:
                  prev_freq = previous_word_and_freq[word]
                  # Calculate the rate of occurance for that word for this 10 mins and last 10 mins
                  freq_rate = (float(freq) / tweet_count)
                  prev_freq_rate = (float(prev_freq) / tweet_count)
                  # If the rate of occurance for the word is increasing by a significant amount, add it to the list
                  if freq_rate > (prev_freq_rate * exponent_threshold) and freq_rate > frequency_threshold:
                     #print "Frequency of word %15s is increasing.  %.1f%% -> %.1f%% occurrence rate" % (word, prev_freq_rate * 100, freq_rate * 100)
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
#print "\nTop Terms Increasing in Frequency:"
#print "==============================================================================================="
for word,increases in important_terms_to_watch:
   #print "%15s: %5d increases. (%7d total occurrences)" % (word, increases, term_total_occurrences[word])
   #print word
   greg.insert(0,word)


# Combine all the resutls and union them

outfile = open("Output.txt", 'w')
for i in range (len(byron)):
    count = 1
    if byron[i] in willie:
        count += 1
    if byron [i] in greg:
        count += 1
    if count == 3:
        #print byron[i]
        outfile.write(byron[i])
        outfile.write('\n')

outfile.close()





