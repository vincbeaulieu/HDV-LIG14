import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from ML.py_files import toolbox

G = nx.Graph()

# Get data from ".prob" file
filepath = 'Datasets/HDV/prob/SEQUENCE_0.prob'
data = toolbox.csv_reader(filepath,delimiter='\t')

# Convert data from string to float
prob_data = np.array(data).astype(float)
#np.set_printoptions(suppress=True)
print(prob_data.shape[1])
#print(prob_data[3,5])
#print(type(prob_data[3,5]))

for i in range(prob_data.shape[0]):

    for j in range(prob_data.shape[1]):
        pass
    
    pass

# if not 0, then add edge
G.add_edge(1, 2)
G.add_edge(1, 3)
G.add_edge(1, 5)
G.add_edge(2, 3)
G.add_edge(3, 4)
G.add_edge(4, 5)

# explicitly set positions
pos = nx.circular_layout(G)

options = {
    "font_size": 36,
    "node_size": 3000,
    "node_color": range(len(G.nodes)),
    "cmap": plt.cm.Blues,

    "edge_color":range(len(G.edges)),
    "edge_cmap": plt.cm.Blues,
    "linewidths": 5,
    "width": 5,
}
nx.draw_networkx(G, pos, **options)

# Set margins for the axes so that nodes aren't clipped
plt.gca().margins(0.20)
plt.axis("off")
plt.show()