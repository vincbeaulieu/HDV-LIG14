from copy import deepcopy
import matplotlib.pyplot as plt
import pandas as pd

from ML.py_files.Lib14.data_properties import HDV_LIG14
from mpl_toolkits.mplot3d import Axes3D
import plotly.express as px

from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import numpy as np

# random seed with cluster: 9, 10, 16, 24, 30, 64
# random seed with patterns: 23, 31, 32, 43, 54, 62, 66
#np.random.seed(66)

if __name__ == '__main__':
    # Extract the data
    snp = deepcopy(HDV_LIG14.snp_nucleotides)
    fitness = deepcopy(HDV_LIG14.hdv_fitness)

    letter_mapping = {'A': 0, 'T': 1, 'U': 1, 'C': 2, 'G': 3}

    # Transform strings to list of chars
    for i, j in enumerate(snp):
        # numeral = [letter_mapping[k] for k in j]
        # digital = ''.join(str(n) for n in numeral)
        # decimal = int(digital, 4)
        snp[i] = [*snp[i]]

    # Select the data
    data = np.array(snp)

    y = np.array(fitness)

    # Define a dictionary to map nucleotides to binary vectors
    nucleotide_dict = {'A': [1, 0, 0, 0], 'C': [0, 1, 0, 0], 'G': [0, 0, 1, 0], 'T': [0, 0, 0, 1],  'U': [0, 0, 0, 1]}
    print(len(data))
    # Convert the data to a one-hot encoded matrix
    X = np.zeros((len(data), 14 * 4))
    for i, seq in enumerate(data):
        for j, nucleotide in enumerate(seq):
            X[i, j * 4:(j + 1) * 4] = nucleotide_dict[nucleotide]

    # check if there are any columns with zero variance in X
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
    print(mean)
    print(std)

    # check if there are any NaN values in X
    print(np.isnan(X).any())

    # check if there are any columns with zero variance in X
    print(np.var(X, axis=0) == 0)

    # Center and scale the data
    X = (X - mean) / std

    # Apply PCA with 4 components
    pca = PCA(n_components=4)  # 22
    X_pca = pca.fit_transform(X)

    # Give 19 well defined stripes, but why ?
    import matplotlib.pyplot as plt

    # create a dataframe from X_pca and fitness
    df = pd.DataFrame(X_pca, columns=['PCA1', 'PCA2', 'PCA3', 'PCA4'])
    df['fitness'] = pd.to_numeric(y)

    # create the 3D scatter plot
    fig = px.scatter_3d(df, x='PCA1', y='PCA2', z='PCA3', size='fitness', color='fitness', hover_data=['fitness'])
    # show the plot
    fig.show()

    fig.write_html('PCA_plot.html')



    # Standardize the data
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Compute Covariance
    cov_mat = np.cov(X_scaled, rowvar=False)

    # Compute the eigenvectors and eigenvalues
    eig_vals, eig_vecs = np.linalg.eig(cov_mat)

    # Select the principal components
    explained_variance_ratio = eig_vals / np.sum(eig_vals)
    cumulative_variance_ratio = np.cumsum(explained_variance_ratio)

    # Select the top k eigenvectors that explain the most variance
    k = np.argmax(cumulative_variance_ratio >= 0.8) + 1
    top_k_eig_vecs = eig_vecs[:, :k]

    # Project the data onto the principal components
    X_pca = X_scaled.dot(top_k_eig_vecs)

    # Visualize the results
    #plt.scatter(X_pca[:, 0], X_pca[:, 1], c=y)
    #plt.xlabel('PC1')
    #plt.ylabel('PC2')
    #plt.show()
