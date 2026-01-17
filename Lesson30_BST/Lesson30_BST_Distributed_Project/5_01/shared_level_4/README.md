# Shared Level 4 - Subsystem Coordination Utilities

## Purpose
Contains utilities for coordinating between Analysis Pipeline (4_01) and Infrastructure (4_02).
Used by nodes 4_01 and 4_02.

## Contents
- **coordination.py**: Inter-subsystem communication helpers
- **message_protocol.py**: Message format definitions for subsystem communication
- **resource_manager.py**: Shared resource allocation and management
- **aggregation.py**: Result aggregation between subsystems

## Usage
Used by nodes 4_01 and 4_02 for coordination.

## Access Pattern
```python
from shared_level_4 import coordination, message_protocol
```
