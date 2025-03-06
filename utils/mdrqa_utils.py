# Import the necessary libraries
from pyrqa.time_series import TimeSeries
from pyrqa.settings import Settings
from pyrqa.analysis_type import Classic
from pyrqa.analysis_type import Cross
from pyrqa.neighbourhood import FixedRadius
from pyrqa.metric import EuclideanMetric
from pyrqa.time_series import EmbeddedSeries
from pyrqa.computation import RQAComputation, RPComputation

def perform_mrqa(data, radius=0.2, minLine=2, getRP=True):
    """
    Perform Multivariate Recurrence Quantification Analysis (MRQA) and optionally compute Recurrence Plots (RP)
    on the provided data.

    Parameters:
    data (pd.DataFrame): The input data with time series to be analyzed.
    radius (float): The radius for defining neighborhoods in phase space.
    minLine (int): The minimum line length for MRQA measures.
    getRP (bool): Whether to compute Recurrence Plots (RP). Default is True.

    Returns:
    dict: A dictionary containing MRQA results for the multivariate time series.
    dict (optional): A dictionary containing RP results for the multivariate time series, if getRP is True.
    """

    # Combine all columns into a MultiTimeSeries object
    multivariate_time_series = EmbeddedSeries(data.values.tolist())

    # Set up the settings for MRQA computation
    settings = Settings(
        multivariate_time_series,
        analysis_type=Classic,
        neighbourhood=FixedRadius(radius),
        similarity_measure=EuclideanMetric,
        theiler_corrector=1
        )

    # Perform MRQA computation
    computation = RQAComputation.create(settings)
    result = computation.run()

    # Set minimum line lengths for MRQA measures
    result.min_diagonal_line_length = minLine
    result.min_vertical_line_length = minLine
    result.min_white_vertical_line_length = minLine

    # Optionally compute the Recurrence Plot
    if getRP:
        rp_computation = RPComputation.create(settings)
        rp_result = rp_computation.run()

    # Return the results
    if getRP:
        return result, rp_result
    else:
        return result
