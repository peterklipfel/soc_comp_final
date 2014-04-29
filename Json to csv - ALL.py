# Code by Michael Odbert
#
# Code takes twitter json data and outputs the time and date of a tweet and the tweet text
# The output format is CSV
# All new line and return characters are removed from the tweet text
#

import csv
import json
import simplejson

#Input File
input = open("earthquake_large.json")

#Output all Tweets
All_Tweets = open("All_Tweets.csv",'wb')
tweetWriter = csv.writer(All_Tweets)
line = input.readline()
# write the column headers
tweetWriter.writerow(["dateTime","tweetText"])

#loop over each line of the json file
while (line) : 
        #read in the json object
        lineObj = simplejson.loads(line)

        #extract data from the json object
        dateTime = lineObj.get('created_at')
        tweetText = lineObj.get('text')
        tweetText = tweetText.encode("ascii","ignore").replace('\n',' ').replace('\r',' ')      

        #Output to csv
        tweetWriter.writerow([dateTime,tweetText])

        #Advance to the next json line
        line = input.readline()

#Close csv file
All_Tweets.close()
