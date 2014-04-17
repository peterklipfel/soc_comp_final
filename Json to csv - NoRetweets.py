# Code by Michael Odbert
#
# Code takes twitter json data and outputs the time and date of a tweet and the tweet text
# The output format is CSV
#
# "BUGS": retweet_count only returns 0. A tweet is considered a retweet if it starts with RT
#         This should be fixed to be more accurate based on json Data

import csv
import json
import simplejson

#Input File
input = open("earthquake_large.json")

#Output of all Tweets minus any retweets
No_Retweets = open("No_Retweets.csv",'wb')
tweetWriter = csv.writer(No_Retweets)
line = input.readline()
tweetWriter.writerow(["dateTime","tweetText"])
while (line) : 
        lineObj = simplejson.loads(line)
        #result = lineObj.get('result')
        
        dateTime = lineObj.get('created_at')
        retweet = lineObj.get("retweet_count")
        tweetText = lineObj.get('text')
        tweetText = tweetText.encode("ascii","ignore")
        if tweetText[0] == 'R' and tweetText[1] == 'T':
                retweet = "1"

        if retweet == '0':
                tweetWriter.writerow([dateTime,tweetText])  
        line = input.readline()

No_Retweets.close()

