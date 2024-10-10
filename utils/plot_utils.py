import matplotlib.pyplot as plt

# Set global figure size to enforce smaller plots
plt.rcParams['figure.figsize'] = (12, 5)
plt.rcParams['figure.dpi'] = 100  # Set a moderate DPI to make plots appear smaller

def plot_time_series(numerical_data, save_image, file_path):
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

def plot_ts_and_rqa(numerical_data, recurrence_matrix, rqa_metrics, save_image, file_path):
    # Create a side-by-side plot of the time series, recurrence plot, and metrics
    fig, axes = plt.subplots(1, 3, gridspec_kw={'width_ratios': [1, 1, 0.5]})

    # Plot time series
    axes[0].plot(range(len(numerical_data)), numerical_data, color='blue', linewidth=0.5)
    axes[0].set_title('Time Series')
    axes[0].set_xlabel('Time')
    axes[0].set_ylabel('Category')

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

def plot_rqa_multi_radii(recurrence_matrices, rqa_metrics_list, radii, save_image, file_path):
    # Create a plot with multiple recurrence plots for different radii
    fig, axes = plt.subplots(1, len(recurrence_matrices), figsize=(15, 5))

    for i, (recurrence_matrix, rqa_metrics, radius) in enumerate(zip(recurrence_matrices, rqa_metrics_list, radii)):
        # Plot recurrence plot
        axes[i].imshow(recurrence_matrix, cmap='Blues', origin='lower')
        axes[i].set_title(f'Recurrence Plot (Radius={radius})')

        # Display RQA metrics in the panel
        metrics_text = "\n".join([f"{key}: {value:.3f}" for key, value in rqa_metrics.items()])
        axes[i].text(0.1, -0.1, metrics_text, fontsize=8, verticalalignment='top', transform=axes[i].transAxes)

    # Adjust layout and save/show the plot
    plt.tight_layout()
    if save_image:
        plt.savefig(file_path)
    plt.show()