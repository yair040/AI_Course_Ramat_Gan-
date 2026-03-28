# setup.py
# Author: Yair Levi
"""
Package setup for the AutoEncoder project.
Install in editable mode:  pip install -e .
"""

from setuptools import setup, find_packages
from pathlib import Path

_HERE = Path(__file__).parent
_LONG_DESC = (_HERE / "README.md").read_text(encoding="utf-8")

setup(
    name="autoencoder",
    version="1.0.0",
    author="Yair Levi",
    description="Convolutional AutoEncoder — cats & dogs with cross-domain experiments",
    long_description=_LONG_DESC,
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=["tests*"]),
    python_requires=">=3.10",
    install_requires=[
        "torch>=2.1.0",
        "torchvision>=0.16.0",
        "Pillow>=10.0.0",
        "matplotlib>=3.8.0",
        "numpy>=1.26.0",
        "tqdm>=4.66.0",
    ],
    extras_require={
        "dev": ["pytest>=7.0"],
    },
    entry_points={
        "console_scripts": [
            "ae-run=tasks:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: POSIX :: Linux",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
)
