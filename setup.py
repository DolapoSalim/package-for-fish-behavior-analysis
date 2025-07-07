"""Setup script for fish-behavior-analysis package."""

from setuptools import setup, find_packages
import os

# Read README file
def read_readme():
    with open('README.md', 'r', encoding='utf-8') as f:
        return f.read()

# Read requirements
def read_requirements():
    with open('requirements.txt', 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name="fish-behavior-analysis",
    version="0.1.0",
    author="dolapo-salim",
    author_email="dolaposalim@gmail.com",
    description="A comprehensive toolkit for analyzing fish behavior in video recordings",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/DolapoSalim/package-for-fish-behavior-analysis",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: Apache License 2.0 :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Marine Ecology/Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Marine Ecology/Science :: Image Processing/CoMputer Vision",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.812",
        ],
        "docs": [
            "sphinx>=3.0",
            "sphinx-rtd-theme>=0.5",
        ],
    },
    entry_points={
        "console_scripts": [
            "fish-behavior-analysis=fish_behavior_analysis.cli.main:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)