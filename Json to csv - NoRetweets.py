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

#Output of all Tweets minus any retweets
No_Retweets = open("No_Retweets.csv",'wb')
tweetWriter = csv.writer(No_Retweets)
line = input.readline()
#write the column headers
tweetWriter.writerow(["dateTime","tweetText"])

#loop over each line of the json file
while (line) : 
        #read in the json object
        lineObj = simplejson.loads(line)

        #extract data from the json object
        dateTime = lineObj.get('created_at')
        tweetText = lineObj.get('text')
        tweetText = tweetText.encode("ascii","ignore").replace('\n',' ').replace('\r',' ')
        
        #If retweeted_Status exists in the json object, it is a retweet
        is_retweet = 0
        if "retweeted_status" in lineObj :
                is_retweet = 1
        
        #If the tweet is not a retweet, output to csv
        if is_retweet == 0:
                tweetWriter.writerow([dateTime,tweetText])  

        #Advance to the next json line
        line = input.readline()

#Close csv file
No_Retweets.close()

