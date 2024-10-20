import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

# Helper function to ensure we handle both 1D and 2D timeseries data
def preprocess_timeseries(timeseries):
    """
    Ensures that the input timeseries is a NumPy array and 1D.
    If 2D, it extracts the first column.
    If input is a Pandas Series or DataFrame, it converts to a NumPy array.
    """
    # Ensure the input is a NumPy array
    if isinstance(timeseries, (pd.Series, pd.DataFrame)):
        timeseries = timeseries.values.flatten()  # Convert to 1D NumPy array if it's a Series or DataFrame
    elif not isinstance(timeseries, np.ndarray):
        raise ValueError("Input timeseries must be a NumPy array or Pandas Series/DataFrame")
    
    if timeseries.ndim == 2:
        return timeseries[:, 0]  # Extract the first column if it's 2D
    
    # zscore or unit normalize the data
    return timeseries  # Return the original if it's already 1D

# Auto-determine peak distance and amplitude filters
def auto_find_params(timeseries, samplerate):
    """
    Automatically determine the best DistFLT and AmpFLT values.
    
    Args:
        timeseries (array-like): Time-series data.
        samplerate (int): Sampling rate of the data.
    
    Returns:
        DistFLT (float): Estimated distance filter.
        AmpFLT (float): Estimated amplitude filter.
    """
    # Preprocess the timeseries to ensure it's 1D
    timeseries = preprocess_timeseries(timeseries)

    # Estimate the number of peaks by using a very loose threshold first
    loose_peaks, _ = find_peaks(timeseries, distance=samplerate//10)  # Very loose peak distance (10% of sampling rate)

    # Estimate DistFLT as a fraction of total signal length and number of peaks
    if len(loose_peaks) > 1:
        avg_peak_distance = np.mean(np.diff(loose_peaks))
    else:
        avg_peak_distance = len(timeseries) // 4  # Use quarter of the data if too few peaks are found
    
    DistFLT = avg_peak_distance / samplerate

    # Estimate AmpFLT as a fraction of the signal's amplitude range (30% by default)
    signal_range = np.max(timeseries) - np.min(timeseries)
    AmpFLT = 0.3 * signal_range / np.max(timeseries)

    return DistFLT, AmpFLT

# Function to calculate period statistics
def period(timeseries, samplerate, DistFLT="auto", AmpFLT="auto"):
    """
    Calculates the mean period and standard deviation of periods for rhythmic time-series data.
    
    Args:
        timeseries (array-like): Time-series data.
        samplerate (int): Sampling rate of the data.
        DistFLT (float or str): Minimum peak distance as a fraction of sample rate, or "auto" to estimate it.
        AmpFLT (float or str): Minimum peak height as a fraction of the maximum value, or "auto" to estimate it.
    
    Returns:
        meanPeriod (float): Mean period in seconds.
        sdPeriod (float): Standard deviation of the period in seconds.
        peaks (ndarray): Peak values.
        pkLocs (ndarray): Indices of peak locations.
    """
    # Preprocess the timeseries to ensure it's 1D
    timeseries = preprocess_timeseries(timeseries)

    # If DistFLT and AmpFLT are set to "auto", determine the best values
    if DistFLT == "auto" or AmpFLT == "auto":
        DistFLT, AmpFLT = auto_find_params(timeseries, samplerate)

    # Center Data
    x = timeseries - np.mean(timeseries)

    # Find peaks
    min_peak_distance = int(samplerate * DistFLT)
    min_peak_height = np.max(x) * AmpFLT
    pkLocs, _ = find_peaks(x, distance=min_peak_distance, height=min_peak_height)
    peaks = x[pkLocs]

    # Calculate mean period and SD of periods
    periods = np.diff(pkLocs) / samplerate
    meanPeriod = np.mean(periods)
    sdPeriod = np.std(periods)

    return meanPeriod, sdPeriod, peaks, pkLocs

# Function to calculate amplitude statistics
def amplitude(timeseries, samplerate, DistFLT="auto", AmpFLT="auto"):
    """
    Calculates the mean amplitude and standard deviation of amplitude for rhythmic time-series data.
    
    Args:
        timeseries (array-like): Time-series data.
        samplerate (int): Sampling rate of the data.
        DistFLT (float or str): Minimum peak distance as a fraction of sample rate, or "auto" to estimate it.
        AmpFLT (float or str): Minimum peak height as a fraction of the maximum value, or "auto" to estimate it.
    
    Returns:
        meanAmp (float): Mean amplitude.
        sdAmp (float): Standard deviation of amplitude.
        peaks (ndarray): Peak values.
        pkLocs (ndarray): Indices of peak locations.
        valleys (ndarray): Valley values.
        vLocs (ndarray): Indices of valley locations.
    """
    # Preprocess the timeseries to ensure it's 1D
    timeseries = preprocess_timeseries(timeseries)

    # If DistFLT and AmpFLT are set to "auto", determine the best values
    if DistFLT == "auto" or AmpFLT == "auto":
        DistFLT, AmpFLT = auto_find_params(timeseries, samplerate)

    # Center Data
    x = timeseries - np.mean(timeseries)

    # Find peaks
    min_peak_distance = int(samplerate * DistFLT)
    min_peak_height = np.max(x) * AmpFLT
    pkLocs, _ = find_peaks(x, distance=min_peak_distance, height=min_peak_height)
    peaks = x[pkLocs]

    # Find valleys
    vLocs, _ = find_peaks(-x, distance=min_peak_distance, height=min_peak_height)
    valleys = -x[vLocs]

    # Determine appropriate length for amplitude calculations
    pvLength = min(len(peaks), len(valleys))

    # Calculate mean and SD of amplitude
    meanAmp = np.mean(peaks[:pvLength] - valleys[:pvLength])
    sdAmp = np.std(peaks[:pvLength] - valleys[:pvLength])

    return meanAmp, sdAmp, peaks, pkLocs, valleys, vLocs

# Function to plot the time series with marked peaks
def plot_period(timeseries, samplerate, peaks, pkLocs):
    timeseries = preprocess_timeseries(timeseries)
    time = np.arange(len(timeseries)) / samplerate

    plt.figure()
    plt.plot(time, timeseries, label='Time Series')
    plt.plot(pkLocs / samplerate, timeseries[pkLocs], 'ro', label='Peaks')  # Use timeseries[pkLocs] for correct peak y-values
    plt.xlabel('Time (seconds)')
    plt.ylabel('Amplitude')
    plt.title('Time Series with Peaks (Period Analysis)')
    plt.legend()
    plt.grid(True)
    plt.show()

# Function to plot the time series with marked peaks and valleys
def plot_amplitude(timeseries, samplerate, peaks, pkLocs, valleys, vLocs):
    timeseries = preprocess_timeseries(timeseries)
    time = np.arange(len(timeseries)) / samplerate

    plt.figure()
    plt.plot(time, timeseries, label='Time Series')
    plt.plot(pkLocs / samplerate, timeseries[pkLocs], 'ro', label='Peaks')    # Use timeseries[pkLocs] for correct peak y-values
    plt.plot(vLocs / samplerate, timeseries[vLocs], 'bo', label='Valleys')    # Use timeseries[vLocs] for correct valley y-values
    plt.xlabel('Time (seconds)')
    plt.ylabel('Amplitude')
    plt.title('Time Series with Peaks and Valleys (Amplitude Analysis)')
    plt.legend()
    plt.grid(True)
    plt.show()
