# Quick Start Guide

## Installation (One-time setup)

Run the setup script:
```bash
cd /home/ro/PCA_tSNE
chmod +x setup.sh
./setup.sh
```

Or manually:
```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## Running the Program

### Option 1: Run Everything
```bash
source venv/bin/activate
python main.py
```

This executes all 5 tasks in sequence and displays 3 interactive 3D visualizations.

### Option 2: Run Individual Tasks
```bash
source venv/bin/activate

# Task 1: Generate 100 sentences
python task1_generate.py

# Task 2: Convert to normalized vectors
python task2_vectorize.py

# Task 3: Manual PCA (NumPy only, 11 timed steps)
python task3_manual_pca.py

# Task 4: sklearn PCA (fast, optimized)
python task4_sklearn_pca.py

# Task 5: t-SNE (non-linear, slower)
python task5_tsne.py
```

## What to Expect

### Execution Time
- **Total**: 15-30 seconds (depending on your hardware)
- Task 1: <1 second
- Task 2: 3-5 seconds (model loading)
- Task 3: 1-2 seconds
- Task 4: <1 second
- Task 5: 5-15 seconds (most intensive)

### Output Files
After running, you'll have:
- `sentences.txt` - 100 generated sentences
- `normalized.txt` - Normalized vectors (100 × 384)
- `pca_transformed_manual.txt` - Manual PCA output (100 × 3)
- `pca_transformed_sklearn.txt` - sklearn PCA output (100 × 3)
- `tsne_transformed.txt` - t-SNE output (100 × 3)

### Visualizations
You'll see 3 interactive 3D plots:
1. Manual PCA + K-Means
2. sklearn PCA + K-Means
3. t-SNE + K-Means

Each shows 100 points colored by cluster (3 clusters), with point IDs labeled.

## Troubleshooting

### "No module named 'sentence_transformers'"
Run the setup script again or install dependencies:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### "Display not available"
For WSL without X11:
```bash
export DISPLAY=:0
```
Or modify visualization functions to save plots to files instead.

### "Memory error"
Reduce `NUM_SENTENCES` in `utils.py` to 50 or fewer.

## Next Steps

1. Review generated sentences in `sentences.txt`
2. Examine the 3D visualizations
3. Compare clustering results between methods
4. Check timing outputs for each step
5. Explore the code in each task file

## Documentation

- **README.md** - Complete project documentation
- **PRD.md** - Product requirements
- **Claude.md** - AI assistant context
- **planning.md** - Technical architecture
- **tasks.md** - Implementation breakdown

Enjoy exploring dimensionality reduction!
