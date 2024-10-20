import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.spatial import KDTree
from tqdm import tqdm

# Function to perform FNN Analysis
def fnn(timeseries, tlag, min_dimension, max_dimension):
    # Ensure the input is a NumPy array
    if isinstance(timeseries, (pd.Series, pd.DataFrame)):
        timeseries = timeseries.values.flatten()  # Convert to 1D NumPy array if it's a Series or DataFrame
    elif not isinstance(timeseries, np.ndarray):
        raise ValueError("Input timeseries must be a NumPy array or Pandas Series/DataFrame")
    
    # Preprocess the time series
    time_series = np.array(timeseries)

    percent = np.ones(max_dimension - min_dimension + 1)

    # Mean and radius of the attractor
    mean_x = np.mean(time_series)
    Ra = np.sqrt(np.mean((time_series - mean_x) ** 2))

    # Embedding dimensions to check
    de = np.arange(min_dimension, max_dimension + 1)
    
    for c in tqdm(de, desc="Processing FNN"):
        number_false = 0
        max_l = len(time_series) - c * tlag

        # Embed the time series
        curr_embedding = embed_time_series(time_series, c, tlag)

        # Build KDTree for nearest neighbor search
        tree = KDTree(curr_embedding)

        for c2 in range(max_l):
            # Search for the nearest neighbor
            dist, NN = tree.query(curr_embedding[c2], k=2)  # Nearest neighbor excluding itself
            nearest_d = dist[1]  # Exclude self, take the second closest
            NN = NN[1]

            if NN >= max_l:
                # If NN is beyond available data, assume not false
                test_stat1 = 0
                test_stat2 = 0
            else:
                if nearest_d == 0:
                    test_stat1 = 1
                else:
                    test_stat1 = np.abs(time_series[c2 + c * tlag] - time_series[NN + c * tlag]) / nearest_d
                
                test_stat2 = np.abs(time_series[c2 + c * tlag] - time_series[NN + c * tlag]) / Ra

            # Use Abarbanel's criteria: test_stat1 >= 15 or test_stat2 >= 2
            number_false += ((test_stat1 >= 15) | (test_stat2 >= 2))

        percent[c - min_dimension] = number_false / max_l

    return de, percent * 100


# Embedding the time series based on dimension and lag
def embed_time_series(data, embedding_dim, lag):
    data_length = len(data) - (embedding_dim - 1) * lag
    embedded = np.zeros((data_length, embedding_dim))
    for c in range(embedding_dim):
        embedded[:, c] = data[c * lag : c * lag + data_length]
    return embedded


# Function to plot FNN results
def plot_fnn(dimensions, fnn_percentages):
    plt.figure()
    plt.plot(dimensions, fnn_percentages, 'k-o')
    plt.xlim([dimensions[0], dimensions[-1]])
    plt.xlabel('# Embedding Dimensions')
    plt.ylabel('% False Nearest Neighbors')
    plt.title('False Nearest Neighbors Analysis')
    plt.show()