import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import welch, coherence, detrend, windows

# Helper function to ensure we handle both 1D and 2D timeseries data
def preprocess_timeseries(timeseries):
    if isinstance(timeseries, (pd.Series, pd.DataFrame)):
        timeseries = timeseries.values.flatten()  # Convert to 1D NumPy array if it's a Series or DataFrame
    elif not isinstance(timeseries, np.ndarray):
        raise ValueError("Input timeseries must be a NumPy array or Pandas Series/DataFrame")
    if timeseries.ndim == 2:
        return timeseries[:, 0]  # Extract the first column if it's 2D
    return timeseries  # Return the original if it's already 1D

# Spectral analysis function
def spectral_analysis(timeseries, samplerate, window_size, window_overlap):
    """
    Performs spectral analysis (power spectral density) on a time series.
    Args:
        timeseries (array-like): Time-series data.
        samplerate (int): Sampling rate of the data.
        window_size (int): Size of the FFT window.
        window_overlap (float): Fraction of window overlap (e.g., 0.5).
    Returns:
        power (ndarray): Power spectral density values.
        freq (ndarray): Frequency values.
    """
    timeseries = preprocess_timeseries(timeseries)
    timeseries = detrend(timeseries)  # Detrending the data
    window = windows.hann(window_size)
    n_overlap = int(window_size * window_overlap)
    freq, power = welch(timeseries, fs=samplerate, window=window, noverlap=n_overlap, nfft=window_size)
    return power, freq

# Cross-spectral coherence function
def cross_spectral_coherence(x, y, samplerate, window_size, window_overlap):
    """
    Calculates the average cross-spectral coherence between two time series.
    Args:
        x (array-like): First time-series data.
        y (array-like): Second time-series data.
        samplerate (int): Sampling rate of the data.
        window_size (int): Size of the FFT window.
        window_overlap (float): Fraction of window overlap (e.g., 0.5).
    Returns:
        cohere_stats (ndarray): Average coherence over all frequencies.
        FP1 (tuple): Power and frequency for the first time series.
        FP2 (tuple): Power and frequency for the second time series.
        cohereFP (tuple): Coherence and frequency values.
    """
    # Preprocess the timeseries to ensure they are 1D and NumPy arrays
    x = preprocess_timeseries(x)
    y = preprocess_timeseries(y)
    
    # Linear detrending and normalization (z-score)
    x = detrend(x)
    y = detrend(y)
    x = (x - np.mean(x)) / np.std(x)
    y = (y - np.mean(y)) / np.std(y)

    # Create Hann window and calculate overlap in samples
    window = windows.hann(window_size)
    n_overlap = int(window_size * window_overlap)
    
    # Spectral analysis for both time series
    freq1, power1= welch(x, fs=samplerate, window=window, noverlap=n_overlap, nfft=window_size)
    freq2, power2, = welch(y, fs=samplerate, window=window, noverlap=n_overlap, nfft=window_size)
    FP1 = (power1, freq1)
    FP2 = (power2, freq2)
    
    # Cross-spectral coherence analysis
    f3, Cxy = coherence(x, y, fs=samplerate, window=window, noverlap=n_overlap, nfft=window_size)
    cohereFP = (Cxy, f3)

    # Average coherence across all frequencies
    average_coherence = np.mean(Cxy)
    cohere_stats = [average_coherence]

    # Coherence at peak frequency of ecah time series
    peak_freq1 = freq1[np.argmax(power1)]
    peak_freq2 = freq2[np.argmax(power2)]
    peak_cohere1 = Cxy[np.argmin(np.abs(f3 - peak_freq1))]
    peak_cohere2 = Cxy[np.argmin(np.abs(f3 - peak_freq2))]
    cohere_stats.extend([peak_cohere1, peak_cohere2])

    #average coherence at peak frequency
    avg_peak_cohere = np.mean([peak_cohere1, peak_cohere2])
    cohere_stats.append(avg_peak_cohere)

    return cohere_stats, FP1, FP2, cohereFP

# Plotting function for power spectral density
def plot_spectral_analysis(FP, maxFreq=10):
    power, freq = FP
    valid_idx = freq <= maxFreq  # Filter frequencies below maxFreq
    plt.figure()
    plt.plot(freq[valid_idx], power[valid_idx])  # Plot frequency on x-axis, power on y-axis
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Power/Frequency (dB/Hz)')
    plt.title("Power Spectral Density")
    plt.grid(True)
    plt.show()

# Plotting function for coherence analysis
def plot_coherence(cohereFP, maxFreq=10):
    Cxy, freq = cohereFP
    valid_idx = freq <= maxFreq  # Filter frequencies below maxFreq
    plt.figure()
    plt.plot(freq[valid_idx], Cxy[valid_idx])  # Plot frequency on x-axis, coherence on y-axis
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Coherence')
    plt.title("Cross-Spectral Coherence")
    plt.grid(True)
    plt.show()

