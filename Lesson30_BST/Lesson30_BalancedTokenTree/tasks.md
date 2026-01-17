# Implementation Tasks
## Balanced Token Tree Project

**Author:** Yair Levi
**Purpose:** Step-by-step implementation guide

---

## Task Overview

This document breaks down the implementation into manageable tasks. Each task should result in working, testable code. Follow the order for smooth integration.

**Total Estimated Tasks:** 15
**Approach:** Bottom-up (core structures first, then integration)

---

## Phase 1: Project Setup

### Task 1.1: Create Project Structure
**Priority:** High
**Estimated Effort:** 10 minutes
**Dependencies:** None

**Steps:**
1. Create main package directory: `balanced_token_tree/`
2. Create subdirectories:
   - `log/` (for log files)
   - `output/` (for visualizations)
3. Create `.gitignore` if using version control
4. Verify directory structure

**Deliverables:**
- Directory structure matches planning.md
- All directories created with proper permissions

**Verification:**
```bash
ls -la
# Should show: balanced_token_tree/, log/, output/
```

---

### Task 1.2: Set Up Virtual Environment
**Priority:** High
**Estimated Effort:** 5 minutes
**Dependencies:** Task 1.1

**Steps:**
1. Navigate to `../../` from project root
2. Create virtual environment: `python3 -m venv venv`
3. Activate: `source ../../venv/bin/activate` (WSL)
4. Verify activation: `which python`

**Deliverables:**
- Virtual environment at `../../venv/`
- Activation works correctly

**Verification:**
```bash
which python
# Should show: ../../venv/bin/python
```

---

### Task 1.3: Create requirements.txt
**Priority:** High
**Estimated Effort:** 5 minutes
**Dependencies:** None

**Steps:**
1. Create `requirements.txt` in project root
2. Add dependencies:
   - `matplotlib>=3.5.0`
   - `numpy>=1.21.0`
3. Install: `pip install -r requirements.txt`

**Deliverables:**
- `requirements.txt` with all dependencies
- Dependencies installed in venv

**Verification:**
```bash
pip list
# Should show matplotlib, numpy
```

---

## Phase 2: Core Data Structures

### Task 2.1: Implement TreeNode Class
**Priority:** High
**Estimated Effort:** 30 minutes
**Dependencies:** Task 1.2
**File:** `balanced_token_tree/tree_structure.py`
**Line Limit:** 100 lines

**Steps:**
1. Create `tree_structure.py`
2. Import necessary types from `typing`
3. Implement `TreeNode` class with:
   - `__init__(name: str, level: int)`
   - Attributes: name, level, token_count, left_child, right_child, parent
   - `is_leaf() -> bool`
   - `set_tokens(count: int) -> None`
   - `calculate_sum() -> int` (recursive)
   - `__repr__() -> str`
4. Add type hints to all methods
5. Add docstrings

**Deliverables:**
- `TreeNode` class fully implemented
- Type hints on all methods
- Docstrings for class and methods

**Verification:**
```python
node = TreeNode("1_1", 1)
assert node.name == "1_1"
assert node.level == 1
assert node.is_leaf() == True
```

---

### Task 2.2: Implement BinaryTree Class
**Priority:** High
**Estimated Effort:** 45 minutes
**Dependencies:** Task 2.1
**File:** `balanced_token_tree/tree_structure.py`

**Steps:**
1. Add `BinaryTree` class to same file
2. Implement attributes:
   - `root: TreeNode`
   - `leaves: List[TreeNode]`
   - `all_nodes: List[TreeNode]`
3. Implement methods:
   - `__init__(root: TreeNode, leaves: List[TreeNode])`
   - `get_nodes_by_level(level: int) -> List[TreeNode]`
   - `get_all_leaves_sorted() -> List[TreeNode]`
   - `reset_tokens() -> None`
   - `calculate_all_sums() -> None`
4. Add `build_tree() -> BinaryTree` function (creates 5-level tree)

**Deliverables:**
- `BinaryTree` class complete
- `build_tree()` function creates correct structure
- All nodes properly named and linked

**Verification:**
```python
tree = build_tree()
assert len(tree.leaves) == 16
assert tree.root.name == "5_1"
assert tree.root.level == 5
assert tree.leaves[0].name == "1_1"
```

---

## Phase 3: Token Management

### Task 3.1: Implement Token Assignment
**Priority:** High
**Estimated Effort:** 25 minutes
**Dependencies:** Task 2.2
**File:** `balanced_token_tree/token_manager.py`
**Line Limit:** 80 lines

**Steps:**
1. Create `token_manager.py`
2. Import `random`, `typing`, and `TreeNode`
3. Implement functions:
   - `assign_random_tokens(leaves: List[TreeNode], min_val: int, max_val: int, seed: Optional[int] = None) -> None`
   - `extract_leaf_tokens(leaves: List[TreeNode]) -> List[int]`
   - `assign_token_list(leaves: List[TreeNode], tokens: List[int]) -> None`
4. Add docstrings and type hints

**Deliverables:**
- Token assignment functions working
- Random seed support for reproducibility
- Token extraction working

**Verification:**
```python
tree = build_tree()
assign_random_tokens(tree.leaves, 0, 1000, seed=42)
tokens = extract_leaf_tokens(tree.leaves)
assert len(tokens) == 16
assert all(0 <= t <= 1000 for t in tokens)
```

---

## Phase 4: Balancing Algorithm

### Task 4.1: Implement Balancing Core
**Priority:** High
**Estimated Effort:** 35 minutes
**Dependencies:** Task 3.1
**File:** `balanced_token_tree/balancing.py`
**Line Limit:** 90 lines

**Steps:**
1. Create `balancing.py`
2. Import necessary modules
3. Implement functions:
   - `sort_tokens(tokens: List[int]) -> List[int]`
   - `create_balanced_pairs(sorted_tokens: List[int]) -> List[Tuple[int, int]]`
   - `pair_leaves_by_parent(leaves: List[TreeNode]) -> List[Tuple[TreeNode, TreeNode]]`
4. Test with known values

**Deliverables:**
- Pairing algorithm works correctly
- Sorts and pairs extremes
- Leaf pairing matches tree structure

**Verification:**
```python
tokens = [100, 200, 300, 400, 500, 600, 700, 800]
pairs = create_balanced_pairs(sorted(tokens))
assert pairs == [(100, 800), (200, 700), (300, 600), (400, 500)]
```

---

### Task 4.2: Implement Balancing Application
**Priority:** High
**Estimated Effort:** 30 minutes
**Dependencies:** Task 4.1
**File:** `balanced_token_tree/balancing.py`

**Steps:**
1. Add function: `apply_balancing(tree: BinaryTree, iteration: int) -> Dict[str, Any]`
2. Implementation:
   - Extract leaf tokens
   - Create balanced pairs
   - Reset tree tokens
   - Assign balanced pairs
   - Recalculate sums
   - Calculate statistics
3. Add `calculate_statistics(tree: BinaryTree) -> Dict[str, float]`
   - Calculate variance, std dev, min, max for each level

**Deliverables:**
- Full balancing application working
- Statistics calculation accurate
- Token conservation verified

**Verification:**
```python
tree = build_tree()
assign_random_tokens(tree.leaves, 0, 1000, seed=42)
initial_sum = tree.root.calculate_sum()
stats = apply_balancing(tree, 1)
final_sum = tree.root.calculate_sum()
assert initial_sum == final_sum
```

---

## Phase 5: Logging System

### Task 5.1: Implement Logging Configuration
**Priority:** Medium
**Estimated Effort:** 25 minutes
**Dependencies:** Task 1.1
**File:** `balanced_token_tree/logger_config.py`
**Line Limit:** 70 lines

**Steps:**
1. Create `logger_config.py`
2. Import `logging`, `logging.handlers`, `pathlib`
3. Implement `setup_logging(log_dir: str = "./log", level: int = logging.INFO) -> logging.Logger`
4. Use `RotatingFileHandler`:
   - `maxBytes=16 * 1024 * 1024` (16 MB)
   - `backupCount=19` (total 20 files)
5. Set formatter: `'%(asctime)s - %(name)s - %(levelname)s - %(message)s'`
6. Create log directory if not exists

**Deliverables:**
- Logging configuration working
- Ring buffer rotation configured
- Log directory created automatically

**Verification:**
```python
logger = setup_logging()
logger.info("Test message")
# Check log/app.log exists and contains message
```

---

## Phase 6: Visualization

### Task 6.1: Implement Position Calculation
**Priority:** High
**Estimated Effort:** 40 minutes
**Dependencies:** Task 2.2
**File:** `balanced_token_tree/visualization.py`
**Line Limit:** 140 lines

**Steps:**
1. Create `visualization.py`
2. Configure matplotlib for WSL: `matplotlib.use('Agg')`
3. Import `matplotlib.pyplot`, `BinaryTree`
4. Implement `calculate_node_positions(tree: BinaryTree) -> Dict[str, Tuple[float, float]]`
   - Position leaves evenly on x-axis
   - Position parents centered between children
   - Y-coordinate based on level
5. Test with known tree structure

**Deliverables:**
- Position calculation working
- Positions logical and well-spaced
- No node overlaps

**Verification:**
```python
tree = build_tree()
positions = calculate_node_positions(tree)
assert len(positions) == 31  # 31 total nodes
assert positions["5_1"][1] == 4  # Root at y=4
```

---

### Task 6.2: Implement Tree Drawing
**Priority:** High
**Estimated Effort:** 45 minutes
**Dependencies:** Task 6.1
**File:** `balanced_token_tree/visualization.py`

**Steps:**
1. Add `draw_tree(tree: BinaryTree, output_path: str, title: str) -> None`
2. Implementation:
   - Create figure with appropriate size (16x10)
   - Calculate positions
   - Draw edges between parent-child nodes
   - Draw nodes as circles (scatter plot)
   - Add labels with name and token count
   - Color by level or node type
   - Save to file
3. Create output directory if not exists

**Deliverables:**
- Tree visualization renders correctly
- Nodes labeled with name and tokens
- Edges show parent-child relationships
- Image saved to output/

**Verification:**
```python
tree = build_tree()
assign_random_tokens(tree.leaves, 0, 1000, seed=42)
tree.calculate_all_sums()
draw_tree(tree, "output/test.png", "Test Tree")
# Check output/test.png exists and is valid
```

---

## Phase 7: Task Orchestration

### Task 7.1: Implement Task Functions
**Priority:** High
**Estimated Effort:** 40 minutes
**Dependencies:** Tasks 2.2, 3.1, 4.2, 6.2
**File:** `balanced_token_tree/tasks.py`
**Line Limit:** 130 lines

**Steps:**
1. Create `tasks.py`
2. Import all necessary modules
3. Implement task functions:
   - `task_create_tree() -> BinaryTree`
   - `task_initial_tokens(tree: BinaryTree, seed: Optional[int] = None) -> int`
   - `task_balance_iteration(tree: BinaryTree, iteration: int) -> Dict[str, Any]`
   - `task_visualize(tree: BinaryTree, iteration: int, label: str) -> None`
4. Add logging to each task
5. Add error handling

**Deliverables:**
- All task functions implemented
- Logging at each step
- Error handling for common issues

**Verification:**
```python
tree = task_create_tree()
total = task_initial_tokens(tree, seed=42)
assert total > 0
```

---

### Task 7.2: Implement Pipeline Orchestration
**Priority:** High
**Estimated Effort:** 30 minutes
**Dependencies:** Task 7.1
**File:** `balanced_token_tree/tasks.py`

**Steps:**
1. Add `run_pipeline(seed: Optional[int] = None) -> None`
2. Implementation:
   - Create tree
   - Assign initial tokens and visualize (iteration 0)
   - Balance and visualize (iteration 1)
   - Balance and visualize (iteration 2)
   - Log statistics at each step
   - Print summary to console
3. Add exception handling
4. Log pipeline start and completion

**Deliverables:**
- Complete pipeline working end-to-end
- Three visualizations generated
- Statistics logged

**Verification:**
```bash
python -c "from balanced_token_tree.tasks import run_pipeline; run_pipeline(seed=42)"
# Should generate 3 visualization files
```

---

## Phase 8: Main Entry Point

### Task 8.1: Implement Main Module
**Priority:** High
**Estimated Effort:** 20 minutes
**Dependencies:** Tasks 5.1, 7.2
**File:** `balanced_token_tree/main.py`
**Line Limit:** 50 lines

**Steps:**
1. Create `main.py`
2. Import `tasks`, `logger_config`, `argparse`, `sys`
3. Implement `main()` function:
   - Set up logging
   - Parse command-line arguments (optional seed)
   - Call `run_pipeline()`
   - Handle exceptions gracefully
   - Print summary
4. Add `if __name__ == "__main__":` block

**Deliverables:**
- Main entry point working
- Command-line argument support
- Clean error messages
- Professional console output

**Verification:**
```bash
cd balanced_token_tree
python main.py --seed 42
# Should complete successfully
```

---

### Task 8.2: Create Package __init__.py
**Priority:** Medium
**Estimated Effort:** 10 minutes
**Dependencies:** All previous tasks
**File:** `balanced_token_tree/__init__.py`

**Steps:**
1. Create `__init__.py` in package root
2. Import main components for convenience:
   - `from .tree_structure import TreeNode, BinaryTree, build_tree`
   - `from .tasks import run_pipeline`
3. Define `__version__`
4. Define `__all__` list

**Deliverables:**
- Package imports working
- Version defined
- Clean public API

**Verification:**
```python
from balanced_token_tree import run_pipeline, __version__
print(__version__)
```

---

## Phase 9: Documentation

### Task 9.1: Create README.md
**Priority:** Medium
**Estimated Effort:** 25 minutes
**Dependencies:** Task 8.1

**Steps:**
1. Create `README.md`
2. Include sections:
   - Project description
   - Installation instructions
   - Usage examples
   - Output description
   - Requirements
   - Author information
   - License (if applicable)
3. Add sample commands
4. Add example output images

**Deliverables:**
- Comprehensive README
- Clear installation steps
- Usage examples

---

## Phase 10: Testing & Validation

### Task 10.1: Manual Testing
**Priority:** High
**Estimated Effort:** 30 minutes
**Dependencies:** All implementation tasks

**Test Cases:**
1. Run with fixed seed, verify reproducibility
2. Check all 3 visualizations generated
3. Verify log files created and rotated
4. Check token conservation across iterations
5. Verify tree structure (16 leaves, proper naming)
6. Test with different random seeds
7. Check variance decreases with balancing

**Deliverables:**
- All test cases pass
- No errors or warnings
- Output as expected

---

### Task 10.2: Code Review & Cleanup
**Priority:** Medium
**Estimated Effort:** 20 minutes
**Dependencies:** Task 10.1

**Steps:**
1. Verify all files under 150 lines
2. Check for unused imports
3. Verify all type hints present
4. Check docstrings complete
5. Verify relative paths used throughout
6. Check for code duplication
7. Ensure consistent style

**Deliverables:**
- Clean, maintainable code
- All constraints met
- No linting errors

---

## Task Checklist

### Phase 1: Setup
- [ ] 1.1 Create project structure
- [ ] 1.2 Set up virtual environment
- [ ] 1.3 Create requirements.txt

### Phase 2: Data Structures
- [ ] 2.1 Implement TreeNode class
- [ ] 2.2 Implement BinaryTree class and build_tree()

### Phase 3: Token Management
- [ ] 3.1 Implement token assignment functions

### Phase 4: Balancing
- [ ] 4.1 Implement balancing core (pairing algorithm)
- [ ] 4.2 Implement balancing application and statistics

### Phase 5: Logging
- [ ] 5.1 Implement logging configuration

### Phase 6: Visualization
- [ ] 6.1 Implement position calculation
- [ ] 6.2 Implement tree drawing

### Phase 7: Orchestration
- [ ] 7.1 Implement task functions
- [ ] 7.2 Implement pipeline orchestration

### Phase 8: Entry Point
- [ ] 8.1 Implement main module
- [ ] 8.2 Create package __init__.py

### Phase 9: Documentation
- [ ] 9.1 Create README.md

### Phase 10: Testing
- [ ] 10.1 Manual testing
- [ ] 10.2 Code review and cleanup

---

## Success Criteria

Upon completion of all tasks, the following should be true:

✅ All Python files are under 150 lines
✅ Virtual environment at ../../venv/ works correctly
✅ Logging system uses ring buffer (20 files × 16 MB)
✅ Tree has exactly 5 levels with correct naming
✅ Random tokens assigned to leaves (0-1000 range)
✅ Balancing algorithm reduces variance
✅ Three visualizations generated (iterations 0, 1, 2)
✅ All paths are relative
✅ No errors or warnings during execution
✅ Clean, documented, maintainable code

---

## Notes

- Tasks can be reordered slightly if dependencies allow
- Some tasks can be done in parallel (e.g., logging while working on visualization)
- Test each task before moving to next
- Commit after each completed task (if using version control)
- If a file exceeds 150 lines, split immediately

---

**Document Status:** Ready for implementation
**Next Step:** Begin with Phase 1, Task 1.1
