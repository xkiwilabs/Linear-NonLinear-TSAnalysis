from utils import output_io_utils, cleaning_utils
from utils import rqa_utils_cpp
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np


def perform_rqa(data, params, filename):
    """
    Perform Auto Recurrence Quantification Analysis (RQA).

    Parameters:
        data (pd.DataFrame): Time series data with one or more columns.
        params (dict): Dictionary of RQA parameters.

    Returns:
        dict: RQA results for each column in the data.
        dict: Recurrence plot results.
    """
    # Ensure data is a DataFrame with at least one column
    if not isinstance(data, pd.DataFrame) or data.shape[1] < 1:
        raise ValueError("Expected a DataFrame with at least one column for RQA.")

    # Normalize data
    dataX = cleaning_utils.normalize_data(data, params['norm'])

    # Compute distance matrix for RQA
    ds = rqa_utils_cpp.rqa_dist(dataX, dataX, dim=params['eDim'], lag=params['tLag'])

    # Perform RQA calculations
    td, rs, mats, err_code = rqa_utils_cpp.rqa_stats(
        ds["d"], rescale=params['rescaleNorm'], rad=params['radius'], 
        diag_ignore=params['tw'], minl=params['minl'], rqa_mode="auto"
    )

    # Print stats
    if err_code == 0:
        if params['showMetrics']:
            print(f"%REC: {float(rs['perc_recur']):.3f} | %DET: {float(rs['perc_determ']):.3f} | MaxLine: {float(rs['maxl_found']):.2f}")
            print(f"Mean Line Length: {float(rs['mean_line_length']):.2f} | SD Line Length: {float(rs['std_line_length']):.2f} | Line Count: {float(rs['count_line']):.2f}")
            print(f"ENTR: {float(rs['entropy']):.3f} | LAM: {float(rs['laminarity']):.3f} | TT: {float(rs['trapping_time']):.3f}")
            print(f"Vmax: {float(rs['vmax']):.2f} | Divergence: {float(rs['divergence']):.3f}") 
            print(f"Trend_Lower: {float(rs['trend_lower_diag']):.3f} | Trend_Upper {float(rs['trend_upper_diag']):.3f}")
    else:
        print("Error in RQA computation. Check parameters and data.")

    # Plot results
    # plotMode: 'none', 'rp', 'rp_timeseries',
    plot_mode = params.get('plotMode', 'rp')
    if plot_mode == 'rp' or plot_mode == 'rp-timeseries':
        plot_rqa_results(
            dataX=dataX,
            td=td,
            plot_mode=plot_mode,
            point_size=params['pointSize'],
        )

    # Save statistics if required
    if params['doStatsFile']:
        output_io_utils.write_rqa_stats(filename, params, rs, err_code)

    return rs, td  # Return RQA statistics and recurrence plot matrix

def perform_crqa(data, params, filename):
    """
    Perform Cross Recurrence Quantification Analysis (CRQA).

    Parameters:
        data (pd.DataFrame): A DataFrame with exactly two columns representing the two time series.
        params (dict): Dictionary of CRQA parameters.

    Returns:
        dict: CRQA results.
        dict: Recurrence plot results.
    """
    # Ensure the DataFrame has exactly two columns
    if data.shape[1] != 2:
        raise ValueError("Expected a DataFrame with exactly two columns for CRQA.")

    # Extract the two time series
    dataX1 = data.iloc[:, 0].values  # First column
    dataX2 = data.iloc[:, 1].values  # Second column

    # Normalize data
    dataX1 = cleaning_utils.normalize_data(dataX1, params['norm'])
    dataX2 = cleaning_utils.normalize_data(dataX2, params['norm'])

    # Compute distance matrix for CRQA
    ds = rqa_utils_cpp.rqa_dist(dataX1, dataX2, dim=params['eDim'], lag=params['tLag'])

    # Perform RQA calculations
    td, rs, mats, err_code = rqa_utils_cpp.rqa_stats(
        ds["d"], rescale=params['rescaleNorm'], rad=params['radius'], 
        diag_ignore=params['tw'], minl=params['minl'], rqa_mode="cross"
    )

    # Print stats
    if err_code == 0:
        if params['showMetrics']:
            print(f"%REC: {float(rs['perc_recur']):.3f} | %DET: {float(rs['perc_determ']):.3f} | MaxLine: {float(rs['maxl_found']):.2f}")
            print(f"Mean Line Length: {float(rs['mean_line_length']):.2f} | SD Line Length: {float(rs['std_line_length']):.2f} | Line Count: {float(rs['count_line']):.2f}")
            print(f"ENTR: {float(rs['entropy']):.3f} | LAM: {float(rs['laminarity']):.3f} | TT: {float(rs['trapping_time']):.3f}")
            print(f"Vmax: {float(rs['vmax']):.2f} | Divergence: {float(rs['divergence']):.3f}") 
            print(f"Trend_Lower: {float(rs['trend_lower_diag']):.3f} | Trend_Upper {float(rs['trend_upper_diag']):.3f}")
    else:
        print("Error in RQA computation. Check parameters and data.")

    # Plot results
    # plotMode: 'none', 'rp', 'rp_timeseries',
    if 'rp' in params['plotMode']:
        plot_rqa_results(
            dataX=dataX1,
            dataY=dataX2,
            td=td,
            plot_mode=params['plotMode'],
            point_size=params['pointSize'],
        )

    # Write stats
    if params['doStatsFile']:
        output_io_utils.write_rqa_stats(filename, params, rs, err_code)

def plot_rqa_results(
    dataX=None, dataY=None, td=None,
    plot_mode='rp', point_size=4
):
    """
    Plot RQA or CRQA results with aligned RP and TS width.
    """

    ax_ts_x = None
    ax_ts_y = None

    N = len(dataX)
    fig = plt.figure(figsize=(8, 9))  # Squarer figure to accommodate equal width
    gs = gridspec.GridSpec(3, 2, width_ratios=[1, 12], height_ratios=[1, 12, 2], hspace=0.4, wspace=0.2)

    # === Recurrence Plot ===
    ax_rp = fig.add_subplot(gs[1, 1])
    ax_rp.set_facecolor('#b0c4de')  # Light Steel Blue, a lighter navy shade

    recur_y, recur_x = np.where(td == 1)
    ax_rp.scatter(recur_x, recur_y, c='blue', s=point_size, edgecolors='none')
    ax_rp.set_xlim([0, N])
    ax_rp.set_ylim([0, N])
    ax_rp.set_title("Cross-Recurrence Plot" if dataY is not None else "Recurrence Plot", pad=8)
    ax_rp.set_xlabel("X(i)")
    ax_rp.set_ylabel("Y(j)" if dataY is not None else "X(j)")

    # === Time Series X ===
    if 'timeseries' in plot_mode:
        ax_ts_x = fig.add_subplot(gs[2, 1], sharex=ax_rp)
        ax_ts_x.plot(np.arange(N), dataX[:N], color='tab:blue')
        ax_ts_x.set_xlim([0, N])
        ax_ts_x.set_title("Time Series X", fontsize=10)
        ax_ts_x.set_xlabel("Time")
        ax_ts_x.set_ylabel("X", rotation=0, labelpad=15)

    # === Time Series Y ===
    if dataY is not None and 'timeseries' in plot_mode:
        ax_ts_y = fig.add_subplot(gs[1, 0], sharey=ax_rp)
        ax_ts_y.plot(dataY[:N], np.arange(N), color='tab:blue')
        ax_ts_y.invert_xaxis()
        ax_ts_y.set_ylim([0, N])
        ax_ts_y.set_title("Time Series Y", fontsize=10)
        ax_ts_y.set_ylabel("Time")
        ax_ts_y.set_xlabel("Y", rotation=0, labelpad=15)

    if 'timeseries' in plot_mode:
        if ax_ts_x is not None:
            fig.align_xlabels([ax_rp, ax_ts_x])
        if ax_ts_y is not None:
            fig.align_ylabels([ax_rp, ax_ts_y])
    else:
        fig.align_xlabels([ax_rp])
        fig.align_ylabels([ax_rp])

    plt.show()
