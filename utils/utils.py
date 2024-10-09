import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt
import pyopencl as cl

def get_best_device():
    platforms = cl.get_platforms()
    devices = []
    for platform in platforms:
        devices.extend(platform.get_devices())

    if not devices:
        raise RuntimeError("No OpenCL devices found")

    # Prioritize GPU over CPU
    for device in devices:
        if device.type == cl.device_type.GPU:
            return device
    for device in devices:
        if device.type == cl.device_type.CPU:
            return device

    # If no CPU or GPU found, just return the first device
    return devices[0]


def butter_lowpass(cutoff, fs, order=4):
    """
    Design a Butterworth lowpass filter.

    Parameters:
    cutoff (float): The cutoff frequency of the filter.
    fs (float): The sampling rate of the signal.
    order (int): The order of the filter.

    Returns:
    tuple: Filter coefficients (b, a).
    """
    nyq = 0.5 * fs  # Nyquist frequency
    normal_cutoff = cutoff / nyq  # Normalized cutoff frequency
    b, a = butter(order, normal_cutoff, btype='low', analog=False)  # Butterworth filter design
    return b, a

def apply_filter(data, cutoff=10, fs=30, order=4):
    """
    Apply a lowpass Butterworth filter to the data.

    Parameters:
    data (array-like): The input data to be filtered.
    cutoff (float): The cutoff frequency of the filter.
    fs (float): The sampling rate of the signal.
    order (int): The order of the filter.

    Returns:
    array-like: The filtered data.
    """
    b, a = butter_lowpass(cutoff, fs, order)  # Get filter coefficients
    y = filtfilt(b, a, data)  # Apply the filter to the data
    return y

def filter_data(df):
    """
    Apply a lowpass filter to each column in a DataFrame.

    Parameters:
    df (pd.DataFrame): The input DataFrame with data to be filtered.

    Returns:
    pd.DataFrame: The filtered DataFrame.
    """
    for column in df.columns:
        df[column] = apply_filter(df[column])  # Apply filter to each column
    return df

def interpolate_missing_data(data, method='linear'):
    """
    Interpolate missing data in a DataFrame or Series.

    Parameters:
    data (pd.DataFrame or pd.Series): The input data with missing values.
    method (str): The interpolation method. Default is 'linear'.

    Returns:
    pd.DataFrame or pd.Series: The data with missing values interpolated.
    """
    return data.interpolate(method=method)  # Interpolate missing data
