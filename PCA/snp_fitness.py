from copy import deepcopy
import pandas as pd

from ML.py_files.Lib14.data_properties import HDV_LIG14
import plotly.express as px

from sklearn.decomposition import PCA
import numpy as np


if __name__ == '__main__':
    # Extract the data
    data = np.array(deepcopy(HDV_LIG14.snp_nucleotides))
    y = np.array(deepcopy(HDV_LIG14.hdv_fitness))

    # Transform strings to list of chars
    data = [list(x) for x in data]

    # Define a dictionary to map nucleotides to binary vectors
    nucleotide_dict = {'A': [1, 0, 0, 0],
                       'C': [0, 1, 0, 0],
                       'G': [0, 0, 1, 0],
                       'T': [0, 0, 0, 1],
                       'U': [0, 0, 0, 1]}

    # Convert the data to a one-hot encoded matrix
    X = np.zeros((len(data), 14 * 4))
    for i, seq in enumerate(data):
        for j, nucleotide in enumerate(seq):
            X[i, j * 4:(j + 1) * 4] = nucleotide_dict[nucleotide]

    # Check if there are any columns with zero variance in X
    zero_var_cols = np.where(np.var(X, axis=0) == 0)[0]
    if zero_var_cols.size > 0:
        print("Removing columns with zero variance:")
        print(zero_var_cols)
        X = np.delete(X, zero_var_cols, axis=1)
    else:
        print("No columns with zero variance found.")

    # Compute the mean and standard deviation of each column
    mean = np.mean(X, axis=0)
    std = np.std(X, axis=0)

    # Center and scale the data
    X = (X - mean) / std

    # Apply PCA with 4 components
    pca = PCA(n_components=4)  # max = 22
    X_pca = pca.fit_transform(X)

    # Create a dataframe from X_pca and fitness
    df = pd.DataFrame(X_pca, columns=['PCA1', 'PCA2', 'PCA3', 'PCA4'])
    df['fitness'] = pd.to_numeric(y)

    # Create the 3D scatter plot
    fig = px.scatter_3d(df, x='PCA1', y='PCA2', z='PCA3', size='fitness', color='fitness', hover_data=['fitness'])

    # Show the plot
    fig.show()

    # Save the plot
    fig.write_html('PCA_plot.html')
