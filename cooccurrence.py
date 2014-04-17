import csv
import operator
from itertools import izip
from collections import defaultdict

import networkx as nx
import numpy.numarray as na

import pylab as pl

def get_order_preserving_list():
  allwordpairs = []
  with open('rough_example_data.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
      data = row[2].split()

      # [1, 2, 3, 4] -> [(1, 2), (2, 3), (3, 4)]
      rowwordpairs = zip(data[0::1], data[1::1])
      allwordpairs.extend(rowwordpairs)
  return allwordpairs

def get_order_preserving_hash():
  order_preserving_hash = {}
  order_preserving_hash = defaultdict(lambda: 0, order_preserving_hash)

  for pair in get_order_preserving_list():
    order_preserving_hash[pair] = order_preserving_hash[pair]+1


  sorted_ordered_hash = sorted(order_preserving_hash.iteritems(), key=operator.itemgetter(1))
  # reverse the sorted list
  return sorted_ordered_hash[::-1]

def bar_graph():
  sorted_ordered_hash = get_order_preserving_hash()
  print sorted_ordered_hash
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

# credit: https://www.udacity.com/wiki/creating_network_graphs_with_python
def network(graph, labels=None, graph_layout='shell',
            node_size=1600, node_color='blue', node_alpha=0.3,
            node_text_size=12,
            edge_color='blue', edge_alpha=0.3, edge_tickness=1,
            edge_text_pos=0.3,
            text_font='sans-serif'):
  # create network
  G=nx.Graph()

  # add edges
  for edge in graph:
    G.add_edge(edge[0], edge[1])

  # these are different layouts for the network you may try
  # shell seems to work best
  if graph_layout == 'spring':
    graph_pos=nx.spring_layout(G, iterations=500)
  elif graph_layout == 'spectral':
    graph_pos=nx.spectral_layout(G)
  elif graph_layout == 'random':
    graph_pos=nx.random_layout(G)
  else:
    graph_pos=nx.shell_layout(G)

  # draw graph
  nx.draw_networkx_nodes(G,graph_pos,node_size=node_size, 
                         alpha=node_alpha, node_color=node_color)
  nx.draw_networkx_edges(G,graph_pos,width=edge_tickness,
                         alpha=edge_alpha,edge_color=edge_color)
  nx.draw_networkx_labels(G, graph_pos,font_size=node_text_size,
                          font_family=text_font)

  if labels is None:
    labels = range(len(graph))

  edge_labels = dict(zip(graph, labels))
  nx.draw_networkx_edge_labels(G, graph_pos, edge_labels=edge_labels, 
                               label_pos=edge_text_pos)

  # show graph
  pl.savefig('cooccurringwords.pdf')

network(get_order_preserving_list(), graph_layout="spring", node_size=2500, node_text_size=10)
# bar_graph()
