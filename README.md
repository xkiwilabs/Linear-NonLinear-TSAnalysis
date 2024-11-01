# Linear and Non-Linear Time Series Analysis

### Introduction

This tutorial provides examples of various linear and non-linear time series analyses for exploring the time-evolving nature of human behaviour in social and behavioural research. The goal of this tutorial is to give researchers the necessary tools and examples to perform comprehensive time series analysis using Python.

This tutorial is complemented by the following textbook chapter:

Macpherson, C., Richardson, M., & Kallen, R. W. (2024). Advanced quantitative approaches: Linear and non-linear time-series analyses. In *Cambridge handbook of research methods and statistics for the social and behavioral sciences* (Vol. 3). Cambridge University Press (CUP).

### Tutorial Authors

- **Margaret C. Macpherson** (GitHub: [cathymacpherson](https://github.com/cathymacpherson))
- **Michael J. Richardson** (GitHub: [xkiwilabs](https://github.com/xkiwilabs))

---

### Set-up Information

- For novice users: 
  - Please refer to the [set up instructions](SETUP.md) for full details regarding how to set up the environment for this tutorial.
- For users familiar with python and Visual Studio Code: 
  - [VS Code](https://code.visualstudio.com/) is the recommended editor for this tutorial. To work with Jupyter notebooks in VS Code, ensure that the "Jupyter" extension has been installed.
  - The GitHub Repository can be cloned from here: https://github.com/xkiwilabs/Linear-NonLinear-TSAnalysis.git
  - To install the required dependencies, use:
       ```sh
     pip install -r requirements.txt 
    ```

--- 

### Content Overview

The tutorial is divided into the following sections:

1. **Recurrence Quantification Analysis**
   - [**Categorical RQA**](rqaCategorical.ipynb): Learn about RQA for categorical data and its application in understanding the dynamics of categorical events.
   - [**Continuous RQA**](rqaContinuous.ipynb): Apply RQA to continuous time series data, providing insights into the temporal structure of continuous data.
   - [**Windowed (C)RQA**](rqaWindowed.ipynb): Understand how to apply RQA in a windowed manner to observe temporal changes in recurrence over time.
2. **Cross Recurrence Quantification Analysis**
   - [**Categorical CRQA**](crqaCategorical.ipynb): Explore coordinated behaviour between two categorical time series.
   - [**Continuous CRQA**](crqaContinuous.ipynb): Explore coordinated behaviour between two continuous time series.
   - [**Multidimensional Recurrence Quantification Analysis (mdRQA)**](mdrqaContinuous.ipynb): Learn how to apply RQA to multivariate data.
5. **Phase Space Reconstruction**
    - [**Average Mutual Information (AMI)**](ami.ipynb): Learn how to determine the appropriate delay RQA.
    - [**False Nearest Neighbours (FNN)**](fnn.ipynb): Learn how to select the appropriate embedding dimension for RQA. 
7. **Fractal Analysis**
    - [**Detrended Fluctuation Analysis (DFA)**](dfaAnalysis.ipynb): Learn about DFA, a method used to detect long-term statistical dependencies in time series data. DFA is particularly useful for analysing non-stationary processes where traditional methods may not apply.
    - [**Windowed DFA**](dfaWindowed.ipynb): Understand how to apply DFA in a windowed manner to assess how patterns of variability evolve over time.
    - [**Complexity Matching**](complexityMatching.ipynb): Learn about various methods for capturing the alignment of variability across time series, also known as complexity matching. 
10. [**Linear Metrics**](linearAnalyses.ipynb): *COMING SOON* Examine the use of linear metrics to analyse and summarise time series characteristics.

We hope this tutorial serves as a helpful resource for delving into the world of using time series analysis in social and behavioural research. 

---

### References

This tutorial employs tools from [PyRQA](https://pypi.org/project/PyRQA/) to run RQA:

Rawald, T., Sips, M., & Marwan, N. (2017). PyRQA: Conducting recurrence quantification analysis on very long time series efficiently. *Computers & Geosciences, 104*, 101-108.