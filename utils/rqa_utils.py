from utils import utils, plot_utils, output_io_utils
from utils import rqa_utils_cpp
import pandas as pd

def perform_rqa(data, params):
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
    dataX = utils.normalize_data(data, params['norm'])

    # Compute distance matrix for RQA
    ds = rqa_utils_cpp.rqa_dist(dataX, dataX, dim=params['eDim'], lag=params['tLag'])

    # Perform RQA calculations
    td, rs, mats, err_code = rqa_utils_cpp.rqa_stats(
        ds["d"], rescale=params['rescaleNorm'], rad=params['radius'], 
        diag_ignore=params['tw'], minl=params['minl'], rqa_mode="auto"
    )

    # Handle errors
    if err_code != 0 or not isinstance(rs, dict):
        print("Error in RQA computation. Returning empty results.")
        return {}, {}

    print(f"REC: {rs.get('perc_recur', 0):.3f} | DET: {rs.get('perc_determ', 0):.3f} | MAXLINE: {rs.get('maxl_found', 0):.2f}")

    # Plot results if required
    if params['doPlots']:
        plot_utils.plot_rqa_results(
            dataX=dataX,
            td=td,
            rs=rs,
            plot_mode=params.get('plotMode', 'recurrence'),
            phase_space=params.get('phaseSpace', False),
            eDim=params['eDim'],
            tLag=params['tLag']
        )

    # Save statistics if required
    if params['doStatsFile']:
        output_io_utils.write_rqa_stats("AutoRQA", params, rs, err_code)

    return rs, td  # Return RQA statistics and recurrence plot matrix

def perform_crqa(data, params):
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
    dataX1 = utils.normalize_data(dataX1, params['norm'])
    dataX2 = utils.normalize_data(dataX2, params['norm'])

    # Compute distance matrix for CRQA
    ds = rqa_utils_cpp.rqa_dist(dataX1, dataX2, dim=params['eDim'], lag=params['tLag'])

    # Perform RQA calculations
    td, rs, mats, err_code = rqa_utils_cpp.rqa_stats(
        ds["d"], rescale=params['rescaleNorm'], rad=params['radius'], 
        diag_ignore=params['tw'], minl=params['minl'], rqa_mode="cross"
    )

    # Handle errors
    if err_code != 0 or not isinstance(rs, dict):
        print("Error in CRQA computation. Returning empty results.")
        return {}, {}

    print(f"REC: {rs.get('perc_recur', 0):.3f} | DET: {rs.get('perc_determ', 0):.3f} | MAXLINE: {rs.get('maxl_found', 0):.2f}")

    # Plot results if required
    if params['doPlots']:
        plot_utils.plot_rqa_results(
            dataX=dataX1,
            dataY=dataX2,
            td=td,
            rs=rs,
            plot_mode=params.get('plotMode', 'recurrence'),
            phase_space=params.get('phaseSpace', False),
            eDim=params['eDim'],
            tLag=params['tLag']
        )

    # Save statistics if required
    if params['doStatsFile']:
        output_io_utils.write_rqa_stats("CrossRQA", params, rs, err_code)

    return rs, td  # Return CRQA statistics and recurrence plot matrix