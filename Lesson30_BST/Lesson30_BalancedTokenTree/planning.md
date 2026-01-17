# Technical Planning & Architecture
## Balanced Token Tree Project

**Author:** Yair Levi
**Date:** 2026-01-15

---

## 1. System Architecture

### 1.1 High-Level Design

```
┌─────────────────────────────────────────────────────┐
│                    main.py                          │
│              (Entry Point / CLI)                    │
└─────────────────┬───────────────────────────────────┘
                  │
                  v
┌─────────────────────────────────────────────────────┐
│                   tasks.py                          │
│           (Task Orchestration Layer)                │
│  - Run iteration pipeline                           │
│  - Coordinate between modules                       │
│  - Handle multiprocessing                           │
└──┬────────┬────────┬────────────┬──────────────────┘
   │        │        │            │
   v        v        v            v
┌────────┐ ┌──────┐ ┌──────────┐ ┌────────────────┐
│ tree_  │ │token_│ │balancing │ │ visualization  │
│struct  │ │mgr   │ │.py       │ │ .py            │
└────────┘ └──────┘ └──────────┘ └────────────────┘

┌─────────────────────────────────────────────────────┐
│               logger_config.py                      │
│         (Centralized Logging Setup)                 │
└─────────────────────────────────────────────────────┘
```

### 1.2 Module Breakdown

#### Module: `tree_structure.py` (~100 lines)
**Purpose:** Define tree node and structure

**Classes:**
- `TreeNode`: Represents a single node in the tree
  - Attributes: `name`, `level`, `token_count`, `left_child`, `right_child`, `parent`
  - Methods: `set_tokens()`, `calculate_sum()`, `get_all_leaves()`, `__repr__()`

- `BinaryTree`: Manages the complete tree structure
  - Attributes: `root`, `leaves`, `all_nodes`
  - Methods: `build_tree()`, `get_nodes_by_level()`, `reset_tokens()`, `calculate_all_sums()`

#### Module: `token_manager.py` (~80 lines)
**Purpose:** Handle token assignment and random generation

**Functions:**
- `assign_random_tokens(leaves: List[TreeNode], min_val: int, max_val: int) -> None`
- `extract_leaf_tokens(leaves: List[TreeNode]) -> List[int]`
- `assign_token_pairs(leaf_pairs: List[Tuple[TreeNode, TreeNode]], token_pairs: List[Tuple[int, int]]) -> None`

#### Module: `balancing.py` (~90 lines)
**Purpose:** Implement balancing algorithm

**Functions:**
- `sort_tokens(tokens: List[int]) -> List[int]`
- `create_balanced_pairs(sorted_tokens: List[int]) -> List[Tuple[int, int]]`
- `apply_balancing(tree: BinaryTree, iteration: int) -> Dict[str, Any]`
- `calculate_statistics(tree: BinaryTree) -> Dict[str, float]`

**Statistics to Calculate:**
- Total tokens (should remain constant)
- Variance of parent node totals at each level
- Standard deviation
- Min/max parent node values

#### Module: `visualization.py` (~140 lines)
**Purpose:** Generate tree visualizations

**Functions:**
- `calculate_node_positions(tree: BinaryTree) -> Dict[str, Tuple[float, float]]`
- `draw_tree(tree: BinaryTree, output_path: str, title: str) -> None`
- `create_visualization_parallel(tree: BinaryTree, iteration: int) -> str`

**Visualization Details:**
- Use matplotlib with manual positioning
- Horizontal layout (root on left, leaves on right)
- OR vertical layout (root on top, leaves on bottom)
- Node labels: `{name}\n{tokens}`
- Edge drawing with lines
- Color coding by level (optional)

#### Module: `logger_config.py` (~70 lines)
**Purpose:** Configure logging with ring buffer

**Functions:**
- `setup_logging(log_dir: str, level: int) -> logging.Logger`
- `create_rotating_handler(log_dir: str, max_bytes: int, backup_count: int) -> logging.Handler`

**Implementation:**
```python
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

def setup_logging(log_dir: str = "./log", level: int = logging.INFO):
    log_path = Path(log_dir)
    log_path.mkdir(exist_ok=True)

    handler = RotatingFileHandler(
        log_path / "app.log",
        maxBytes=16 * 1024 * 1024,  # 16 MB
        backupCount=19  # Total 20 files (app.log + 19 backups)
    )

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)

    logger = logging.getLogger()
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger
```

#### Module: `tasks.py` (~130 lines)
**Purpose:** Orchestrate the complete workflow

**Functions:**
- `task_create_tree() -> BinaryTree`
- `task_initial_tokens(tree: BinaryTree) -> None`
- `task_balance_iteration(tree: BinaryTree, iteration: int) -> Dict[str, Any]`
- `task_visualize(tree: BinaryTree, iteration: int, label: str) -> None`
- `run_pipeline() -> None`

**Pipeline Flow:**
```python
def run_pipeline():
    logger.info("Starting pipeline")

    # 1. Create tree
    tree = task_create_tree()

    # 2. Initial tokens and visualize
    task_initial_tokens(tree)
    task_visualize(tree, 0, "initial")

    # 3. First balancing iteration
    stats1 = task_balance_iteration(tree, 1)
    task_visualize(tree, 1, "balanced")

    # 4. Second balancing iteration
    stats2 = task_balance_iteration(tree, 2)
    task_visualize(tree, 2, "balanced")

    logger.info("Pipeline completed")
    return stats1, stats2
```

#### Module: `main.py` (~50 lines)
**Purpose:** Entry point

**Functionality:**
- Parse command-line arguments (if any)
- Set up logging
- Call `tasks.run_pipeline()`
- Handle exceptions
- Display summary

---

## 2. Data Structures

### 2.1 TreeNode Class

```python
from typing import Optional, List

class TreeNode:
    def __init__(self, name: str, level: int):
        self.name: str = name
        self.level: int = level
        self.token_count: int = 0
        self.left_child: Optional[TreeNode] = None
        self.right_child: Optional[TreeNode] = None
        self.parent: Optional[TreeNode] = None

    def is_leaf(self) -> bool:
        return self.left_child is None and self.right_child is None

    def calculate_sum(self) -> int:
        if self.is_leaf():
            return self.token_count

        left_sum = self.left_child.calculate_sum() if self.left_child else 0
        right_sum = self.right_child.calculate_sum() if self.right_child else 0
        self.token_count = left_sum + right_sum
        return self.token_count
```

### 2.2 Tree Building Algorithm

```python
def build_tree() -> BinaryTree:
    """Build a complete binary tree with 5 levels."""

    # Level 1: Create 16 leaves
    leaves = [TreeNode(f"1_{i+1}", level=1) for i in range(16)]

    # Level 2: Create 8 nodes, connect to leaves
    level2 = []
    for i in range(8):
        node = TreeNode(f"2_{i+1}", level=2)
        node.left_child = leaves[i * 2]
        node.right_child = leaves[i * 2 + 1]
        leaves[i * 2].parent = node
        leaves[i * 2 + 1].parent = node
        level2.append(node)

    # Level 3: Create 4 nodes
    level3 = []
    for i in range(4):
        node = TreeNode(f"3_{i+1}", level=3)
        node.left_child = level2[i * 2]
        node.right_child = level2[i * 2 + 1]
        level2[i * 2].parent = node
        level2[i * 2 + 1].parent = node
        level3.append(node)

    # Level 4: Create 2 nodes
    level4 = []
    for i in range(2):
        node = TreeNode(f"4_{i+1}", level=4)
        node.left_child = level3[i * 2]
        node.right_child = level3[i * 2 + 1]
        level3[i * 2].parent = node
        level3[i * 2 + 1].parent = node
        level4.append(node)

    # Level 5: Create root
    root = TreeNode("5_1", level=5)
    root.left_child = level4[0]
    root.right_child = level4[1]
    level4[0].parent = root
    level4[1].parent = root

    return BinaryTree(root, leaves)
```

---

## 3. Algorithm Details

### 3.1 Balancing Algorithm

**Input:** List of token counts from leaves
**Output:** Rebalanced tree with same total tokens

```python
def create_balanced_pairs(tokens: List[int]) -> List[Tuple[int, int]]:
    """
    Pair largest with smallest tokens for balanced distribution.

    Example:
        Input: [100, 200, 300, 400, 500, 600, 700, 800]
        Sorted: [100, 200, 300, 400, 500, 600, 700, 800]

        Pairs:
        1. (100, 800) = 900
        2. (200, 700) = 900
        3. (300, 600) = 900
        4. (400, 500) = 900

        Result: Perfect balance with all parent sums equal
    """
    sorted_tokens = sorted(tokens)
    pairs = []

    while sorted_tokens:
        smallest = sorted_tokens.pop(0)
        largest = sorted_tokens.pop()  # pop() removes last element
        pairs.append((smallest, largest))

    return pairs
```

**Why This Works:**
- Pairing extremes distributes variance
- Each parent gets one low and one high value
- Minimizes differences between parent node totals
- Converges toward optimal distribution

### 3.2 Token Assignment

```python
def assign_token_pairs(
    leaf_pairs: List[Tuple[TreeNode, TreeNode]],
    token_pairs: List[Tuple[int, int]]
) -> None:
    """Assign token pairs to leaf pairs."""
    for (left_leaf, right_leaf), (token1, token2) in zip(leaf_pairs, token_pairs):
        left_leaf.token_count = token1
        right_leaf.token_count = token2
```

### 3.3 Sum Propagation

```python
def propagate_sums(root: TreeNode) -> None:
    """Calculate sums from leaves to root (post-order traversal)."""
    if root is None:
        return

    if root.is_leaf():
        return  # Leaf tokens already set

    propagate_sums(root.left_child)
    propagate_sums(root.right_child)

    root.token_count = (
        root.left_child.token_count + root.right_child.token_count
    )
```

---

## 4. Visualization Design

### 4.1 Layout Strategy

**Vertical Layout (Recommended):**
```
            5_1 (5000)
              /    \
       4_1 (2500)  4_2 (2500)
         /   \       /   \
    3_1    3_2    3_3    3_4
    ...    ...    ...    ...
```

**Position Calculation:**
- X coordinate: Based on in-order traversal position
- Y coordinate: Based on level (5 at top, 1 at bottom)
- Spacing: Proportional to level depth

```python
def calculate_positions(tree: BinaryTree) -> Dict[str, Tuple[float, float]]:
    positions = {}

    # Get leaves in left-to-right order
    leaves = tree.get_all_leaves_sorted()
    x_spacing = 1.0

    # Position leaves
    for i, leaf in enumerate(leaves):
        positions[leaf.name] = (i * x_spacing, 0)

    # Position internal nodes (centered between children)
    for level in range(2, 6):
        nodes = tree.get_nodes_by_level(level)
        for node in nodes:
            left_x, left_y = positions[node.left_child.name]
            right_x, right_y = positions[node.right_child.name]
            x = (left_x + right_x) / 2
            y = level - 1
            positions[node.name] = (x, y)

    return positions
```

### 4.2 Rendering

```python
import matplotlib.pyplot as plt

def draw_tree(tree: BinaryTree, output_path: str, title: str):
    fig, ax = plt.subplots(figsize=(16, 10))
    positions = calculate_positions(tree)

    # Draw edges
    for node in tree.all_nodes:
        if not node.is_leaf():
            x1, y1 = positions[node.name]
            x2, y2 = positions[node.left_child.name]
            ax.plot([x1, x2], [y1, y2], 'k-', linewidth=1)

            x3, y3 = positions[node.right_child.name]
            ax.plot([x1, x3], [y1, y3], 'k-', linewidth=1)

    # Draw nodes
    for node in tree.all_nodes:
        x, y = positions[node.name]
        color = 'lightblue' if node.is_leaf() else 'lightgreen'
        ax.scatter(x, y, s=800, c=color, zorder=2)
        ax.text(x, y, f"{node.name}\n{node.token_count}",
                ha='center', va='center', fontsize=8)

    ax.set_title(title, fontsize=14)
    ax.axis('off')
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
```

---

## 5. Multiprocessing Strategy

### 5.1 Parallelization Opportunities

**1. Visualization (Best candidate)**
```python
from multiprocessing import Pool

def generate_all_visualizations(trees: List[BinaryTree], iterations: List[int]):
    with Pool(processes=3) as pool:
        pool.starmap(task_visualize, zip(trees, iterations))
```

**2. Statistics Calculation**
- Calculate variance for multiple levels in parallel
- Minimal benefit for this tree size

**3. Token Assignment**
- Not beneficial (operation is already fast)

### 5.2 Implementation Decision

**Use multiprocessing for:**
- Generating multiple visualizations if saving in different formats
- Future: Processing multiple trees concurrently

**Don't use multiprocessing for:**
- Tree building (too fast, overhead not worth it)
- Balancing algorithm (sequential by nature)
- Token assignment (too fast)

**Current Scope:** Implement multiprocessing for visualization generation if time permits, otherwise keep sequential.

---

## 6. Error Handling

### 6.1 Potential Errors

1. **Log Directory Creation Failure**
   - Handler: Create directory with proper permissions
   - Fallback: Log to console only

2. **Visualization Backend Unavailable (WSL)**
   - Handler: Use `matplotlib.use('Agg')` at import
   - Fallback: Skip visualization, log warning

3. **Invalid Tree Structure**
   - Handler: Validate tree after building
   - Raise: Custom exception with details

4. **Token Assignment Mismatch**
   - Handler: Verify token count before/after balancing
   - Raise: If totals don't match

### 6.2 Validation Functions

```python
def validate_tree_structure(tree: BinaryTree) -> None:
    """Ensure tree has correct structure."""
    assert len(tree.leaves) == 16, "Must have 16 leaves"
    assert tree.root.level == 5, "Root must be level 5"

    for node in tree.all_nodes:
        if not node.is_leaf():
            assert node.left_child is not None
            assert node.right_child is not None

def validate_token_conservation(before: int, after: int) -> None:
    """Ensure total tokens unchanged."""
    assert before == after, f"Token count mismatch: {before} != {after}"
```

---

## 7. File Organization

```
Lesson30_BalancedTokenTree/
│
├── balanced_token_tree/       # Main package
│   ├── __init__.py
│   ├── main.py
│   ├── tree_structure.py
│   ├── token_manager.py
│   ├── balancing.py
│   ├── visualization.py
│   ├── logger_config.py
│   └── tasks.py
│
├── log/                       # Created at runtime
│   └── app.log               # Ring buffer logs
│
├── output/                    # Created at runtime
│   ├── tree_iteration_0_initial.png
│   ├── tree_iteration_1_balanced.png
│   └── tree_iteration_2_balanced.png
│
├── PRD.md
├── Claude.md
├── planning.md               # This file
├── tasks.md
├── requirements.txt
└── README.md                 # User guide
```

---

## 8. Performance Estimates

### 8.1 Time Complexity

- Tree building: O(n) where n = 31 nodes → ~1ms
- Token assignment: O(16) → ~1ms
- Balancing sort: O(n log n) where n = 16 → ~1ms
- Sum propagation: O(n) where n = 31 → ~1ms
- Visualization: O(n) rendering → 100-500ms
- **Total per iteration:** ~500ms

### 8.2 Space Complexity

- Tree nodes: 31 * ~200 bytes = ~6 KB
- Token list: 16 * 8 bytes = 128 bytes
- Visualization: ~1-5 MB per PNG
- Log buffer: Up to 320 MB total
- **Total:** < 350 MB worst case

---

## 9. Testing Plan

### 9.1 Unit Tests (Optional but Recommended)

```python
def test_tree_creation():
    tree = build_tree()
    assert len(tree.leaves) == 16
    assert tree.root.name == "5_1"

def test_balancing_pairs():
    tokens = [100, 200, 300, 400]
    pairs = create_balanced_pairs(tokens)
    assert pairs == [(100, 400), (200, 300)]

def test_token_conservation():
    tree = build_tree()
    assign_random_tokens(tree.leaves, 0, 1000)
    initial_sum = tree.root.calculate_sum()

    apply_balancing(tree, 1)
    final_sum = tree.root.calculate_sum()

    assert initial_sum == final_sum
```

### 9.2 Integration Test

```python
def test_full_pipeline():
    run_pipeline()

    # Check output files exist
    assert Path("output/tree_iteration_0_initial.png").exists()
    assert Path("output/tree_iteration_1_balanced.png").exists()
    assert Path("output/tree_iteration_2_balanced.png").exists()

    # Check logs exist
    assert Path("log/app.log").exists()
```

---

## 10. Future Enhancements

### 10.1 Phase 2 Features
- Configurable tree depth
- Multiple balancing algorithms (comparison)
- Interactive visualization with zoom
- Animation showing balancing process
- Export tree to JSON/XML

### 10.2 Phase 3 Features
- Web interface with Flask
- Real-time updates
- Historical comparison
- Performance benchmarks
- Unit test suite

---

## 11. Open Questions

1. **Balancing Goal Interpretation:**
   - Current: Minimize variance of parent node totals
   - Alternative: Balance tree height (not applicable here)
   - **Decision:** Proceed with variance minimization

2. **Visualization Format:**
   - PNG (default), PDF, SVG?
   - **Decision:** PNG at 150 DPI

3. **Random Seed:**
   - Fixed for reproducibility or truly random?
   - **Decision:** Use fixed seed for testing, configurable

4. **Statistics Display:**
   - Show in visualization or separate report?
   - **Decision:** Log to console and include in image title

---

**Document Status:** Complete
**Ready for Implementation:** Yes
**Next Step:** Review tasks.md for implementation order
