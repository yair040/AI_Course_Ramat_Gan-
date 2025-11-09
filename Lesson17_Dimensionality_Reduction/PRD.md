# Product Requirements Document (PRD)
## PCA and t-SNE Text Vectorization & Clustering System

### Project Overview
A Python-based system for text vectorization, dimensionality reduction, and clustering analysis. The project compares manual PCA implementation with library-based approaches (PCA and t-SNE) for 3D visualization of sentence embeddings.

### Environment Requirements
- **Platform**: WSL (Windows Subsystem for Linux)
- **Python Environment**: Virtual environment (venv)
- **Code Structure**: Modular design with each Python file ≤ 150-200 lines
- **Architecture**: Main program orchestrates task modules

### Functional Requirements

#### 1. Sentence Generation
- Generate 100 random short sentences
- Each sentence randomly assigned to one of three subjects:
  - Sport
  - Food
  - Work
- **Outputs**:
  - Print sentences to console
  - Save to `sentences.txt`

#### 2. Text Vectorization
- Convert 100 sentences to vector embeddings
- Normalize all vectors (unit length)
- **Output**:
  - Save normalized vectors to `normalized.txt`

#### 3. Manual PCA Implementation (NumPy Only)
**Constraint**: No sklearn allowed, NumPy only

**Process Steps** (with timing measurements):
1. **Mean Calculation**
   - Calculate mean for each feature across all vectors

2. **Centering**
   - Subtract mean from each feature value
   - Center data around zero

3. **Matrix Construction**
   - Arrange centered vectors as columns in matrix X

4. **Covariance Matrix**
   - Compute S = (X^T × X) / (n-1)
   - Where n = 100 (number of vectors)

5. **Eigenvalue Calculation**
   - Solve det(S - λI) = 0
   - Where λ = eigenvalues, I = identity matrix

6. **Eigenvector Calculation**
   - Solve (S - λI) × V = 0
   - Where V = eigenvectors

7. **Transformation Matrix**
   - Build matrix P from eigenvectors
   - Order by eigenvalue magnitude (descending)
   - Select top 3 eigenvectors only

8. **Transpose Calculation**
   - Compute P^T

9. **Dimensionality Reduction**
   - Transform each vector: new_vector = P^T × original_vector
   - Result: 100 vectors in 3D space
   - Save transformed vectors to file

10. **K-Means Clustering**
    - Cluster 100 3D vectors with K=3

11. **Visualization**
    - 3D scatter plot
    - Color by cluster assignment
    - Display serial numbers for each point (to trace back to original sentence)

**Performance Requirements**:
- Measure and print execution time for each step

#### 4. Library-Based PCA (sklearn)
**Constraint**: Use sklearn or similar libraries for fastest implementation

**Process Steps** (with timing measurements):
1. Apply PCA to normalized vectors from Task 2
2. Reduce to 3 dimensions
3. K-Means clustering (K=3)
4. 3D visualization with:
   - Points colored by cluster
   - Serial numbers displayed for traceability

**Performance Requirements**:
- Measure and print execution time for each step

#### 5. t-SNE Dimensionality Reduction
**Constraint**: Use built-in libraries (sklearn, etc.)

**Process Steps** (with timing measurements):
1. Apply t-SNE to normalized vectors from Task 2
2. Reduce to 3 dimensions
3. K-Means clustering (K=3)
4. 3D visualization with:
   - Points colored by cluster
   - Serial numbers displayed for traceability

**Performance Requirements**:
- Measure and print execution time for each step

### Non-Functional Requirements

#### Code Quality
- Maximum 150-200 lines per Python file
- Modular architecture
- Clear function separation
- Type hints recommended
- Proper error handling

#### Performance
- All timing measurements displayed with appropriate precision
- Efficient memory usage for 100-vector dataset

#### Usability
- Clear console output
- Informative progress messages
- Easy-to-read visualizations
- Labeled axes in 3D plots

#### Maintainability
- Well-documented code
- Clear file naming conventions
- Logical task separation
- Configuration constants at top of files

### File Structure
```
PCA_tSNE/
├── main.py                    # Main orchestration program
├── task1_generate.py          # Sentence generation
├── task2_vectorize.py         # Text to normalized vectors
├── task3_manual_pca.py        # Manual PCA implementation
├── task4_sklearn_pca.py       # sklearn PCA implementation
├── task5_tsne.py              # t-SNE implementation
├── utils.py                   # Shared utilities (timing, etc.)
├── visualization.py           # 3D plotting functions
├── requirements.txt           # Python dependencies
├── sentences.txt              # Generated sentences (output)
├── normalized.txt             # Normalized vectors (output)
├── PRD.md                     # This document
├── Claude.md                  # AI assistant context
├── planning.md                # Technical planning document
└── tasks.md                   # Task breakdown document
```

### Dependencies
- Python 3.8+
- NumPy (mathematical operations)
- sentence-transformers or similar (text vectorization)
- scikit-learn (PCA, t-SNE, K-Means)
- matplotlib (3D visualization)
- Any required supporting libraries

### Success Criteria
1. All 100 sentences generated and saved
2. Vectors properly normalized
3. Manual PCA produces correct 3D transformation
4. All three methods (manual PCA, sklearn PCA, t-SNE) complete successfully
5. All visualizations clearly show clusters
6. Timing measurements provided for all steps
7. Code structure adheres to line limits
8. Program runs successfully in WSL virtual environment

### Deliverables
1. Working Python application
2. All output files (sentences.txt, normalized.txt, transformed vectors)
3. 3D visualizations (3 plots total)
4. Documentation (PRD.md, Claude.md, planning.md, tasks.md)
5. requirements.txt for reproducibility

### Out of Scope
- Real-time processing
- Web interface
- Database integration
- Multi-language support
- GPU acceleration
- Production deployment

### Future Enhancements (Optional)
- Comparison metrics between methods
- Additional clustering algorithms
- Parameter tuning interface
- Batch processing for larger datasets
- Interactive 3D visualizations
