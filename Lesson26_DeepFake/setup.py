"""
Setup script for DeepFake Detection Tool.
Author: Yair Levi
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_file = Path(__file__).parent / 'README.md'
long_description = readme_file.read_text(encoding='utf-8') if readme_file.exists() else ''

setup(
    name='deepfake-detector',
    version='1.0.0',
    author='Yair Levi',
    description='A comprehensive tool for detecting deepfake manipulations in video files',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    python_requires='>=3.9',
    install_requires=[
        'opencv-python>=4.8.0',
        'opencv-contrib-python>=4.8.0',
        'numpy>=1.24.0',
        'scipy>=1.11.0',
        'torch>=2.1.0',
        'face-recognition>=1.3.0',
        'scikit-learn>=1.3.0',
        'pandas>=2.1.0',
    ],
    extras_require={
        'full': [
            'pymediainfo>=6.1.0',
            'tensorflow>=2.15.0',
            'mediapipe>=0.10.0',
        ],
        'dev': [
            'pytest>=7.4.0',
            'pytest-cov>=4.1.0',
            'pylint>=3.0.0',
            'black>=23.12.0',
        ],
    },
    entry_points={
        'console_scripts': [
            'deepfake-detect=deepfake_detector.main:main',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Multimedia :: Video',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)
