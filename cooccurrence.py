import csv
import operator
from itertools import izip
from collections import defaultdict

import numpy.numarray as na

from pylab import *

order_preserving_hash = {}
order_preserving_hash = defaultdict(lambda: 0, order_preserving_hash)

with open('rough_example_data.csv', 'rb') as csvfile:
  reader = csv.reader(csvfile)
  for row in reader:
    data = row[2].split()

    # [1, 2, 3, 4] -> [(1, 2), (2, 3), (3, 4)]
    wordpairs = zip(data[0::1], data[1::1])

    for pair in wordpairs:
      order_preserving_hash[pair] = order_preserving_hash[pair]+1


sorted_ordered_hash = sorted(order_preserving_hash.iteritems(), key=operator.itemgetter(1))
# reverse the sorted list
sorted_ordered_hash = sorted_ordered_hash[::-1]

labels = [i[0] for i in sorted_ordered_hash]
data = [i[1] for i in sorted_ordered_hash]

print labels
print data

xlocations = na.array(range(len(data)))+0.5
width = 0.5
bar(xlocations, data, width=width)
yticks(range(0, sorted_ordered_hash[0][1]))
xticks(xlocations+ width/2, labels)
xlim(0, xlocations[-1]+width*2)
title("Average Ratings on the Training Set")
gca().get_xaxis().tick_bottom()
gca().get_yaxis().tick_left()

savefig('cooccurringwords.pdf')


