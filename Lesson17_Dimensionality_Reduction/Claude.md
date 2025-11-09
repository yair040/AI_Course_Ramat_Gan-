# Claude Context Document
## PCA and t-SNE Text Vectorization Project

### Purpose
This document provides context for AI assistants (like Claude) to understand the project structure, constraints, and implementation approach.

### Project Context

#### Background
This is an educational/research project comparing different dimensionality reduction techniques:
1. **Manual PCA**: Implemented from mathematical first principles using only NumPy
2. **Library PCA**: Using sklearn's optimized implementation
3. **t-SNE**: Using sklearn's t-SNE for non-linear dimensionality reduction

The goal is to understand the mathematical foundations of PCA while also comparing performance with modern libraries.

#### Target Environment
- **OS**: WSL (Windows Subsystem for Linux)
- **Python**: Virtual environment (venv)
- **Package Management**: pip
- **Development**: Command-line focused

### Design Constraints

#### Code Organization
- **Maximum file length**: 150-200 lines per file
- **Rationale**: Maintainability and readability
- **Approach**: Modular design with task-specific files
- **Main program**: Orchestration only, delegates to task modules

#### Library Restrictions
- **Task 3 (Manual PCA)**: NumPy ONLY - no sklearn, no scipy linalg beyond basic operations
- **Tasks 4-5**: Use standard libraries (sklearn encouraged)
- **Reasoning**: Educational value in implementing PCA manually

### Mathematical Implementation Notes

#### Task 3: Manual PCA Deep Dive

**Critical Implementation Details**:

1. **Covariance Matrix**:
   ```python
   # X is matrix with vectors as COLUMNS
   S = (X.T @ X) / (n - 1)
   # NOT: X @ X.T (that would be wrong dimensionality)
   ```

2. **Eigenvalue/Eigenvector Calculation**:
   - User wants solution via characteristic equation: det(S - λI) = 0
   - For small matrices: Can use `numpy.linalg.eig()` as it's basic linear algebra
   - For educational rigor: Show the mathematical process clearly
   - Eigenvectors must be sorted by eigenvalue (descending)

3. **Transformation Matrix P**:
   - Columns are eigenvectors
   - Ordered by eigenvalue magnitude (largest first)
   - Take only first 3 columns (top 3 principal components)

4. **Projection**:
   ```python
   # For each original vector v:
   new_v = P.T @ v
   # Result is 3D vector
   ```

5. **Timing Requirements**:
   - Time each lettered step (a through k)
   - Use `time.perf_counter()` for precision
   - Display in milliseconds or seconds as appropriate

#### Vectorization Strategy

The user doesn't specify which vectorization model to use. Recommended approach:
- **sentence-transformers**: Modern, effective, easy to use
- **Model suggestion**: `all-MiniLM-L6-v2` (fast, lightweight, good quality)
- **Alternative**: `all-mpnet-base-v2` (higher quality, slower)
- **Normalization**: L2 normalization to unit length

#### Sentence Generation Strategy

**Requirements**:
- 100 sentences
- Random assignment to: sport, food, work
- "Short sentences"

**Suggested Approach**:
1. Create template-based generator for variety
2. Use random selection from predefined patterns
3. Ensure semantic differences between categories
4. Keep sentences natural but simple

**Example Templates**:
- Sport: "I enjoy playing [sport]", "The [team] won the championship"
- Food: "I love eating [food]", "The [dish] tastes delicious"
- Work: "The meeting starts at [time]", "I finished the [task]"

### File Architecture

#### main.py
- Import all task modules
- Execute tasks in sequence
- Handle command-line arguments (if any)
- Overall error handling
- Summary reporting

#### task1_generate.py
- Function: `generate_sentences(count=100) -> list[str]`
- Save to sentences.txt
- Print to console
- Return list for next task

#### task2_vectorize.py
- Function: `vectorize_sentences(sentences: list[str]) -> np.ndarray`
- Load sentences from file if needed
- Convert to embeddings
- Normalize to unit vectors
- Save to normalized.txt
- Return normalized array

#### task3_manual_pca.py
- Function: `manual_pca_pipeline(vectors: np.ndarray) -> dict`
- All steps (a-k) as separate functions
- Time each step individually
- Save transformed vectors
- K-means clustering
- Generate visualization
- Return results dict

#### task4_sklearn_pca.py
- Function: `sklearn_pca_pipeline(vectors: np.ndarray) -> dict`
- Use sklearn.decomposition.PCA
- Time each major step
- K-means clustering
- Generate visualization
- Return results dict

#### task5_tsne.py
- Function: `tsne_pipeline(vectors: np.ndarray) -> dict`
- Use sklearn.manifold.TSNE
- Time each major step
- K-means clustering
- Generate visualization
- Return results dict

#### utils.py
- Timing decorator or context manager
- File I/O helpers
- Common constants
- Configuration values

#### visualization.py
- Function: `plot_3d_clusters(points_3d, labels, title, sentence_ids=None)`
- Matplotlib 3D scatter plot
- Color by cluster
- Optional: Display point numbers for traceability
- Save figure option
- Consistent styling across all plots

### Key Technical Decisions

#### Why NumPy-only for Task 3?
Educational value: Understanding PCA's mathematical foundation by implementing the actual steps rather than using a black-box library.

#### Why Compare Three Methods?
1. **Manual PCA**: Understanding + control
2. **sklearn PCA**: Performance + reliability
3. **t-SNE**: Non-linear alternative, often better for visualization

#### Timing Granularity
- Task 3: Time each lettered step (11 steps)
- Tasks 4-5: Time major operations (loading, transformation, clustering, visualization)

### Expected Challenges

1. **Eigenvalue/Eigenvector Computation**:
   - NumPy's `linalg.eig()` should be acceptable
   - If user wants fully manual: Would need to implement power iteration or QR algorithm
   - Clarify if needed

2. **Numerical Stability**:
   - Centering data is crucial
   - Watch for near-zero eigenvalues
   - Eigenvector normalization

3. **K-Means Randomness**:
   - Set random seed for reproducibility
   - Document seed value

4. **Visualization Clarity**:
   - 100 points with numbers may be crowded
   - Consider: hover tooltips, or separate legend, or adjustable point size

5. **File Line Limits**:
   - Task 3 has many steps - may need to split into helper functions
   - Keep visualization code in separate module

### Testing Strategy

**Validation Checks**:
1. Verify 100 sentences generated (count check)
2. Verify vectors are normalized (unit length check)
3. Verify 3D output from all methods (shape check: 100x3)
4. Verify clusters sum to 100 points
5. Compare eigenvalue ordering (should be descending)

**Sanity Checks**:
1. PCA explained variance should be reasonable
2. Clusters should show some separation
3. Manual PCA and sklearn PCA should give similar results (possibly sign-flipped)
4. t-SNE results will differ but should still show structure

### Performance Expectations

**Approximate Timing** (on moderate hardware):
- Sentence generation: <1 second
- Vectorization: 1-3 seconds
- Manual PCA: 0.1-1 second (100 vectors, moderate dimensions)
- sklearn PCA: <0.1 second
- t-SNE: 2-10 seconds (most expensive)
- K-means: <0.5 second each
- Visualization: <1 second each

### Common Pitfalls to Avoid

1. **Matrix Dimensions**:
   - Watch whether vectors are rows or columns
   - Covariance matrix formula depends on this

2. **Eigenvalue Sorting**:
   - Must sort in descending order
   - Eigenvectors must be reordered correspondingly

3. **Transpose Confusion**:
   - P or P^T for transformation? (Depends on vector orientation)
   - Be consistent

4. **Normalization**:
   - Task 2 vectors must be normalized before PCA/t-SNE
   - Don't normalize again in later tasks

5. **File Path Handling**:
   - Use pathlib or os.path for cross-platform compatibility
   - WSL can access Windows files but path formats differ

### Development Workflow

**Recommended Order**:
1. Set up virtual environment
2. Create requirements.txt and install dependencies
3. Implement utils.py (timing, I/O)
4. Implement task1 and test
5. Implement task2 and test
6. Implement visualization.py
7. Implement task3 (most complex)
8. Implement task4 (quick)
9. Implement task5
10. Create main.py orchestration
11. Full integration test
12. Documentation updates

### Success Indicators

When complete, you should have:
- ✅ All sentences appear semantically related to their category
- ✅ All timing outputs are clear and readable
- ✅ Three distinct 3D visualizations
- ✅ Manual PCA matches sklearn PCA (approximately)
- ✅ All code files respect 150-200 line limit
- ✅ No hard-coded paths that won't work on WSL
- ✅ Clear console output explaining what's happening
- ✅ Reproducible results (seeded randomness)

### Questions to Consider

If implementing this project, consider asking the user:
1. Which sentence embedding model to use?
2. Should K-means be seeded for reproducibility?
3. Should plots be displayed interactively or saved to files?
4. Preferred precision for timing outputs (ms/s)?
5. Should intermediate matrices be saved for inspection?

### References

**Mathematical Background**:
- PCA: Linear dimensionality reduction via eigendecomposition
- t-SNE: Non-linear manifold learning technique
- K-means: Partition-based clustering algorithm

**Key Libraries**:
- NumPy: Numerical computing
- sklearn: Machine learning algorithms
- matplotlib: Plotting and visualization
- sentence-transformers: Text embeddings
