from setuptools import setup, Extension
import pybind11

ext_modules = [
    Extension(
        "rqa_utils_cpp",
        ["rqa_utils.cpp"],
        include_dirs=[pybind11.get_include()],
        language="c++",
        extra_compile_args=["-std=c++14"]  # or "-std=c++17"
    )
]

setup(
    name="rqa_utils_cpp",
    ext_modules=ext_modules,
)
