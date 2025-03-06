import matplotlib.pyplot as plt
import numpy as np
from matplotlib.gridspec import GridSpec
from mpl_toolkits.mplot3d import Axes3D

# Set global figure size to enforce smaller plots
plt.rcParams['figure.figsize'] = (12, 5)
plt.rcParams['figure.dpi'] = 100  # Set a moderate DPI to make plots appear smaller

def plot_time_series(numerical_data, save_image, file_path):
    numerical_data = (numerical_data - np.mean(numerical_data)) / np.std(numerical_data)
    plt.figure()
    time = range(len(numerical_data))
    plt.plot(time, numerical_data, color='blue', linewidth=0.5)
    plt.title('Time Series')
    plt.xlabel('Time')
    plt.ylabel('Category')
    plt.tight_layout()
    if save_image:
        plt.savefig(file_path)
    plt.show()

def plot_rqa(recurrence_matrix, save_image, file_path):
    plt.figure()
    plt.imshow(recurrence_matrix, cmap='Blues', origin='lower')
    plt.title('Recurrence Plot')
    plt.tight_layout()
    if save_image:
        plt.savefig(file_path)
    plt.show()

def plot_ts_and_rqa(numerical_data, recurrence_matrix, rqa_metrics, save_image, file_path, y_axis_label = 'Data'):
    numerical_data = (numerical_data - np.mean(numerical_data)) / np.std(numerical_data)
    # Create a side-by-side plot of the time series, recurrence plot, and metrics
    fig, axes = plt.subplots(1, 3, gridspec_kw={'width_ratios': [1, 1, 0.5]})

    # Plot time series
    axes[0].plot(range(len(numerical_data)), numerical_data, color='blue', linewidth=0.5)
    axes[0].set_title('Time Series')
    axes[0].set_xlabel('Time')
    axes[0].set_ylabel(y_axis_label)  # Use the new y_axis_label parameter

    # Plot recurrence plot
    axes[1].imshow(recurrence_matrix, cmap='Blues', origin='lower')
    axes[1].set_title('Recurrence Plot')

    # Display RQA metrics in the third panel
    if rqa_metrics:
        metrics_text = "\n".join([f"{key}: {value:.3f}" for key, value in rqa_metrics.items()])
    else:
        metrics_text = "No metrics available"
    axes[2].text(0.1, 0.5, metrics_text, fontsize=10, verticalalignment='center', transform=axes[2].transAxes)
    axes[2].axis('off')
    axes[2].set_title('RQA Metrics')

    # Adjust layout and save/show the plot
    plt.tight_layout()
    if save_image:
        plt.savefig(file_path)
    plt.show()

def plot_windowed_ts_and_rqa(numerical_data, recurrence_matrix, rqa_metrics, save_image, file_path):
    numerical_data = (numerical_data - np.mean(numerical_data)) / np.std(numerical_data)
    # Create a side-by-side plot of the time series, recurrence plot, and metrics
    fig, axes = plt.subplots(1, 3, gridspec_kw={'width_ratios': [1, 1, 0.5]})

    # Plot time series for the window
    axes[0].plot(range(len(numerical_data)), numerical_data, color='blue', linewidth=0.5)
    axes[0].set_title('Time Series')
    axes[0].set_xlabel('Time')
    axes[0].set_ylabel('Value')

    # Plot recurrence plot
    axes[1].imshow(recurrence_matrix, cmap='Blues', origin='lower')
    axes[1].set_title('Recurrence Plot')

    # Display RQA metrics in the third panel
    if rqa_metrics:
        metrics_text = "\n".join([f"{key}: {value:.3f}" for key, value in rqa_metrics.items()])
    else:
        metrics_text = "No metrics available"
    axes[2].text(0.1, 0.5, metrics_text, fontsize=10, verticalalignment='center', transform=axes[2].transAxes)
    axes[2].axis('off')
    axes[2].set_title('RQA Metrics')

    # Adjust layout and save/show the plot
    plt.tight_layout()
    if save_image:
        plt.savefig(file_path)
    plt.show()

import numpy as np
import matplotlib.pyplot as plt

def plot_rqa_multi_radii(recurrence_matrices, rqa_metrics_list, radii, save_image, file_path):
    """
    Plots multiple recurrence matrices with corresponding RQA metrics.

    Parameters:
        recurrence_matrices (list of np.ndarray): List of recurrence matrices to plot.
        rqa_metrics_list (list of dict): List of dictionaries containing RQA metrics for each recurrence matrix.
        radii (list of float): List of recurrence radii used for each plot.
        save_image (bool): Whether to save the plot as an image.
        file_path (str): File path for saving the plot.
    """
    
    # Limit the number of plots to 3 to ensure readability
    num_plots = min(len(recurrence_matrices), 3)
    
    # Create subplots with one row and 'num_plots' columns
    fig, axes = plt.subplots(1, num_plots, figsize=(15, 5))

    # Ensure axes is always iterable (handles case when num_plots = 1)
    if num_plots == 1:
        axes = [axes]

    # Loop through the number of plots to display
    for i in range(num_plots):
        # Copy recurrence matrix to avoid modifying the original data
        recurrence_matrix = np.array(recurrence_matrices[i], copy=True)
        # Retrieve the corresponding RQA metrics and radius
        rqa_metrics = rqa_metrics_list[i]
        radius = radii[i]

        # Select the corresponding axis
        ax = axes[i]
        # Plot the recurrence matrix with a blue colormap
        im = ax.imshow(recurrence_matrix, cmap='Blues', origin='lower')
        # Set the title with the radius value
        ax.set_title(f'Recurrence Plot (Radius={radius})')

        # Format RQA metrics as text and display it below the plot
        metrics_text = "\n".join([f"{key}: {value:.3f}" for key, value in rqa_metrics.items()])
        ax.text(0.1, -0.1, metrics_text, fontsize=8, verticalalignment='top', transform=ax.transAxes)

    # Adjust layout for better spacing
    plt.tight_layout()

    # Save the plot if requested
    if save_image:
        plt.savefig(file_path)

    # Show the final plot
    plt.show()

def plot_ts_and_dfa(numerical_data, scales, flucts, fit_line, alpha, save_image, file_path):
    numerical_data = (numerical_data - np.mean(numerical_data)) / np.std(numerical_data)
    # Create a side-by-side plot of the time series and DFA results
    fig, axes = plt.subplots(1, 2, figsize=(15, 5))

    # Plot time series
    axes[0].plot(range(len(numerical_data)), numerical_data, color='blue', linewidth=0.5)
    axes[0].set_title('Time Series')
    axes[0].set_xlabel('Time')
    axes[0].set_ylabel('Value')

    # Plot RMS of fluctuations vs. window size and show the slope (alpha) and fit line
    axes[1].loglog(scales, flucts, 'o-', label=f'Fluctuations (alpha = {alpha:.2f})')
    axes[1].loglog(scales, np.exp(fit_line), '--', label='Fit line')
    axes[1].set_title('RMS of Fluctuations vs. Window Size')
    axes[1].set_xlabel('Window size (samples)')
    axes[1].set_ylabel('RMS of fluctuations')
    axes[1].legend()

    # Adjust layout and save/show the plot
    plt.tight_layout()
    if save_image:
        plt.savefig(file_path)
    plt.show()

def plot_cm_cross_cor(cross_corr_values, save_image, file_path):
    # Create a box plot comparing cond 0 and cond 1 at lag 0
    plt.figure(figsize=(10, 6))
    plt.boxplot([cross_corr_values['cond_0'], cross_corr_values['cond_1']], labels=['Sitting', 'Standing'])
    plt.title('Cross-correlation at Lag 0: Sitting vs Standing')
    plt.ylabel('Cross-correlation values')
    plt.xlabel('Condition')
    plt.grid(True)

    # Calculate and add average cross-correlation value for each condition
    mean_cond_0 = np.mean(cross_corr_values['cond_0'])
    mean_cond_1 = np.mean(cross_corr_values['cond_1'])
    plt.text(1, mean_cond_0, f'Mean: {mean_cond_0:.2f}', horizontalalignment='center', verticalalignment='bottom', fontsize=10, color='blue')
    plt.text(2, mean_cond_1, f'Mean: {mean_cond_1:.2f}', horizontalalignment='center', verticalalignment='bottom', fontsize=10, color='blue')

    # Save or show the plot
    if save_image:
        plt.savefig(file_path)
    plt.show()

def plot_ts_and_crqa(ts_a, ts_b, recurrence_matrix, rqa_metrics, save_image, file_path):
    ts_a = (ts_a - np.mean(ts_a)) / np.std(ts_a)
    ts_b = (ts_b - np.mean(ts_b)) / np.std(ts_b)
    # Create a custom layout with GridSpec
    fig = plt.figure(figsize=(15, 6))
    spec = GridSpec(3, 3, figure=fig, width_ratios=[1, 1, 0.5], height_ratios=[1, 1, 1], hspace=0.75)

    # Plot time series A
    ax_ts_a = fig.add_subplot(spec[0, 0])
    ax_ts_a.plot(range(len(ts_a)), ts_a, color='blue', linewidth=0.5)
    ax_ts_a.set_title('Time Series A')
    ax_ts_a.set_xlabel('Time')
    ax_ts_a.set_ylabel('Value')

    # Plot time series B
    ax_ts_b = fig.add_subplot(spec[1, 0])
    ax_ts_b.plot(range(len(ts_b)), ts_b, color='green', linewidth=0.5)
    ax_ts_b.set_title('Time Series B')
    ax_ts_b.set_xlabel('Time')
    ax_ts_b.set_ylabel('Value')

    # Plot recurrence plot for CRQA
    ax_rqa = fig.add_subplot(spec[:, 1])
    ax_rqa.imshow(recurrence_matrix, cmap='Blues', origin='lower')
    ax_rqa.set_title('CRQA Recurrence Plot')

    # Display RQA metrics in the third panel
    ax_metrics = fig.add_subplot(spec[:, 2])
    if rqa_metrics:
        metrics_text = "\n".join([f"{key}: {value:.3f}" for key, value in rqa_metrics.items()])
    else:
        metrics_text = "No metrics available"
    ax_metrics.text(0.1, 0.5, metrics_text, fontsize=10, verticalalignment='center', transform=ax_metrics.transAxes)
    ax_metrics.axis('off')
    ax_metrics.set_title('CRQA Metrics')

    # Save and/or show the plot
    if save_image:
        plt.savefig(file_path)
    plt.show()

def plot_ts_and_mdrqa(dataframe, recurrence_matrix, rqa_metrics, save_image, file_path):
    # Normalize each time series in the dataframe using z-score
    normalized_data = dataframe.apply(lambda x: (x - x.mean()) / x.std(), axis=0)

    # Create a custom layout with GridSpec
    fig = plt.figure(figsize=(15, 8))
    spec = GridSpec(2, 3, figure=fig, width_ratios=[1, 1, 0.5], height_ratios=[2, 1], hspace=0.5, wspace=0.5)

    # Plot all time series on the same subplot
    ax_ts = fig.add_subplot(spec[0, 0])
    for column in normalized_data.columns:
        ax_ts.plot(range(len(normalized_data[column])), normalized_data[column], linewidth=0.5, label=f'Time Series {column}')
    ax_ts.set_title('Normalized Time Series')
    ax_ts.set_xlabel('Time')
    ax_ts.set_ylabel('Value')
    ax_ts.legend()

    # Plot recurrence plot for MdRQA
    ax_rqa = fig.add_subplot(spec[0, 1])
    ax_rqa.imshow(recurrence_matrix, cmap='Blues', origin='lower')
    ax_rqa.set_title('MdRQA Recurrence Plot')

    # Display RQA metrics in the third panel
    ax_metrics = fig.add_subplot(spec[0, 2])
    if rqa_metrics:
        metrics_text = "\n".join([f"{key}: {value:.3f}" for key, value in rqa_metrics.items()])
    else:
        metrics_text = "No metrics available"
    ax_metrics.text(0.1, 0.5, metrics_text, fontsize=10, verticalalignment='center', transform=ax_metrics.transAxes)
    ax_metrics.axis('off')
    ax_metrics.set_title('MdRQA Metrics')

    # Save and/or show the plot
    if save_image:
        plt.savefig(file_path)
    plt.show()

def plot_rqa_results(dataX, dataY=None, td=None, rs=None, plot_mode='recurrence', phase_space=False, eDim=3, tLag=1):
    """
    Plot RQA results based on the chosen mode.

    Parameters:
        dataX (np.ndarray): Time series data for X-axis.
        dataY (np.ndarray): Time series data for Y-axis (for cross-RQA).
        td (np.ndarray): Thresholded distance matrix (recurrence or cross-recurrence plot).
        rs (dict): RQA statistics dictionary (optional for display).
        plot_mode (str): 
            'recurrence': Basic recurrence plot.
            'recurrence_with_timeseries': Recurrence plot with time series underneath or to the side.
            'phase_space': Recurrence plot with phase space reconstruction.
        phase_space (bool): True to include a 2D/3D phase space plot.
        eDim (int): Embedding dimension for phase space.
        tLag (int): Time lag for phase space.
    """

    def reconstruct_phase_space(data, dim, lag):
        """ Reconstruct phase space using embedding dimension and time lag """
        n_points = len(data) - (dim - 1) * lag
        phase_space = np.array([data[i:i + n_points] for i in range(0, dim * lag, lag)]).T
        return phase_space

    plt.figure(figsize=(10, 8))

    # Plot 1: Recurrence or Cross-Recurrence Plot
    plt.subplot(2, 2, 1)
    plt.imshow((1 - td).T, cmap='gray', origin='lower')
    title = "Cross-Recurrence Plot" if dataY is not None else "Recurrence Plot"
    plt.title(title)
    plt.xlabel("X(i)")
    plt.ylabel("Y(j)" if dataY is not None else "X(j)")

    # Optionally display RQA statistics
    if rs:
        plt.figtext(0.5, 0.02, f"%REC: {rs['perc_recur']:.2f} | %DET: {rs['perc_determ']:.2f} | "
                               f"MAXLINE: {rs['maxl_found']:.0f} | MEANLINE: {rs['llmnsd'][0]:.0f} | "
                               f"ENTROPY: {rs['entropy'][0]:.2f}",
                    ha="center", fontsize=10)

    # Plot 2: Time Series - Underneath or to the side
    if plot_mode == 'recurrence_with_timeseries':
        plt.subplot(2, 2, 3)
        plt.plot(dataX, 'b-')
        plt.title("Time Series (X)")
        plt.xlabel("Sample")
        plt.ylabel("Amplitude")
        if dataY is not None:
            plt.subplot(2, 2, 4)
            plt.plot(dataY, 'g-')
            plt.title("Time Series (Y)")
            plt.xlabel("Sample")
            plt.ylabel("Amplitude")

    # Plot 3: Phase Space Reconstruction
    if phase_space:
        phase_data = reconstruct_phase_space(dataX, eDim, tLag)
        if eDim == 2:
            plt.subplot(2, 2, 4)
            plt.plot(phase_data[:, 0], phase_data[:, 1], 'b-')
            plt.title("2D Phase Space Reconstruction")
            plt.xlabel("X(t)")
            plt.ylabel(f"X(t + {tLag})")
        elif eDim >= 3:
            ax = plt.subplot(2, 2, 4, projection='3d')
            ax.plot(phase_data[:, 0], phase_data[:, 1], phase_data[:, 2], 'b-')
            ax.set_title("3D Phase Space Reconstruction")
            ax.set_xlabel("X(t)")
            ax.set_ylabel(f"X(t + {tLag})")
            ax.set_zlabel(f"X(t + {2 * tLag})")

    plt.tight_layout()
    plt.show()