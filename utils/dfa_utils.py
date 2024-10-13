import numpy as np
import nolds

# Function to perform DFA on a single column of data
def perform_nolds_dfa(data):
    try:
        # Perform DFA analysis
        alpha = nolds.dfa(data)
        return alpha
    except Exception as e:
        print(f"Failed to compute DFA: {e}")
        return float('nan')  # Return NaN if DFA fails

# Custom DFA function
def dfa(data, min_window_size=8):
    N = len(data)
    data = np.cumsum(data - np.mean(data))    #integrate data
    flucts = []
    scales = np.logspace(np.log10(min_window_size), np.log10(N//4), num=16, dtype=int)
    scales = np.unique(scales)  # Remove duplicate scales
    for scale in scales:
        rms_vals = []
        for i in range(0, N, scale):
            if i + scale < N:
                segment = data[i:i+scale]
                trend = np.polyfit(np.arange(scale), segment, 1)
                fit = np.polyval(trend, np.arange(scale))
                rms = np.sqrt(np.mean((segment - fit) ** 2))
                rms_vals.append(rms)
        flucts.append(np.mean(rms_vals))
    flucts = np.array(flucts)
    scales = np.array(scales)
    coeffs = np.polyfit(np.log(scales), np.log(flucts), 1)
    alpha = coeffs[0]
    fit_line = np.polyval(coeffs, np.log(scales))
    return alpha, scales, flucts, fit_line

def perform_dfa_for_plotting(data, min_window_size=8):
    column = data.columns[0]
    data[column] = (data[column] - data[column].mean()) / data[column].std()
    alpha, scales, flucts, fit_line = dfa(data[column], min_window_size)
    return {column: {'alpha': alpha, 'scales': scales, 'flucts': flucts, 'fit_line': fit_line}}

def perform_dfa(data, min_window_size=8):
    column = data.columns[0]
    data[column] = (data[column] - data[column].mean()) / data[column].std()
    alpha, scales, flucts, fit_line = dfa(data[column], min_window_size)
    return {column: alpha}  # Only store alpha for simplicity