# Shared Level 5 - System-Wide Utilities

## Purpose
Contains utilities and resources shared across the entire BST system.
Used by root node (5_01) and accessible to all lower levels.

## Contents
- **common_types.py**: System-wide data structures and type definitions
- **constants.py**: Global constants and configuration values
- **exceptions.py**: Custom exception classes
- **utils.py**: General utility functions used across all levels
- **communication.py**: Inter-node communication protocol

## Usage
All nodes can import from this shared folder to avoid code duplication.

## Access Pattern
```python
from shared_level_5 import common_types, constants, exceptions
```
