#Daniel Palmer -- 4/24/2014

#city file used: http://www.maxmind.com/en/worldcities

import string

cities = []


datafile = open("worldCities.txt")

for row in datafile:
    splitRow = row.split(",")
    cities.append(splitRow[1])

cleanList = list(set(cities))
output = open("cityText.txt", 'w')
for item in cleanList:
    output.write(item + '\n') 
output.close()


    

