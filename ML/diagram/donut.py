import networkx as nx
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import pandas as pd

from ML.py_files import toolbox

G = nx.Graph()

# Get data from ".prob" file
sequence_nb = 1000
filepath = 'Datasets/HDV/prob/SEQUENCE_'+str(sequence_nb)+'.prob'
data = toolbox.csv_reader(filepath,delimiter='\t')

# Convert data from string to float
prob_data = np.array(data).astype(float)

# Extract data and create nodes and edges
edge_stack=[]
color_stack=[]
max_prob = 0
min_prob = 1
for i in range(prob_data.shape[0]):
    for j in range(prob_data.shape[1]):
        tmp_prob = prob_data[i,j]
        if tmp_prob > 0:
            if tmp_prob > max_prob: max_prob = tmp_prob
            if tmp_prob < min_prob: min_prob = tmp_prob
        G.add_edge(i,j)
        edge_stack.append(tmp_prob)
        pass
    pass

# Set background color
plt.style.use('dark_background')
fig, ax = plt.subplots()

# Choose colormap ref: https://matplotlib.org/stable/tutorials/colors/colormaps.html
cmap = plt.cm.coolwarm

# Get the colormap colors
my_cmap = cmap(np.arange(cmap.N))

# Set alpha (transparency)
my_cmap[:,-1] = np.linspace(0, 1, cmap.N)

# Create new colormap
my_cmap = mpl.colors.ListedColormap(my_cmap)

# Assign the new color map
norm = mpl.colors.Normalize(vmin=min_prob, vmax=max_prob)
m = mpl.cm.ScalarMappable(norm=norm, cmap=my_cmap)
for e in edge_stack:
    color_stack.append(m.to_rgba(e))

# Define labels
filepath = 'Datasets/HDV/fasta/single/SEQUENCE_'+str(sequence_nb)+'.fasta'
data = toolbox.csv_reader(filepath,delimiter='\n')
labeldict = {}
for i in range(len(G.nodes)):
    tmp = list(data[1][0])
    labeldict[i] = tmp[i]

# Define the layout
pos = nx.circular_layout(G)
options = {
    "node_size"  : 100,
    "node_color" : 'blue',

    "font_size"   : 8,
    "with_labels" : True,
    "labels"      : labeldict,
    "font_color"  : "w",

    "edge_color" : color_stack,
    "width"      : 1,
}
nx.draw_networkx(G, pos, **options)

# Display the diagram
plt.gca().margins(0)
plt.tight_layout()
plt.axis("off")
plt.show()