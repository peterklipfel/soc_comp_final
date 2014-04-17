# Code by Michael Odbert
#
# Code takes twitter json data and outputs the time and date of a tweet and the tweet text
# The output format is CSV

import csv
import json
import simplejson

#Input File
input = open("earthquake_large.json")

#Output all Tweets
All_Tweets = open("All_Tweets.csv",'wb')
tweetWriter = csv.writer(All_Tweets)
line = input.readline()
tweetWriter.writerow(["dateTime","tweetText"])
while (line) : 
        lineObj = simplejson.loads(line)
        #result = lineObj.get('result')

        dateTime = lineObj.get('created_at')
        tweetText = lineObj.get('text')
        tweetText = tweetText.encode("ascii","ignore")       

        tweetWriter.writerow([dateTime,tweetText])
        line = input.readline()

All_Tweets.close()
