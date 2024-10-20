import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm

def ami(timeseries, min_lag, max_lag):
    # Ensure the input is a NumPy array
    if isinstance(timeseries, (pd.Series, pd.DataFrame)):
        timeseries = timeseries.values.flatten()  # Convert to 1D NumPy array if it's a Series or DataFrame
    elif not isinstance(timeseries, np.ndarray):
        raise ValueError("Input timeseries must be a NumPy array or Pandas Series/DataFrame")

    x = timeseries
    length = len(x)

    # Create Lag Vector
    if max_lag <= (length // 2 - 1):
        if min_lag < max_lag:
            lag = np.arange(min_lag, max_lag + 1)
        else:
            print('error - maximum lag not greater than minimum lag')
            print('default lag vector used (0 - 50)')
            lag = np.arange(0, 51)
    else:
        print('error - maximum lag exceeds recommendation')
        print('maximum lag set to n/2-1')
        lag = np.arange(0, length // 2)

    # Normalize the data
    x = (x - np.min(x)) / (np.max(x) - np.min(x))

    ami_values = np.zeros(len(lag))

    # Compute Average Mutual Information (AMI)
    for i in tqdm(range(len(lag)), desc='Processing AMI'):
        k = int(np.floor(1 + np.log2(length - lag[i]) + 0.5))

        if np.var(x, ddof=1) == 0:
            ami_values[i] = 0
        else:
            ami_sum = 0
            for k1 in range(1, k + 1):
                for k2 in range(1, k + 1):
                    cond1 = (k1 - 1) / k < x[:length - lag[i]]
                    cond2 = x[:length - lag[i]] <= k1 / k
                    cond3 = (k2 - 1) / k < x[lag[i]:]
                    cond4 = x[lag[i]:] <= k2 / k

                    ppp = np.sum(cond1 & cond2 & cond3 & cond4)
                    px1 = np.sum(cond1 & cond2)
                    px2 = np.sum(cond3 & cond4)

                    if ppp > 0:
                        ppp = ppp / (length - lag[i])
                        px1 = px1 / (length - lag[i])
                        px2 = px2 / (length - lag[i])
                        ami_sum += ppp * np.log2(ppp / (px1 * px2))

            ami_values[i] = ami_sum

    # Create the AMI result array
    ami_result = np.column_stack((lag, ami_values))
    
    return ami_result


def cross_ami(timeseries1, timeseries2, min_lag, max_lag):
    # Ensure the inputs are NumPy arrays
    if isinstance(timeseries1, (pd.Series, pd.DataFrame)):
        timeseries1 = timeseries1.values.flatten()
    if isinstance(timeseries2, (pd.Series, pd.DataFrame)):
        timeseries2 = timeseries2.values.flatten()

    elif not isinstance(timeseries1, np.ndarray) or not isinstance(timeseries2, np.ndarray):
        raise ValueError("Both input timeseries must be NumPy arrays or Pandas Series/DataFrame")

    x = timeseries1
    y = timeseries2
    length = min(len(x), len(y))

    # Create Lag Vector
    if max_lag <= (length // 2 - 1):
        if min_lag < max_lag:
            lag = np.arange(min_lag, max_lag + 1)
        else:
            print('error - maximum lag not greater than minimum lag')
            print('default lag vector used (0 - 50)')
            lag = np.arange(0, 51)
    else:
        print('error - maximum lag exceeds recommendation')
        print('maximum lag set to n/2-1')
        lag = np.arange(0, length // 2)

    # Normalize both data series
    x = (x - np.min(x)) / (np.max(x) - np.min(x))
    y = (y - np.min(y)) / (np.max(y) - np.min(y))

    ami_values = np.zeros(len(lag))

    # Compute Cross Average Mutual Information (Cross-AMI)
    for i in tqdm(range(len(lag)), desc='Processing Cross-AMI'):
        k = int(np.floor(1 + np.log2(length - lag[i]) + 0.5))

        if np.var(x, ddof=1) == 0 or np.var(y, ddof=1) == 0:
            ami_values[i] = 0
        else:
            ami_sum = 0
            for k1 in range(1, k + 1):
                for k2 in range(1, k + 1):
                    cond1 = (k1 - 1) / k < x[:length - lag[i]]
                    cond2 = x[:length - lag[i]] <= k1 / k
                    cond3 = (k2 - 1) / k < y[lag[i]:]
                    cond4 = y[lag[i]:] <= k2 / k

                    ppp = np.sum(cond1 & cond2 & cond3 & cond4)
                    px1 = np.sum(cond1 & cond2)
                    py2 = np.sum(cond3 & cond4)

                    if ppp > 0:
                        ppp = ppp / (length - lag[i])
                        px1 = px1 / (length - lag[i])
                        py2 = py2 / (length - lag[i])
                        ami_sum += ppp * np.log2(ppp / (px1 * py2))

            ami_values[i] = ami_sum

    # Create the Cross-AMI result array
    cross_ami_result = np.column_stack((lag, ami_values))
    
    return cross_ami_result

def plot_ami(ami_result):
    # Plot AMI Function
    plt.figure()
    plt.plot(ami_result[:, 0], ami_result[:, 1])
    plt.xlabel('TLag')
    plt.ylabel('AMI')
    plt.title('Average Mutual Information')
    plt.show()

def plot_cross_ami(cross_ami_result):
    # Plot Cross-AMI Function
    plt.figure()
    plt.plot(cross_ami_result[:, 0], cross_ami_result[:, 1])
    plt.xlabel('TLag')
    plt.ylabel('Cross-AMI')
    plt.title('Cross Average Mutual Information')
    plt.show()