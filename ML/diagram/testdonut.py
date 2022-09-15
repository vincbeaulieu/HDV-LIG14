
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

from ML.py_files import toolbox

G = nx.Graph()

sequence_nb=1000
filepath = 'Datasets/HDV/fasta/single/SEQUENCE_'+str(sequence_nb)+'.fasta'
data = toolbox.csv_reader(filepath,delimiter='\n')
labeldict = {}
tmp = list(data[1][0])
print(tmp)
for i in range(len(G.nodes)):
    #labeldict[i] = tmp[i]
    G.add_node(tmp[i],color='red',style='filled',fillcolor='blue',shape='square')


pos = nx.circular_layout(G)
options = {
    "node_size"  : 100,
    #"node_color" : 'blue',

    "font_size"   : 8,
    "with_labels" : True,
    #"labels"      : labeldict,
    "font_color"  : "w",

    "edge_color" : "w",
    "width"      : 1,
}
nx.draw_networkx(G, pos, **options)

# Display the diagram
plt.gca().margins(0)
plt.tight_layout()
plt.axis("off")
plt.show()

