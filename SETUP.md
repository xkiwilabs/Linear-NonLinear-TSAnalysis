### Set-up Information

Follow these steps to set up the environment for this tutorial:

1. **Download Python**

   - Download and install Python from [https://www.python.org/downloads/](https://www.python.org/downloads/).
   - Make sure to check the box to add Python to your system PATH during installation. This will allow you to use Python from the command line.

2. **Download VS Code**

   - Download and install Visual Studio Code (VS Code) from [https://code.visualstudio.com/](https://code.visualstudio.com/).
   - VS Code is a recommended editor for working with this tutorial, offering a wide range of extensions and features that simplify Python development.
   - To work with Jupyter notebooks in VS Code, install the "Jupyter" extension from the Extensions Marketplace.

3. **Install Git**

   - Download and install Git from [https://git-scm.com/](https://git-scm.com/).
   - Git is required to clone the tutorial repository. Follow the installation instructions on the website to set up Git on your system.

4. **Clone the GitHub Repository**

   - Open a terminal (Command Prompt on Windows, Terminal on macOS/Linux).
   - Navigate to the folder where you want to clone the repository using the `cd` command.
   - Run the following command to clone the repository:
     ```sh
     git clone https://github.com/xkiwilabs/Linear-NonLinear-TSAnalysis.git
     ```

5. **Create and Activate a Virtual Environment**

   - Open a terminal (Command Prompt on Windows, Terminal on macOS/Linux).
   - Navigate to the folder where you want to store your virtual environment using the `cd` command.
   - Run the following command to create a virtual environment:
     ```sh
     python -m venv env_name
     ```
   - To activate the virtual environment, run the appropriate command for your system:
     - **For Miniconda/Conda users (Windows/macOS/Linux)**:
       ```sh
       conda create --name env_name python=3.9
       conda activate env_name
       ```
     - **On Windows**:
       ```sh
       .\env_name\Scripts\activate
       ```
     - **On macOS/Linux**:
       ```sh
       source env_name/bin/activate
       ```

6. **Install Dependencies**

   - Once the virtual environment is activated, run the following command to install the required dependencies using the provided requirements file:
     ```sh
     pip install -r requirements.txt
     ```

7. **Verify the Installation**

   - To verify that everything is set up correctly, run the following command to check the Python version:
     ```sh
     python --version
     ```
   - Also, check that pip is installed by running:
     ```sh
     pip --version
     ```
   - If you encounter any issues, refer to the official documentation for Python, VS Code, or Git for troubleshooting help.
