import numpy as np
from scipy.signal import hilbert, find_peaks
from scipy.stats import circmean, circstd
import matplotlib.pyplot as plt

def irp(x1, x2):
    """
    Calculates instantaneous relative phase between two time-series using Hilbert transform.
    
    Args:
        x1 (array-like): First time-series.
        x2 (array-like): Second time-series.
        
    Returns:
        meanRP (float): Circular mean of relative phase in radians.
        sdRP (float): Circular standard deviation of relative phase in radians.
        rvRP (float): Resultant vector length (measure of concentration).
        radians (array): Time-series of relative phase in radians.
    """
    # Center data by subtracting the mean
    x1 = x1 - np.mean(x1)
    x2 = x2 - np.mean(x2)
    
    # Hilbert transform to calculate relative phase
    h1 = hilbert(x1)
    h2 = hilbert(x2)
    num = np.imag(h2) * x1 - np.imag(h1) * x2
    denom = x2 * x1 + np.imag(h2) * np.imag(h1)
    radians = np.arctan2(num, denom)
    
    # Circular statistics
    meanRP = circmean(radians)
    rvRP = np.abs(np.mean(np.exp(1j * radians)))
    sdRP = circstd(radians)
    
    return meanRP, sdRP, rvRP, radians


def drp(x1, x2, samplerate, DistFLT=0.5, AmpFLT=0.3):
    """
    Calculate discrete instantaneous relative phase angle between two time series.
    
    Args:
        x1 (array-like): First time-series (referent).
        x2 (array-like): Second time-series.
        samplerate (int): Sampling rate.
        DistFLT (float): Minimum peak distance in seconds.
        AmpFLT (float): Minimum peak amplitude (fraction of max amplitude).
        
    Returns:
        meanRP (float): Circular mean of relative phase in radians.
        sdRP (float): Circular standard deviation of relative phase in radians.
        rvRP (float): Resultant vector length (measure of concentration).
        radians (array): Discrete relative phase at peak locations of x1.
    """
    # Center data
    x1 = x1 - np.mean(x1)
    x2 = x2 - np.mean(x2)
    
    # Find peaks in x1
    peak_dist = int(samplerate * DistFLT)
    peaks, _ = find_peaks(x1, distance=peak_dist, height=max(x1) * AmpFLT)
    
    # Hilbert transform for phase angles in x2
    hbt = hilbert(x2)
    radians = np.arctan2(np.imag(hbt), x2)
    
    # Use relative phase at peak locations
    radians = radians[peaks]
    
    # Circular statistics
    meanRP = circmean(radians)
    rvRP = np.abs(np.mean(np.exp(1j * radians)))
    sdRP = circstd(radians)
    
    return meanRP, sdRP, rvRP, radians, peaks


import numpy as np
import matplotlib.pyplot as plt

def plot_irp(radians, samplerate):
    """
    Plot relative phase in radians over time, ensuring the phase is centered around 0 (-2π to +2π).
    
    Args:
        radians (array): Relative phase in radians.
        samplerate (int): Sampling rate of the time series.
        centre (int): Set to 0 to center phase around 0 (-2π to 2π).
    """
    # Generate time points
    time = np.arange(0, len(radians) / samplerate, 1 / samplerate)
        
    plt.figure()
    plt.plot(time, radians, label='Relative Phase')
    plt.xlabel('Time (s)')
    plt.ylabel('Phase (radians)')
    plt.title('Instantaneous Relative Phase')
    plt.grid(True)
    plt.legend()
    plt.show()


def plot_drp(radians, peaks, samplerate):
    """
    Plot discrete relative phase at peak locations.
    
    Args:
        radians (array): Relative phase in radians at peaks.
        peaks (array): Indices of the peaks in the time series.
        samplerate (int): Sampling rate.
    """
    # Convert peak indices to time values
    time_peaks = peaks / samplerate
    
    plt.figure()
    plt.plot(time_peaks, radians, 'o', label='Discrete Relative Phase')
    plt.xlabel('Time (s)')
    plt.ylabel('Phase (radians)')
    plt.title('Discrete Relative Phase at Peaks')
    plt.grid(True)
    plt.legend()
    plt.show()


def plot_rp_distribution(radians, bins=30, centre=0):
    """
    Plot distribution of relative phase angles.
    
    Args:
        radians (array): Relative phase in radians.
    """

    # Centre around 0
    # Ensure the phase is centered between -π and π
    if centre == 0: 
        radians = np.mod(radians + np.pi, 2 * np.pi) - np.pi

    plt.figure()
    plt.hist(radians, bins=bins, color='skyblue', edgecolor='black')
    plt.xlabel('Phase (radians)')
    plt.ylabel('Count')
    plt.title('Relative Phase Distribution')
    if centre == 0:
        plt.xticks(np.arange(-np.pi, np.pi + 1, np.pi))
    else:
        plt.xticks(np.arange(0, 2*np.pi + 1, np.pi))
    plt.grid(True)
    plt.show()


def return_plot(x1, x2, samplerate):
    """
    Generate return plot of relative phase for two time-series.
    
    Args:
        x1 (array-like): First time-series.
        x2 (array-like): Second time-series.
        samplerate (int): Sampling rate.
    """
    # Get discrete relative phase for x1 and x2
    _, _, _, radians1, _ = drp(x1, x2, samplerate)
    _, _, _, radians2, _ = drp(x2, x1, samplerate)
    
    # Plot return plot
    plt.figure()
    plt.scatter(radians1[:-1], radians1[1:], color='red', label='x1:x2')
    plt.scatter(radians2[:-1], radians2[1:], color='blue', label='x2:x1')
    plt.xlabel('Relative Phase (t)')
    plt.ylabel('Relative Phase (t+1)')
    plt.xticks(np.arange(-np.pi, np.pi + 1, np.pi))
    plt.yticks(np.arange(-np.pi, np.pi + 1, np.pi))
    plt.title('Relative Phase Return Plot')
    plt.grid(True)
    plt.legend()
    plt.show()