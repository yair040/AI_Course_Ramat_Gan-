# Quick Start Guide
## Balanced Token Tree

**Author:** Yair Levi

---

## Installation Steps

### 1. Navigate to Virtual Environment Location
```bash
cd ../..
```

### 2. Create Virtual Environment
```bash
python3 -m venv venv
```

### 3. Activate Virtual Environment
```bash
source venv/bin/activate
```

### 4. Return to Project Directory
```bash
cd Lesson30/Lesson30_BalancedTokenTree
```

### 5. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## Running the Program

### Basic Run (Random Seed)
```bash
cd balanced_token_tree
python main.py
```

### Run with Fixed Seed (Reproducible)
```bash
cd balanced_token_tree
python main.py --seed 42
```

### Run with Debug Logging
```bash
cd balanced_token_tree
python main.py --seed 42 --log-level DEBUG
```

---

## Expected Output

The program runs **2 complete iterations**:

**Iteration 0:**
1. Create a 5-level binary tree with 16 leaves
2. Assign random tokens (0-1000) to each leaf
3. Visualize the initial tree
4. Apply balancing algorithm (pairs largest with smallest)
5. Visualize the balanced tree

**Iteration 1:**
6. Assign NEW random tokens (0-1000) to each leaf
7. Visualize the new initial tree
8. Apply balancing algorithm again
9. Visualize the balanced tree

### Output Files

**Visualizations** (in `output/` directory):
- `tree_iteration_0_initial.png` - First random distribution
- `tree_iteration_0_balanced.png` - After first balancing
- `tree_iteration_1_initial.png` - Second random distribution
- `tree_iteration_1_balanced.png` - After second balancing

**Log Files** (in `log/` directory):
- `app.log` (with automatic rotation up to 20 files × 16 MB)

---

## Quick Test

```bash
# From project root
cd balanced_token_tree
python -c "from balanced_token_tree import run_pipeline; run_pipeline(seed=42)"
```

This should complete successfully and generate all output files.

---

## Troubleshooting

### ImportError
Make sure you're in the correct directory:
```bash
pwd  # Should show: .../Lesson30_BalancedTokenTree/balanced_token_tree
```

### Virtual Environment Not Active
```bash
which python  # Should show: .../venv/bin/python
```

If not, activate it:
```bash
source ../../../venv/bin/activate
```

### matplotlib Issues on WSL
The program uses `matplotlib.use('Agg')` for headless operation, so no display server is needed.

---

## File Size Verification

All Python files are under 150 lines:
```bash
wc -l *.py
```

Expected output:
- All files ≤ 150 lines
- Total: ~850 lines

---

**Ready to Run!** 🚀
