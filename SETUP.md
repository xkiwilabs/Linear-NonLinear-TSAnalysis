## **Set-up Information**

Follow these steps to set up the environment for this tutorial:

---

### **1. Download Python**
- Download and install Python from [https://www.python.org/downloads/](https://www.python.org/downloads/).
- **Make sure to check the box to add Python to your system PATH** during installation. This will allow you to use Python from the command line.

---

### **2. Download VS Code**
- Download and install Visual Studio Code (VS Code) from [https://code.visualstudio.com/](https://code.visualstudio.com/).
- VS Code is recommended for this tutorial because of its extensions and Python support.
- To work with Jupyter notebooks in VS Code, install the `Jupyter` extension from the Extensions Marketplace.

---

### **3. Install Git**
- Download and install Git from [https://git-scm.com/](https://git-scm.com/).
- Git is required to clone the tutorial repository. Follow the installation instructions on the website to set up Git on your system.
- After installation, verify it by running:
  ```sh
  git --version
  ```

---

### **4. Clone the GitHub Repository**
- Open a terminal (**Command Prompt** on Windows, **Terminal** on macOS/Linux).
- Navigate to the folder where you want to clone the repository using `cd`:
  ```sh
  cd path/to/your/folder
  ```
- Clone the repository:
  ```sh
  git clone https://github.com/xkiwilabs/Linear-NonLinear-TSAnalysis.git
  ```

---

### **5. Create and Activate a Virtual Environment**
A virtual environment helps isolate dependencies for this tutorial.

- Open a terminal (**Command Prompt on Windows, Terminal on macOS/Linux**).
- Navigate to the cloned repository:
  ```sh
  cd Linear-NonLinear-TSAnalysis
  ```
- Create a virtual environment:
  ```sh
  python -m venv env_name
  ```
- **Activate the virtual environment**:
  - **For Conda users**:
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

---

### **6. Install Dependencies**
Once the virtual environment is activated, install the required dependencies:
```sh
pip install -r requirements.txt
```

---

### **7. Compile the C++ Code**
This tutorial includes **C++ extensions** that need to be compiled before use.

#### **7.1 Ensure a C++ Compiler Is Installed**
A **C++ compiler is required** to build the extension. Check if one is installed:

**For Windows (Microsoft Visual C++ Compiler)**:
```sh
cl
```
If `cl` is not found:
- Install **Visual Studio Build Tools**:  
  [https://visualstudio.microsoft.com/visual-cpp-build-tools/](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
- Restart your terminal and ensure `cl` is detected.

**For macOS/Linux (GCC/Clang)**:
```sh
g++ --version
```
If missing, install it:
- **macOS**:
  ```sh
  xcode-select --install
  ```
- **Ubuntu/Debian Linux**:
  ```sh
  sudo apt install g++
  ```

---

#### **7.2 Build the C++ Code**
Once a C++ compiler is installed and available in your terminal, compile the code:
```sh
python setup.py build_ext --inplace
```
This will automatically detect the compiler, configure the environment if needed, and generate a `.pyd` (Windows) or `.so` (macOS/Linux) file that Python can use.

---

### **8. Verify the Installation**
Run these commands to check if everything is set up correctly:

```sh
python --version
pip --version
```

If you encounter any issues, please refer to the official documentation for Python, VS Code, or Git for help troubleshooting.

