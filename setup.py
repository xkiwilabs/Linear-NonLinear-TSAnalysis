import os
import sys
import subprocess
from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
from setuptools import setup, Extension, find_packages
import pybind11

class BuildExt(build_ext):
    """Custom build command to check for C++ compiler before compiling"""

    def run(self):
        self.check_cpp_compiler()
        super().run()

    def check_cpp_compiler(self):
        """Automatically detect MSVC and set environment if missing"""
        if sys.platform == "win32":
            try:
                subprocess.run(["cl"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            except (FileNotFoundError, subprocess.CalledProcessError):
                print("\nMSVC compiler not found. Attempting to load it...")
                vs_path = r"C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvars64.bat"
                if os.path.exists(vs_path):
                    print(f"Loading MSVC environment from: {vs_path}")
                    subprocess.call(f'call "{vs_path}"', shell=True)
                else:
                    sys.stderr.write("Error: No C++ compiler found. Install MSVC before proceeding.\n")
                    sys.exit(1)

setup(
    name="lnl_ts_analysis",
    version="0.1",
    author="Mike Richardson, Cathy Macpherson",
    description="A tutorial on linear and nonlinear time series analysis, including RQA.",
    url="https://github.com/xkiwilabs/Linear-NonLinear-TSAnalysis",
    packages=find_packages(),
    ext_modules=[
        Extension(
            "utils.rqa_utils_cpp",
            sources=["utils/rqa_utils.cpp"],
            include_dirs=[pybind11.get_include()],
            language="c++",
            extra_compile_args=["-std=c++14"],
        ),
    ],
    cmdclass={"build_ext": BuildExt},
    install_requires=open("requirements.txt").read().splitlines(),
    python_requires=">=3.6",
)
