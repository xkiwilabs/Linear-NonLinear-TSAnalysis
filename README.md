# Linear and Non-Linear Time Series Analysis

### Introduction

This tutorial provides examples of various linear and non-linear time series analyses for exploring the time-evolving nature of human behaviour in social and behavioural research. The goal of this tutorial is to give researchers the necessary tools and examples to perform comprehensive time series analysis using Python.

This tutorial is complemented by the following textbook chapter:

Macpherson, C., Richardson, M., & Kallen, R. W. (2024). Advanced quantitative approaches: Linear and non-linear time-series analyses. In *Cambridge handbook of research methods and statistics for the social and behavioral sciences* (Vol. 3). Cambridge University Press (CUP).&#x20;

### Tutorial Authors

- **Margaret C. Macpherson** (GitHub: [cathymacpherson](https://github.com/cathymacpherson))
- **Michael J. Richardson** (GitHub: [xkiwilabs](https://github.com/xkiwilabs))

### Set-up Information

Follow these steps to set up the environment for this tutorial:

1. **Download VS Code**

   - Download and install Visual Studio Code (VS Code) from [https://code.visualstudio.com/](https://code.visualstudio.com/).
   - VS Code is a recommended editor for working with this tutorial, offering a wide range of extensions and features that simplify Python development, particularly for those working with time series analysis.
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
     - For Miniconda/Conda users:
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

### Content Overview

The tutorial is divided into the following main sections:

1. [**Categorical Recurrence Quantification Analysis (catRQA)**](rqaCategorical.ipynb): Learn about RQA for categorical data and its application in understanding the dynamics of categorical events.
2. [**Continuous Recurrence Quantification Analysis (contRQA)**](rqaContinuous.ipynb) Apply RQA to continuous time series data, providing insights into recurrence properties and temporal structures.
3. [**Cross Recurrence Quantification Analysis (CRQA)**](crqaContinuous.ipynb): Explore the coordinated behaviour between two time series.
4. [**Windowed RQA**](rqaWindowed.ipynb): Understand how to apply RQA in a windowed manner, to observe temporal changes in recurrence properties over time.
5. **False Nearest Neighbours (FNN) and Average Mutual Information (AMI)**: Understand the utility of these methods in determining appropriate embedding parameters for time series analysis.
6. **Detrended Fluctuation Analysis (DFA)**: Learn about DFA, a method used to detect long-term statistical dependencies in time series data. DFA is particularly useful for analysing non-stationary processes where traditional methods may not apply.
7. **Windowed DFA**: Understand how to apply DFA in a windowed manner to assess how fluctuation patterns evolve over time.
8. **Linear Metrics**: Examine the use of linear metrics to analyse and summarise time series characteristics.

We hope this tutorial serves as a helpful resource for delving into the world of time-evolving human behaviour analysis. 
