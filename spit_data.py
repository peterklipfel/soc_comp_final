import csv
import httplib, urllib2
import json
import time
import sys

filename = raw_input('Enter a file name: ')

with open(filename, 'rb') as csvfile:
  reader = csv.reader(csvfile)
  i = 0    
  for row in reader:
    tweet = ""
    if len(row) == 1:
      tweet = ' '.join(row[0].replace('"', '').replace("'", "").split())
    elif len(row) == 2:
      tweet = ' '.join(row[1].replace('"', '').replace("'", "").split())
    else:
      continue

    if tweet != "":
      data = {"tweet":tweet}
      req = urllib2.Request('http://ec2-54-87-190-53.compute-1.amazonaws.com/')
      # req.add_header('Content-Type', 'application/json')

      response = urllib2.urlopen(req, json.dumps(data))

      if i%10 == 0:
        sys.stdout.write("\rParsed tweets: %i" % i)
        sys.stdout.flush()

      i = i+1
    # time.sleep(1)
