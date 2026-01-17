# Product Requirements Document
## Balanced Token Tree

**Author:** Yair Levi
**Date:** 2026-01-15
**Version:** 1.0

---

## 1. Executive Summary

The Balanced Token Tree is a Python application that demonstrates tree balancing algorithms using a Binary Search Tree (BST) structure. The program creates a 5-level tree with 16 leaves, assigns random token values, and applies a balancing algorithm to optimize token distribution.

---

## 2. Project Overview

### 2.1 Purpose
Create a visualization and processing tool for balanced token distribution across a binary tree structure using a custom balancing algorithm.

### 2.2 Target Environment
- **Platform:** Windows Subsystem for Linux (WSL)
- **Python Version:** 3.8+
- **Virtual Environment:** Located at `../../venv/` relative to project root
- **Execution:** Command-line interface with task-based architecture

---

## 3. Technical Requirements

### 3.1 Architecture
- **Package Structure:** Modular package with `__init__.py` files
- **File Organization:** Each Python file limited to 150 lines maximum
- **Path Management:** All paths must be relative, no absolute paths
- **Concurrency:** Use multiprocessing where applicable for performance

### 3.2 Logging System
- **Library:** Python `logging` module
- **Log Level:** INFO and above
- **Format:** Ring buffer rotation
- **File Count:** 20 log files
- **File Size:** 16 MB per file
- **Location:** `./log/` subfolder
- **Rotation:** When file 20 is full, overwrite file 1 (circular)

### 3.3 Dependencies
- `matplotlib` or `networkx` for tree visualization
- `multiprocessing` for parallel processing
- Standard library modules for logging and file operations

---

## 4. Functional Requirements

### 4.1 Tree Structure
**Requirement:** Create a complete BST with 5 levels

- **Level 1 (Leaves):** 16 nodes named `1_1` to `1_16`
- **Level 2:** 8 nodes named `2_1` to `2_8`
- **Level 3:** 4 nodes named `3_1` to `3_4`
- **Level 4:** 2 nodes named `4_1` to `4_2`
- **Level 5 (Root):** 1 node named `5_1`

**Parent-Child Relationships:**
- Each node at level N has exactly 2 children at level N-1
- Leaves (Level 1) have no children

### 4.2 Token Assignment (Initial)
**Requirement:** Randomly assign tokens to leaves

- Each leaf receives a random integer between 0 and 1000 (inclusive)
- Parent nodes calculate their value as the sum of their children's values
- Propagate sums upward to the root

### 4.3 Tree Visualization
**Requirement:** Display tree structure with token values

- Show all nodes with their names and token counts
- Display parent-child relationships
- Save visualization as image file
- Generate both initial and balanced tree visualizations

### 4.4 Balancing Algorithm
**Requirement:** Redistribute tokens to balance the tree

**Algorithm Steps:**
1. **Extract:** Collect all leaf token values into an array
2. **Sort:** Sort array by token count (ascending or descending)
3. **Clear:** Remove all token values from leaves and internal nodes
4. **Pair:** Take the largest and smallest values from sorted array
5. **Assign:** Place the pair in two leaves under the same parent
6. **Remove:** Delete the two values from the array
7. **Repeat:** Continue steps 4-6 until array is empty
8. **Propagate:** Recalculate parent node values from leaves to root

**Goal:** Minimize variance in token distribution across parent nodes

### 4.5 Iteration
**Requirement:** Run 2 complete balancing iterations with different data

**Iteration 0:**
- Assign random tokens (0-1000) to leaves
- Visualize initial distribution
- Apply balancing algorithm
- Visualize balanced result

**Iteration 1:**
- Assign NEW random tokens (0-1000) to leaves
- Visualize new initial distribution
- Apply balancing algorithm
- Visualize balanced result

This demonstrates the algorithm's effectiveness on different initial distributions.

---

## 5. Non-Functional Requirements

### 5.1 Performance
- Tree creation and balancing should complete within seconds
- Use multiprocessing for independent operations (visualization, calculations)
- Efficient memory usage for tree structure

### 5.2 Maintainability
- Modular code structure with clear separation of concerns
- Comprehensive logging for debugging
- Type hints where applicable
- Docstrings for all public functions and classes

### 5.3 Usability
- Clear console output showing progress
- Meaningful log messages
- Generated visualizations saved with descriptive names
- Easy to run via main entry point

---

## 6. Deliverables

### 6.1 Documentation
- `PRD.md` - This document
- `Claude.md` - Claude Code development context
- `planning.md` - Technical architecture and design decisions
- `tasks.md` - Implementation task breakdown
- `README.md` - User guide and setup instructions

### 6.2 Code
- Package structure with `__init__.py`
- Main entry point module
- Tree data structure module
- Balancing algorithm module
- Visualization module
- Logging configuration module
- Task orchestration module

### 6.3 Configuration
- `requirements.txt` - Python dependencies
- Logging configuration (programmatic)

### 6.4 Output
- Tree visualization images (PNG/PDF)
- Log files in `./log/` directory
- Console output showing results

---

## 7. Success Criteria

1. ✅ Tree with correct structure (5 levels, proper naming)
2. ✅ Random token assignment working correctly
3. ✅ Balancing algorithm produces more balanced distribution
4. ✅ Visualizations clearly show tree structure and values
5. ✅ Logging system works with ring buffer rotation
6. ✅ All files under 150 lines
7. ✅ Works in WSL environment with virtual environment
8. ✅ Uses relative paths throughout

---

## 8. Future Enhancements (Out of Scope)

- Support for trees with different depths
- Alternative balancing algorithms
- Interactive GUI
- Real-time visualization
- Performance metrics comparison
- Export to different formats (JSON, XML)

---

## 9. Assumptions and Constraints

### Assumptions
- User has Python 3.8+ installed in WSL
- Virtual environment already created at `../../venv/`
- User has basic command-line knowledge
- Matplotlib backend supports WSL (or headless operation)

### Constraints
- Maximum 150 lines per Python file
- Fixed tree structure (5 levels, 16 leaves)
- Ring buffer limited to 20 files of 16MB each
- Token range fixed at 0-1000

---

## 10. Glossary

- **BST:** Binary Search Tree
- **Token:** A numerical value assigned to tree nodes
- **Ring Buffer:** Circular file rotation system
- **WSL:** Windows Subsystem for Linux
- **Leaf:** Terminal node with no children
- **Internal Node:** Non-leaf node with children
- **Root:** Top-level node of the tree

---

## Appendix A: Example Tree Structure

```
                    5_1
                   /    \
                4_1      4_2
               /  \      /  \
            3_1   3_2  3_3  3_4
            / \   / \  / \  / \
          2_1 2_2 ...      ... 2_8
          / \ / \              / \
        1_1 ... ...          ... 1_16
```

---

**Document Status:** Final
**Next Review Date:** As needed during development
