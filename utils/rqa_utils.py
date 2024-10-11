# Import the necessary libraries
from pyrqa.time_series import TimeSeries
from pyrqa.settings import Settings
from pyrqa.analysis_type import Classic
from pyrqa.analysis_type import Cross
from pyrqa.neighbourhood import FixedRadius
from pyrqa.metric import EuclideanMetric
from pyrqa.time_series import EmbeddedSeries
from pyrqa.computation import RQAComputation, RPComputation

# Define the RQA functions
def perform_rqa(data, delay=15, embedding_dimension=3, radius=0.2, minLine=2, getRP=True):
    """
    Perform Recurrence Quantification Analysis (RQA) and optionally compute Recurrence Plots (RP) 
    on the provided data.

    Parameters:
    data (pd.DataFrame): The input data with time series to be analyzed.
    delay (int): The time delay for embedding.
    embedding_dimension (int): The embedding dimension for the time series.
    radius (float): The radius for defining neighborhoods in phase space.
    minLine (int): The minimum line length for RQA measures.
    getRP (bool): Whether to compute Recurrence Plots (RP). Default is True.

    Returns:
    dict: A dictionary containing RQA results for each column.
    dict (optional): A dictionary containing RP results for each column, if getRP is True.
    """
    rqa_results = {}  # Dictionary to store RQA results
    rp_results = {}  # Dictionary to store RP results (if getRP is True)
    
    for column in data.columns:
        # Create a time series object for the current column
        time_series = TimeSeries(data[column], embedding_dimension=embedding_dimension, time_delay=delay)
        
        # Set up the settings for RQA computation
        settings = Settings(
            time_series,
            analysis_type=Classic,
            neighbourhood=FixedRadius(radius),
            similarity_measure=EuclideanMetric
        )
        
        # Perform RQA computation
        computation = RQAComputation.create(settings)
        result = computation.run()
        
        # Set minimum line lengths for RQA measures
        result.min_diagonal_line_length = minLine
        result.min_vertical_line_length = minLine
        result.min_white_vertical_line_length = minLine
        
        # Store the RQA result
        rqa_results[column] = result
        
        # Optionally compute the Recurrence Plot
        if getRP:
            rp_computation = RPComputation.create(settings)
            rp_result = rp_computation.run()
            rp_results[column] = rp_result
    
    # Return the results
    if getRP:
        return rqa_results, rp_results
    else:
        return rqa_results


# Function to perform CRQA
def perform_crqa(data, delay=15, embedding_dimension=3, radius=0.2, minLine=2, getRP=True):
    """
    Perform Cross Recurrence Quantification Analysis (CRQA) and optionally compute Cross Recurrence Plots (CRP) 
    on the provided data.

    Parameters:
    data (pd.DataFrame): The input data with time series to be analyzed.
    delay (int): The time delay for embedding.
    embedding_dimension (int): The embedding dimension for the time series.
    radius (float): The radius for defining neighborhoods in phase space.
    minLine (int): The minimum line length for CRQA measures.
    getRP (bool): Whether to compute Cross Recurrence Plots (CRP). Default is True.

    Returns:
    dict: A dictionary containing CRQA results for each pair of columns.
    dict (optional): A dictionary containing CRP results for each pair of columns, if getRP is True.
    """
    crqa_results = {}
    crp_results = {}

    time_series1 = TimeSeries(data.iloc[:, 0], embedding_dimension=embedding_dimension, time_delay=delay)
    time_series2 = TimeSeries(data.iloc[:, 1], embedding_dimension=embedding_dimension, time_delay=delay)

    settings = Settings(
        (time_series1, time_series2),
        analysis_type=Cross,
        neighbourhood=FixedRadius(radius),
        similarity_measure=EuclideanMetric
    )

    computation = RQAComputation.create(settings)
    result = computation.run()

    result.min_diagonal_line_length = minLine
    result.min_vertical_line_length = minLine
    result.min_white_vertical_line_length = minLine

    crqa_results['0_1'] = result

    if getRP:
        crp_computation = RPComputation.create(settings)
        crp_result = crp_computation.run()
        crp_results['0_1'] = crp_result

    if getRP:
        return crqa_results, crp_results
    else:
        return crqa_results
    

def perform_mrqa(data, radius=0.2, minLine=2, getRP=True):
    """
    Perform Multivariate Recurrence Quantification Analysis (MRQA) and optionally compute Recurrence Plots (RP)
    on the provided data.

    Parameters:
    data (pd.DataFrame): The input data with time series to be analyzed.
    delay (int): The time delay for embedding.
    embedding_dimension (int): The embedding dimension for the time series.
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
