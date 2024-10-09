import matplotlib.pyplot as plt

def plot_time_series(numerical_data, save_image, file_path):
    plt.figure(figsize=(10, 4))
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
    plt.figure(figsize=(6, 6))
    plt.imshow(recurrence_matrix, cmap='Blues', origin='lower')
    plt.title('Recurrence Plot')
    plt.tight_layout()
    if save_image:
        plt.savefig(file_path)
    plt.show()

def plot_ts_and_rqa(numerical_data, recurrence_matrix, save_image, file_path):
    # Create a side-by-side plot of the time series and the recurrence plot
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))

    # Plot time series
    axes[0].plot(range(len(numerical_data)), numerical_data, color='blue', linewidth=0.5)
    axes[0].set_title('Time Series')
    axes[0].set_xlabel('Time')
    axes[0].set_ylabel('Category')

    # Plot recurrence plot
    axes[1].imshow(recurrence_matrix, cmap='Blues', origin='lower')
    axes[1].set_title('Recurrence Plot')

    # Adjust layout and save/show the plot
    plt.tight_layout()
    if save_image:
        plt.savefig(file_path)
    plt.show()

def plot_windowed_ts_and_rqa(numerical_data, recurrence_matrix, save_image, file_path):
    # Create a side-by-side plot of the time series and the recurrence plot
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))

    # Plot time series for the window
    axes[0].plot(range(len(numerical_data)), numerical_data, color='blue', linewidth=0.5)
    axes[0].set_title('Time Series')
    axes[0].set_xlabel('Time')
    axes[0].set_ylabel('Value')

    # Plot recurrence plot
    axes[1].imshow(recurrence_matrix, cmap='Blues', origin='lower')
    axes[1].set_title('Recurrence Plot')

    # Adjust layout and save/show the plot
    plt.tight_layout()
    if save_image:
        plt.savefig(file_path)
    plt.show()