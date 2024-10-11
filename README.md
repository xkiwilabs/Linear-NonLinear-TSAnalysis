# Linear and Non-Linear Time Series Analysis

### Introduction

This tutorial provides examples of various linear and non-linear time series analyses for exploring the time-evolving nature of human behaviour in social and behavioral research. The goal of this tutorial is to give researchers the necessary tools and examples to perform comprehensive time series analysis using Python.

This tutorial is complemented by the following textbook chapter:

Macpherson, C., Richardson, M., & Kallen, R. W. (2024). Advanced quantitative approaches: Linear and non-linear time-series analyses. In *Cambridge handbook of research methods and statistics for the social and behavioral sciences* (Vol. 3). Cambridge University Press (CUP).

### Tutorial Authors

- **Margaret C. Macpherson** (GitHub: [cathymacpherson](https://github.com/cathymacpherson))
- **Michael J. Richardson** (GitHub: [xkiwilabs](https://github.com/xkiwilabs))

### Set-up Information

Follow these steps to set up the environment for this tutorial:

1. **Download VS Code**

   - Download and install Visual Studio Code (VS Code) from [https://code.visualstudio.com/](https://code.visualstudio.com/).
   - VS Code is a recommended editor for working with this tutorial, offering a wide range of extensions and features that simplify Python development.
   - To work with Jupyter notebooks in VS Code, install the "Jupyter" extension from the Extensions Marketplace.

2. **Clone the GitHub Repository**

   - Open a terminal and navigate to the directory where you want to clone the repository.
   - Clone the repository using the following command:
     ```sh
     git clone https://github.com/xkiwilabs/Linear-NonLinear-TSAnalysis.git
     ```

3. **Create and Activate a Virtual Environment**

   - Open a terminal and navigate to the directory where you want to store your virtual environment.
   - Create a virtual environment using the following command:
     ```sh
     python -m venv env_name
     ```
   - Activate the virtual environment:
   - For Miniconda/Conda users, you can create and activate a virtual environment with the following commands:
     ```sh
     conda create --name env_name python=3.9
     conda activate env_name
     ```
     - On Windows:
       ```sh
       .\env_name\Scripts\activate
       ```
     - On macOS/Linux:
       ```sh
       source env_name/bin/activate
       ```

4. **Install Dependencies**

   - Once the virtual environment is activated, install the required dependencies using the provided requirements file:
     ```sh
     pip install -r requirements.txt
     ```

5. **Directory Structure**

   - The data for different RQA methods should be placed in their respective directories as referenced in the code (e.g., `data/crqaContinuous/`).
   - Images and plots generated during the analysis will be saved in `images/rqa/`.

### Content Overview

The tutorial is divided into the following main sections:

1. **Categorical RQA**: Learn about Recurrence Quantification Analysis (RQA) for categorical data and its application in understanding the dynamics of categorical events.
2. **Continuous RQA**: Apply RQA to continuous time series data, providing insights into recurrence properties and temporal structures.
3. **Cross Recurrence Quantification Analysis (CRQA)**: Explore coordinated behavior between two time series.
4. **Windowed RQA**: Understand how to apply RQA in a windowed manner to observe temporal changes in recurrence properties over time.
5. **Linear Metrics**: Examine the use of linear metrics to analyze and summarize time series characteristics.
6. **FNN and AMI**: Understand the utility of False Nearest Neighbors (FNN) and Average Mutual Information (AMI) in determining appropriate embedding parameters for time series analysis.

We hope this tutorial serves as a helpful resource for delving into the world of time series analysis.
