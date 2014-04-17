import csv
import operator
from itertools import izip
from collections import defaultdict

import numpy.numarray as na

import pylab as pl

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

xlocations = na.array(range(len(data)))+0.5
width = 0.5
pl.bar(xlocations, data, width=width)
pl.yticks(range(0, sorted_ordered_hash[0][1]))
pl.xticks(xlocations+ width/2, labels, rotation=70)
pl.xlim(0, xlocations[-1]+width*2)
pl.title("Order preserving word cooccurrence")
pl.gca().get_xaxis().tick_bottom()
pl.gca().get_yaxis().tick_left()

pl.savefig('cooccurringwords.pdf', bbox_inches='tight', pad_inches = 3.0)


