import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Function to compute autocorrelation
def auto_correlation(timeseries, max_lag):
    """
    Computes the autocorrelation of a time series for lags from 0 to max_lag.
    
    Args:
        timeseries (array-like): The time series data.
        max_lag (int): The maximum lag to compute autocorrelation for.
    
    Returns:
        lags (ndarray): Array of lags from 0 to max_lag.
        autocorr (ndarray): Autocorrelation values for each lag.
    """
    # Ensure the input is a NumPy array
    if isinstance(timeseries, (pd.Series, pd.DataFrame)):
        timeseries = timeseries.values.flatten()  # Convert to 1D NumPy array if it's a Series or DataFrame
    elif not isinstance(timeseries, np.ndarray):
        raise ValueError("Input timeseries must be a NumPy array or Pandas Series/DataFrame")
    
    timeseries = np.array(timeseries)
    mean = np.mean(timeseries)
    var = np.var(timeseries)
    lags = np.arange(0, max_lag + 1)
    autocorr = np.correlate(timeseries - mean, timeseries - mean, mode='full')[len(timeseries)-1:] / (len(timeseries) * var)
    
    return lags, autocorr[:max_lag + 1]

# Function to compute cross-correlation
def cross_correlation(timeseries1, timeseries2, max_lag):
    """
    Computes the cross-correlation between two time series for lags from -max_lag to +max_lag.
    
    Args:
        timeseries1 (array-like): The first time series data.
        timeseries2 (array-like): The second time series data.
        max_lag (int): The maximum lag to compute cross-correlation for.
    
    Returns:
        lags (ndarray): Array of lags from -max_lag to max_lag.
        crosscorr (ndarray): Cross-correlation values for each lag.
    """
    # Ensure the inputs are NumPy arrays
    if isinstance(timeseries1, (pd.Series, pd.DataFrame)):
        timeseries1 = timeseries1.values.flatten()
    if isinstance(timeseries2, (pd.Series, pd.DataFrame)):
        timeseries2 = timeseries2.values.flatten()

    elif not isinstance(timeseries1, np.ndarray) or not isinstance(timeseries2, np.ndarray):
        raise ValueError("Both input timeseries must be NumPy arrays or Pandas Series/DataFrame")
    
    timeseries1 = np.array(timeseries1)
    timeseries2 = np.array(timeseries2)
    mean1 = np.mean(timeseries1)
    mean2 = np.mean(timeseries2)
    var1 = np.var(timeseries1)
    var2 = np.var(timeseries2)
    
    crosscorr_full = np.correlate(timeseries1 - mean1, timeseries2 - mean2, mode='full') / (np.sqrt(var1 * var2) * len(timeseries1))
    lags = np.arange(-max_lag, max_lag + 1)
    mid = len(crosscorr_full) // 2
    
    return lags, crosscorr_full[mid - max_lag: mid + max_lag + 1]

# Function to plot autocorrelation
def plot_autocorrelation(lags, autocorr):
    """
    Plots the autocorrelation function.
    
    Args:
        lags (ndarray): The lags.
        autocorr (ndarray): Autocorrelation values.
    """
    plt.figure()
    plt.stem(lags, autocorr)
    plt.xlabel('Lag')
    plt.ylabel('Autocorrelation')
    plt.title('Autocorrelation Function')
    plt.grid(True)
    plt.show()

# Function to plot cross-correlation
def plot_crosscorrelation(lags, crosscorr):
    """
    Plots the cross-correlation function.
    
    Args:
        lags (ndarray): The lags.
        crosscorr (ndarray): Cross-correlation values.
    """
    plt.figure()
    plt.stem(lags, crosscorr)
    plt.xlabel('Lag')
    plt.ylabel('Cross-Correlation')
    plt.title('Cross-Correlation Function')
    plt.grid(True)
    plt.show()