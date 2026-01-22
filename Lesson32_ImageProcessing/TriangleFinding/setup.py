"""
Setup script for Triangle Edge Detection System.
Author: Yair Levi
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read requirements
requirements_path = Path(__file__).parent / 'requirements.txt'
with open(requirements_path) as f:
    requirements = [
        line.strip() 
        for line in f 
        if line.strip() and not line.startswith('#')
    ]

setup(
    name='triangle-edge-detection',
    version='1.0.0',
    author='Yair Levi',
    description='Triangle edge detection using frequency domain filtering',
    long_description='A Python application for detecting triangle edges using FFT-based frequency domain filtering with interactive threshold adjustment.',
    python_requires='>=3.8',
    packages=find_packages(),
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'triangle-edge-detection=main:main',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering :: Image Processing',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)